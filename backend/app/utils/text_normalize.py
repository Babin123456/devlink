"""
Folding text down to something a term list can actually match.

A moderation check written as ``term in text.lower()`` is defeated by every
evasion anybody has ever tried, and they are all trivial:

    f u c k        spacing
    f.u.c.k        separators
    fvck / f4ck    letter substitution
    fυck           a Greek upsilon that renders as a "u"
    𝐟𝐮𝐜𝐤          mathematical bold, a different codepoint per letter
    fuuuuuck       repetition

Each is a different mechanism, so they are undone in a specific order:
decompose the Unicode first (which handles the mathematical and fullwidth
alphabets), then fold the script homoglyphs (Greek and Cyrillic lookalikes),
then collapse repeats, then handle separators.

The one thing this module is careful *not* to do is fold everything into one
undifferentiated blob and substring-match against it. With separators gone,
"class" contains a slur and "Scunthorpe" contains a swear word -- the famous
Scunthorpe problem, which every filter that ships without a test for it
eventually ships as a bug. Evasion is instead detected with a per-term pattern
that tolerates separators and substitutions *inside* the term while still
requiring a word boundary around the whole match.
"""

from __future__ import annotations

import re
import unicodedata

# Letters from other scripts that render close enough to a Latin letter to be
# used as a substitute. Not the full Unicode confusables table -- that has
# thousands of entries, and almost none of them show up in real abuse.
#
# These fold during ordinary normalisation because they are unambiguously
# letters: nobody writes a Cyrillic "о" in an English sentence by accident.
SCRIPT_HOMOGLYPHS = {
    # Cyrillic
    "а": "a",
    "в": "b",
    "с": "c",
    "е": "e",
    "н": "h",
    "к": "k",
    "м": "m",
    "о": "o",
    "р": "p",
    "ѕ": "s",
    "т": "t",
    "у": "y",
    "х": "x",
    "і": "i",
    "ј": "j",
    # Greek
    "α": "a",
    "β": "b",
    "ε": "e",
    "η": "n",
    "ι": "i",
    "κ": "k",
    "ν": "v",
    "ο": "o",
    "ρ": "p",
    "τ": "t",
    "υ": "u",
    "χ": "x",
    "γ": "y",
    "ζ": "z",
}

# Symbols used *as* letters. These deliberately do not fold during ordinary
# normalisation: "!" is punctuation far more often than it is an "i", and
# folding it there destroys the word boundaries every whole-word check depends
# on. They are only consulted when building an evasion pattern.
SYMBOL_HOMOGLYPHS = {
    "@": "a",
    "!": "i",
    "|": "l",
    "$": "s",
    "€": "e",
    "£": "l",
    "(": "c",
}

# Digit-for-letter substitutions. Same reasoning: "123" is a number, not
# "ize", so these are not applied to ordinary text either.
LEET = {
    "0": "o",
    "1": "i",
    "3": "e",
    "4": "a",
    "5": "s",
    "6": "g",
    "7": "t",
    "8": "b",
    "9": "g",
}

# Latin letters standing in for other Latin letters. Only ever used inside an
# evasion pattern -- "v" for "u" is a real evasion but a catastrophic global
# substitution.
LETTER_SUBSTITUTIONS = {
    "u": "v",
    "i": "lj",
    "s": "z",
    "k": "q",
}

# What may appear *between* the letters of an evaded term. Kept short and
# capped in the pattern, because allowing unbounded separators would let a
# term match across half a sentence.
_TERM_SEPARATORS = r"[\s._\-*+|/\\'\"~,]{0,2}"

_SEPARATORS = re.compile(r"[\s\-_.,;:!?'\"/\\|+*()\[\]{}<>~`^&#%​-‏⁠]+")

_NON_ALNUM = re.compile(r"[^a-z0-9]+")

_REPEATS = re.compile(r"(.)\1{2,}")

_WORD = re.compile(r"[a-z0-9]+")


def strip_accents(text: str) -> str:
    """
    Remove combining marks, so ``café`` and ``cafe`` compare equal.

    NFKD splits a precomposed character into its base plus its marks; dropping
    the marks leaves the base. The K in NFKD is what also turns fullwidth and
    mathematical alphabets into plain ASCII, which is the main reason this runs
    first.
    """
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(c for c in decomposed if not unicodedata.combining(c))


