"""
Tests for text normalisation and moderation scoring.

Two halves, and the second is the one that matters most. Catching evasion is
easy; the hard part is not catching everything else, and the classic failures
here are famous enough to have names. "Scunthorpe" is the canonical one, and
every filter that ships without a test for it eventually ships the bug.
"""

import pytest

from app.services.moderation_service import (
    Action,
    AuthorContext,
    Category,
    ModerationService,
)
from app.utils.text_normalize import (
    collapse_repeats,
    contains_word,
    fold_homoglyphs,
    fold_leet,
    normalise,
    repeated_character_runs,
    shout_ratio,
    squash,
    strip_accents,
    words,
)


@pytest.fixture
def service():
    return ModerationService()


# ======================================================================
# Normalisation
# ======================================================================


def test_strips_accents():
    assert strip_accents("café") == "cafe"


def test_normalises_fullwidth_and_mathematical_alphabets():
    # NFKD is what turns 𝐟𝐮𝐜𝐤 and ｆｕｃｋ into plain ASCII. Without it, every
    # one of these is a distinct codepoint the term list has never seen.
    assert strip_accents("𝐡𝐞𝐥𝐥𝐨") == "hello"
    assert strip_accents("ｈｅｌｌｏ") == "hello"


def test_folds_cyrillic_lookalikes():
    # A Cyrillic "о" renders identically to a Latin "o" and compares unequal.
    assert fold_homoglyphs("hеllо") == "hello"


def test_folds_greek_lookalikes():
    assert fold_homoglyphs("fυck") == "fuck"


def test_folds_leetspeak():
    assert fold_leet("h3ll0") == "hello"


def test_collapses_repeats_to_two():
    # Two rather than one, because English is full of genuine doubles and
    # collapsing to one turns "boot" into "bot".
    assert collapse_repeats("sooooo goooood") == "soo good"
    assert collapse_repeats("boot") == "boot"


def test_normalise_turns_separators_into_spaces():
    # Word boundaries have to survive, or every whole-word check becomes a
    # substring check.
    assert normalise("hello-world") == "hello world"
    assert normalise("hello...world") == "hello world"


def test_squash_removes_everything():
    assert squash("f u c k") == "fuck"
    assert squash("f-u-c-k") == "fuck"
    assert squash("f.u.c.k") == "fuck"


def test_words_tokenises_the_normalised_text():
    assert words("Hello, World! 123") == ["hello", "world", "123"]


def test_contains_word_matches_whole_words_only():
    assert contains_word("that damn bug", "damn") is True
    # "damned" is not "damn", and a substring check would say otherwise.
    assert contains_word("the damned thing", "damn") is False


def test_shout_ratio_ignores_non_letters():
    assert shout_ratio("ABC") == 1.0
    assert shout_ratio("abc") == 0.0
    # Digits and punctuation have no case; counting them makes a phone number
    # look like shouting.
    assert shout_ratio("123!!!") == 0.0


def test_repeated_character_runs_counts_long_runs():
    assert repeated_character_runs("aaaa bbbb") == 2
    assert repeated_character_runs("normal text") == 0


# ======================================================================
# Not catching the wrong things
# ======================================================================


def test_scunthorpe_is_fine(service):
    # The canonical false positive. A substring check flags this and the
    # resulting bug report is embarrassing.
    result = service.check("I grew up in Scunthorpe and moved to Penistone.")

    assert result.action == Action.ALLOW
    assert result.score == 0.0


@pytest.mark.parametrize(
    "text",
    [
        "I finished the assignment last night.",
        "The class implements a shared interface.",
        "Run the analysis and share the output.",
        "This document covers the specification.",
        "Let's discuss the constitution of the team.",
    ],
)
def test_ordinary_words_containing_substrings_are_fine(service, text):
    assert service.check(text).action == Action.ALLOW


def test_a_technical_post_with_several_links_is_fine(service):
    # A well-referenced answer should never look like a link drop.
    result = service.check(
        "Here's the fix. The upstream issue is at https://github.com/foo/bar/issues/12 "
        "and the relevant docs are https://docs.python.org/3/library/asyncio.html "
        "plus the discussion at https://stackoverflow.com/questions/12345 which "
        "explains the reasoning behind the change in some detail."
    )

    assert result.action == Action.ALLOW


def test_a_normal_message_scores_zero(service):
    result = service.check(
        "Hey, I pushed the branch with the auth fix. Could you take a look when "
        "you get a chance? No rush."
    )

    assert result.score == 0.0
    assert result.signals == []


def test_empty_and_whitespace_text_is_allowed(service):
    assert service.check("").action == Action.ALLOW
    assert service.check("    \n  ").action == Action.ALLOW


def test_an_email_on_its_own_is_not_harvesting(service):
    # An email address in a bug report is an email address.
    result = service.check(
        "The webhook fires with the wrong address; it sends to old@example.com "
        "instead of the configured one."
    )

    assert Category.CONTACT_HARVESTING not in result.categories


# ======================================================================
# Catching the right things
# ======================================================================


def test_profanity_is_flagged_not_blocked(service):
    # A developer platform that refuses "this API is a shitshow" is a platform
    # nobody uses. Coarse language is a flag.
    result = service.check("this fucking API is a mess")

    assert Category.PROFANITY in result.categories
    assert result.action in (Action.FLAG, Action.REVIEW)
    assert result.action != Action.BLOCK


def test_a_slur_is_blocked(service):
    result = service.check("you absolute retard")

    assert Category.SLUR in result.categories
    assert result.action == Action.BLOCK


def test_harassment_is_blocked(service):
    result = service.check("nobody likes you, just go die")

    assert Category.HARASSMENT in result.categories
    assert result.action == Action.BLOCK


