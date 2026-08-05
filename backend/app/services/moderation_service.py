"""
Scoring user-submitted text for abuse and spam.

DevLink's moderation story today is entirely reactive: something gets posted,
somebody reads it, somebody reports it, a moderator eventually acts. That works
for a small community and stops working the moment the platform is worth
spamming.

This is the deterministic layer that runs on every write. It returns a
**recommendation**, not a verdict:

    ALLOW   nothing interesting
    FLAG    publish it, but queue it for review
    REVIEW  hold it, a moderator decides
    BLOCK   refuse it, and tell the author why

The caller decides what to do with the recommendation, because a profile bio
and a direct message should not share a threshold. That is a call-site
decision, not a property of the text.

Every result carries the rules that fired and what each contributed. An
unexplainable moderation decision is an unappealable one, and somebody will
eventually have to answer a "why was my post blocked" ticket.

Deliberately not a model. A model cannot be unit-tested against "does
Scunthorpe still work", and this layer has to be cheap enough to run inline on
every submission.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from urllib.parse import urlparse

from app.core.moderation_terms import (
    ALLOWED_DOMAINS,
    CONTACT_SOLICITATION,
    EMAIL_PATTERN,
    HARASSMENT,
    PHONE_PATTERN,
    PROFANITY,
    SLURS,
    SPAM_PHRASES,
    URL_PATTERN,
    URL_SHORTENERS,
)
from app.utils.text_normalize import (
    evasion_pattern,
    normalise,
    repeated_character_runs,
    shout_ratio,
    words,
)

# Compiled once at import. Only terms of four characters or more get an
# evasion pattern: below that the pattern is loose enough to start matching
# ordinary text, and the short terms on the list are the mild ones anyway.
_EVASION_PATTERNS = [
    (term, evasion_pattern(term))
    for term in sorted(PROFANITY | SLURS)
    if len(term) >= 4
]


class Action(str, Enum):
    ALLOW = "allow"
    FLAG = "flag"
    REVIEW = "review"
    BLOCK = "block"


class Category(str, Enum):
    PROFANITY = "profanity"
    HARASSMENT = "harassment"
    SLUR = "slur"
    SPAM = "spam"
    CONTACT_HARVESTING = "contact_harvesting"
    FORMATTING = "formatting"


# Score thresholds. These are the defaults; a caller that wants a stricter or
# looser line passes its own.
DEFAULT_THRESHOLDS = {
    Action.BLOCK: 1.0,
    Action.REVIEW: 0.6,
    Action.FLAG: 0.3,
}

# Below this many characters the ratio-based signals are meaningless -- "OK!"
# is 100% uppercase and is not shouting.
MIN_LENGTH_FOR_RATIOS = 20


@dataclass(frozen=True)
class Signal:
    """One rule that fired, and what it contributed."""

    category: Category
    rule: str
    weight: float
    detail: str = ""


@dataclass
class ModerationResult:
    """
    The verdict on a piece of text.

    ``score`` is unbounded above; it saturates at the block threshold in
    practice, but leaving it uncapped means the difference between "one swear
    word" and "a wall of slurs" survives into the audit log.
    """

    action: Action
    score: float
    signals: list[Signal] = field(default_factory=list)

    @property
    def categories(self) -> set[Category]:
        return {s.category for s in self.signals}

    @property
    def is_allowed(self) -> bool:
        return self.action == Action.ALLOW

    @property
    def needs_human(self) -> bool:
        return self.action in (Action.REVIEW, Action.BLOCK)

    def explain(self) -> str:
        """
        A one-line, human-readable reason.

        This is what ends up in a moderator queue and, in redacted form, in the
        message shown to the author.
        """
        if not self.signals:
            return "No moderation signals."

        parts = [f"{s.rule} ({s.weight:+.2f})" for s in self.signals]
        return f"{self.action.value} @ {self.score:.2f}: " + ", ".join(parts)


@dataclass(frozen=True)
class AuthorContext:
    """
    What we know about who is writing.

    Optional, and the service works without it, but it changes the answer a
    lot. A brand-new account posting five links is not the same event as a
    two-year-old account doing it, and no amount of keyword matching can tell
    those apart.
    """

    account_age_days: Optional[int] = None
    prior_flags: int = 0
    is_verified: bool = False


class ModerationService:
    """Pure scoring. No database, no network, no state."""

    def check(
        self,
        text: str,
        *,
        author: Optional[AuthorContext] = None,
        thresholds: Optional[dict] = None,
    ) -> ModerationResult:
        """Score a piece of text and recommend an action."""
        if not text or not text.strip():
            return ModerationResult(action=Action.ALLOW, score=0.0)

        signals: list[Signal] = []
        signals.extend(self._abuse_signals(text))
        signals.extend(self._spam_signals(text))
        signals.extend(self._formatting_signals(text))

        score = sum(s.weight for s in signals)
        score *= self._author_multiplier(author, signals)

        return ModerationResult(
            action=self._action_for(score, thresholds or DEFAULT_THRESHOLDS),
            score=round(score, 3),
            signals=signals,
        )

    # ------------------------------------------------------------------
    # Abuse
    # ------------------------------------------------------------------

    def _abuse_signals(self, text: str) -> list[Signal]:
        signals: list[Signal] = []

        normalised = normalise(text)
        token_set = set(words(text))

        # Whole-word matching against the normalised text. This is what keeps
        # "assignment" and "Scunthorpe" out of the results -- a substring check
        # flags both, and the resulting bug report is embarrassing.
        profanity_hits = sorted(token_set & PROFANITY)
        if profanity_hits:
            # Coarse language on its own is a flag, not a block. A developer
            # platform that refuses "this API is a shitshow" is unusable.
            signals.append(
                Signal(
                    category=Category.PROFANITY,
                    rule="profanity",
                    weight=min(0.3 + 0.15 * (len(profanity_hits) - 1), 0.6),
                    detail=", ".join(profanity_hits),
                )
            )

        slur_hits = sorted(token_set & SLURS)
        if slur_hits:
            signals.append(
                Signal(
                    category=Category.SLUR,
                    rule="slur",
                    weight=1.0,
                    detail=", ".join(slur_hits),
                )
            )

        # Harassment terms are phrases, so they are matched against the
        # normalised string rather than the token set.
        harassment_hits = sorted(p for p in HARASSMENT if p in normalised)
        if harassment_hits:
            signals.append(
                Signal(
                    category=Category.HARASSMENT,
                    rule="harassment",
                    weight=1.0,
                    detail=", ".join(harassment_hits),
                )
            )

        # Evasion. Each pattern tolerates separators and substitutions *inside*
        # the term while still requiring a word boundary around the whole
        # match, which is what catches "f u c k" without catching "Scunthorpe".
        # Only checked when plain matching found nothing, since a plain hit
        # already scored.
        if not profanity_hits and not slur_hits:
            evaded = [
                term
                for term, pattern in _EVASION_PATTERNS
                if pattern.search(normalised)
            ]
            if evaded:
                # Scored a little below a plain hit: deliberate obfuscation is
                # evidence of intent, but the pattern is looser than an exact
                # match and should not block on its own.
                signals.append(
                    Signal(
                        category=Category.PROFANITY,
                        rule="obfuscated_term",
                        weight=0.35,
                        detail=", ".join(evaded[:3]),
                    )
                )

        return signals

    # ------------------------------------------------------------------
    # Spam
    # ------------------------------------------------------------------

    def _spam_signals(self, text: str) -> list[Signal]:
        signals: list[Signal] = []
        normalised = normalise(text)

        urls = URL_PATTERN.findall(text)
        domains = [self._domain(u) for u in urls]
        notable = [d for d in domains if d and d not in ALLOWED_DOMAINS]

        # Link density relative to length. Three links in a paragraph is a
        # well-referenced paragraph; three links in fifteen words is a drop.
        word_count = max(len(normalised.split()), 1)
        if len(notable) >= 2 and word_count < len(notable) * 25:
            signals.append(
                Signal(
                    category=Category.SPAM,
                    rule="link_density",
                    weight=min(0.2 * len(notable), 0.6),
                    detail=f"{len(notable)} links in {word_count} words",
                )
            )

        shorteners = sorted({d for d in domains if d in URL_SHORTENERS})
        if shorteners:
            # A shortener hides its destination, which is the whole reason it
            # gets used here. There is no innocent version of this in a
            # project description.
            signals.append(
                Signal(
                    category=Category.SPAM,
                    rule="url_shortener",
                    weight=0.4 * len(shorteners),
                    detail=", ".join(shorteners),
                )
            )

        phrase_hits = sorted(p for p in SPAM_PHRASES if p in normalised)
        if phrase_hits:
            signals.append(
                Signal(
                    category=Category.SPAM,
                    rule="spam_phrase",
                    weight=min(0.3 * len(phrase_hits), 0.9),
                    detail=", ".join(phrase_hits[:3]),
                )
            )

        signals.extend(self._contact_signals(text, normalised))

        return signals

    def _contact_signals(self, text: str, normalised: str) -> list[Signal]:
        """
        Contact details, weighted by whether they are being *solicited*.

        An email address in a bug report is an email address. "Reach me at"
        followed by an email is somebody routing around the platform, which is
        the shape of both recruitment spam and most scams.
        """
        signals: list[Signal] = []

        solicits = sorted(p for p in CONTACT_SOLICITATION if p in normalised)
        has_email = bool(EMAIL_PATTERN.search(text))
        has_phone = bool(PHONE_PATTERN.search(text))

        if solicits and (has_email or has_phone):
            signals.append(
                Signal(
                    category=Category.CONTACT_HARVESTING,
                    rule="solicited_contact_details",
                    weight=0.5,
                    detail=", ".join(solicits[:3]),
                )
            )
        elif solicits:
            signals.append(
                Signal(
                    category=Category.CONTACT_HARVESTING,
                    rule="offsite_contact_request",
                    weight=0.25,
                    detail=", ".join(solicits[:3]),
                )
            )

        return signals

    # ------------------------------------------------------------------
    # Formatting
    # ------------------------------------------------------------------

    def _formatting_signals(self, text: str) -> list[Signal]:
        """
        Shouting and character mashing.

        Weak signals individually -- somebody is allowed to be excited -- but
        they correlate strongly with everything else on this list, so they earn
        their place as a tiebreaker.
        """
        signals: list[Signal] = []

        if len(text) >= MIN_LENGTH_FOR_RATIOS:
            ratio = shout_ratio(text)
            if ratio > 0.7:
                signals.append(
                    Signal(
                        category=Category.FORMATTING,
                        rule="excessive_caps",
                        weight=0.2,
                        detail=f"{ratio:.0%} uppercase",
                    )
                )

        runs = repeated_character_runs(text)
        if runs >= 3:
            signals.append(
                Signal(
                    category=Category.FORMATTING,
                    rule="character_repetition",
                    weight=0.15,
                    detail=f"{runs} runs",
                )
            )

        tokens = words(text)
        if len(tokens) >= 8:
            distinct_ratio = len(set(tokens)) / len(tokens)
            if distinct_ratio < 0.35:
                signals.append(
                    Signal(
                        category=Category.FORMATTING,
                        rule="word_repetition",
                        weight=0.25,
                        detail=f"{distinct_ratio:.0%} distinct",
                    )
                )

        return signals

    # ------------------------------------------------------------------
    # Context and thresholds
    # ------------------------------------------------------------------

    @staticmethod
    def _author_multiplier(
        author: Optional[AuthorContext],
        signals: list[Signal],
    ) -> float:
        """
        Weight the score by who is writing.

        Applied only when something already fired: a trusted account's clean
        post and a new account's clean post are both zero, and multiplying zero
        is pointless. The account-age effect deliberately does not apply to
        slurs and harassment -- seniority is not a licence.
        """
        if author is None or not signals:
            return 1.0

        severe = {Category.SLUR, Category.HARASSMENT}
        if severe & {s.category for s in signals}:
            return 1.0

        multiplier = 1.0

        if author.account_age_days is not None:
            if author.account_age_days < 1:
                multiplier *= 1.5
            elif author.account_age_days < 7:
                multiplier *= 1.25
            elif author.account_age_days > 365:
                multiplier *= 0.8

        if author.prior_flags >= 3:
            multiplier *= 1.4
        elif author.prior_flags >= 1:
            multiplier *= 1.15

        if author.is_verified:
            multiplier *= 0.7

        return multiplier

    @staticmethod
    def _action_for(score: float, thresholds: dict) -> Action:
        if score >= thresholds[Action.BLOCK]:
            return Action.BLOCK
        if score >= thresholds[Action.REVIEW]:
            return Action.REVIEW
        if score >= thresholds[Action.FLAG]:
            return Action.FLAG
        return Action.ALLOW

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _domain(url: str) -> Optional[str]:
        """The registrable-ish domain of a URL, with any ``www.`` dropped."""
        try:
            host = (urlparse(url).hostname or "").lower()
        except ValueError:
            return None

        if not host:
            return None

        return host[4:] if host.startswith("www.") else host


moderation_service = ModerationService()