def fold_homoglyphs(text: str) -> str:
    """Replace lookalike *letters* from other scripts with their Latin twin."""
    return "".join(SCRIPT_HOMOGLYPHS.get(c, c) for c in text)


def fold_symbols(text: str) -> str:
    """Replace symbols being used as letters. Not safe for general text."""
    return "".join(SYMBOL_HOMOGLYPHS.get(c, c) for c in text)


def fold_leet(text: str) -> str:
    """Replace digits standing in for letters. Not safe for general text."""
    return "".join(LEET.get(c, c) for c in text)


def collapse_repeats(text: str, *, keep: int = 2) -> str:
    """
    Squash runs of the same character down to ``keep``.

    Two rather than one, because English is full of genuine doubles and
    collapsing all the way to one turns "boot" into "bot" and starts matching
    things it should not.
    """
    return _REPEATS.sub(lambda m: m.group(1) * keep, text)


def normalise(text: str) -> str:
    """
    The safe fold, for whole-word matching.

    Accents, script homoglyphs and repeated characters are dealt with;
    separators become single spaces so word boundaries survive. Digits and
    symbols are left alone, because "123" is a number and "!" is punctuation.
    """
    text = strip_accents(text).lower()
    text = fold_homoglyphs(text)
    text = _SEPARATORS.sub(" ", text)
    text = collapse_repeats(text)
    return " ".join(text.split())


def squash(text: str) -> str:
    """
    The aggressive fold, with every separator and substitution undone.

    Useful for comparing two strings that should be "the same word", and
    **not** safe for substring-matching a term list against: with the spaces
    gone, "class" contains a slur and "Scunthorpe" contains a swear word. Use
    :func:`contains_evaded` for that instead.
    """
    text = strip_accents(text).lower()
    text = fold_homoglyphs(text)
    text = fold_symbols(text)
    text = fold_leet(text)
    text = _NON_ALNUM.sub("", text)
    return collapse_repeats(text, keep=1)


def words(text: str) -> list[str]:
    """The normalised text split into word tokens."""
    return _WORD.findall(normalise(text))


def contains_word(text: str, term: str) -> bool:
    """
    Whether a normalised term appears as a whole word.

    Whole-word is the difference between flagging "assignment" and not.
    """
    return normalise(term) in set(words(text))


def _character_class(char: str) -> str:
    """Every character that could be standing in for ``char``."""
    alternatives = {char}

    alternatives.update(k for k, v in SCRIPT_HOMOGLYPHS.items() if v == char)
    alternatives.update(k for k, v in SYMBOL_HOMOGLYPHS.items() if v == char)
    alternatives.update(k for k, v in LEET.items() if v == char)
    alternatives.update(LETTER_SUBSTITUTIONS.get(char, ""))

    return "[" + "".join(re.escape(c) for c in sorted(alternatives)) + "]"


def evasion_pattern(term: str) -> re.Pattern:
    """
    A pattern that matches ``term`` however it has been mangled.

    Between every pair of letters it tolerates up to two separators, and each
    letter may be repeated or substituted. Crucially the *whole match* is
    still bounded by non-word characters, which is what keeps "cunt" out of
    "Scunthorpe" while still catching "c u n t".

    Word-internal separators are allowed; word boundaries around the term are
    not negotiable. That asymmetry is the entire design.
    """
    pieces = [f"{_character_class(c)}+" for c in term if not c.isspace()]

    body = _TERM_SEPARATORS.join(pieces)

    # Lookarounds rather than \b: \b is defined against \w, which includes the
    # digits and underscores that evasions are built out of.
    return re.compile(rf"(?<![a-z0-9]){body}(?![a-z0-9])", re.IGNORECASE)


def contains_evaded(text: str, pattern: re.Pattern) -> bool:
    """Whether an evasion pattern matches, after the safe fold."""
    return pattern.search(normalise(text)) is not None


def shout_ratio(text: str) -> float:
    """
    Fraction of the letters that are uppercase.

    Letters only: digits and punctuation have no case, and counting them makes
    a phone number look like shouting.
    """
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return 0.0
    return sum(1 for c in letters if c.isupper()) / len(letters)


def repeated_character_runs(text: str, *, threshold: int = 4) -> int:
    """How many runs of the same character are at least ``threshold`` long."""
    runs = 0
    run_length = 1

    for previous, current in zip(text, text[1:]):
        if current == previous:
            run_length += 1
            if run_length == threshold:
                runs += 1
        else:
            run_length = 1

    return runs