@pytest.mark.parametrize(
    "evasion",
    ["f u c k", "f-u-c-k", "f.u.c.k", "fvck you"],
)
def test_spaced_and_punctuated_evasion_is_caught(service, evasion):
    result = service.check(evasion)

    assert result.signals != []


@pytest.mark.parametrize("evasion", ["that is sh1t", "you b1tch", "a$$hole"])
def test_leetspeak_and_symbol_evasion_is_caught(service, evasion):
    # Substitutions come from a table, so an unusual one ("f4ck", where a 4
    # stands for a u rather than the a it normally spells) is missed. That is
    # an accepted limit of a deterministic layer, not an oversight -- the
    # answer is to add the mapping, not to loosen the pattern.
    assert service.check(evasion).signals != []


def test_homoglyph_evasion_is_caught(service):
    # Greek upsilon in place of "u".
    assert service.check("what the fυck").signals != []


def test_repetition_evasion_is_caught(service):
    assert service.check("fuuuuuck this").signals != []


# ======================================================================
# Spam
# ======================================================================


def test_a_url_shortener_is_a_strong_signal(service):
    # A shortener hides its destination, which is the whole reason it is here.
    result = service.check("Amazing opportunity, check https://bit.ly/abc123")

    assert Category.SPAM in result.categories
    assert result.score >= 0.4


def test_spam_phrases_score(service):
    result = service.check(
        "Make money online with guaranteed returns! Limited time offer."
    )

    assert Category.SPAM in result.categories
    assert result.action in (Action.REVIEW, Action.BLOCK)


def test_link_density_is_relative_to_length(service):
    result = service.check(
        "check https://a.example.com https://b.example.com https://c.example.com"
    )

    assert Category.SPAM in result.categories


def test_allowed_domains_do_not_count_toward_density(service):
    result = service.check(
        "https://github.com/a https://github.com/b https://gitlab.com/c"
    )

    assert "link_density" not in {s.rule for s in result.signals}


def test_solicited_contact_details_score_higher_than_a_bare_request(service):
    solicited = service.check("DM me for details, telegram me at +1 555 123 4567")
    bare = service.check("dm me if you want to pair on this")

    assert solicited.score > bare.score


# ======================================================================
# Formatting
# ======================================================================


def test_shouting_is_a_weak_signal(service):
    result = service.check("PLEASE LOOK AT THIS RIGHT NOW IT IS URGENT")

    assert "excessive_caps" in {s.rule for s in result.signals}
    # Weak on its own -- somebody is allowed to be excited.
    assert result.action in (Action.ALLOW, Action.FLAG)


def test_a_short_shout_is_not_flagged(service):
    # "OK!" is 100% uppercase and is not shouting. Ratios need length.
    assert service.check("OK!").signals == []


def test_word_repetition_is_detected(service):
    result = service.check("buy buy buy buy buy buy buy buy buy now")

    assert "word_repetition" in {s.rule for s in result.signals}


# ======================================================================
# Author context
# ======================================================================


def test_a_brand_new_account_scores_higher(service):
    text = "Make money online, limited time offer"

    new = service.check(text, author=AuthorContext(account_age_days=0))
    old = service.check(text, author=AuthorContext(account_age_days=800))

    assert new.score > old.score


def test_prior_flags_increase_the_score(service):
    text = "Make money online, limited time offer"

    repeat = service.check(text, author=AuthorContext(prior_flags=5))
    first = service.check(text, author=AuthorContext(prior_flags=0))

    assert repeat.score > first.score


def test_verification_lowers_the_score(service):
    text = "Make money online, limited time offer"

    verified = service.check(text, author=AuthorContext(is_verified=True))
    plain = service.check(text, author=AuthorContext())

    assert verified.score < plain.score


def test_seniority_is_not_a_licence_for_slurs(service):
    # The account-age discount deliberately does not apply to slurs and
    # harassment. A two-year-old account does not get to say this.
    trusted = AuthorContext(account_age_days=2000, is_verified=True)

    assert service.check("you retard", author=trusted).action == Action.BLOCK


def test_context_does_not_manufacture_a_score(service):
    # Multiplying zero is pointless, and a new account posting something clean
    # must still score zero.
    result = service.check(
        "Hello, nice work on this.", author=AuthorContext(account_age_days=0)
    )

    assert result.score == 0.0
    assert result.action == Action.ALLOW


# ======================================================================
# Explainability
# ======================================================================


def test_every_result_lists_the_rules_that_fired(service):
    result = service.check("Make money online at https://bit.ly/x")

    assert result.signals
    for signal in result.signals:
        assert signal.rule
        assert signal.weight > 0
        assert isinstance(signal.category, Category)


def test_explain_names_the_action_the_score_and_the_rules(service):
    explanation = service.check("Make money online at https://bit.ly/x").explain()

    assert "url_shortener" in explanation
    assert "@" in explanation


def test_explain_is_readable_when_nothing_fired(service):
    assert service.check("hello").explain() == "No moderation signals."


def test_thresholds_can_be_overridden(service):
    text = "this fucking API is a mess"

    strict = service.check(
        text,
        thresholds={Action.BLOCK: 0.1, Action.REVIEW: 0.05, Action.FLAG: 0.01},
    )
    lenient = service.check(
        text,
        thresholds={Action.BLOCK: 5.0, Action.REVIEW: 4.0, Action.FLAG: 3.0},
    )

    # Same text, same score, different call-site policy -- which is the point.
    assert strict.action == Action.BLOCK
    assert lenient.action == Action.ALLOW
    assert strict.score == lenient.score


def test_needs_human_covers_review_and_block(service):
    assert service.check("you retard").needs_human is True
    assert service.check("hello there").needs_human is False
