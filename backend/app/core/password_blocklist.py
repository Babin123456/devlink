"""
Local screening for obviously-guessable passwords.

Composition rules (upper + lower + digit + symbol) are a weak signal on their
own: ``Password1!``, ``Welcome123!`` and ``Qwerty123!`` all satisfy them and all
sit near the top of every credential-stuffing wordlist. NIST SP 800-63B
recommends screening candidates against known-bad values instead of leaning on
composition alone.

This module is the offline half of that. The network half -- the Have I Been
Pwned range API -- lives in ``app/services/password_breach_service.py``.
"""

import re
import unicodedata
from typing import Iterable, Optional, Set

# The most frequently observed passwords across public breach corpora, plus the
# ones this project's own domain invites ("devlink", "github", ...). Entries are
# stored already normalised (see ``normalise_password``) so lookup is a single
# set membership test.
#
# Deliberately kept small and in-repo rather than shipping a multi-megabyte
# wordlist: HIBP covers the long tail, and this list only needs to catch the
# passwords people actually reach for first, including when HIBP is unreachable.
_RAW_COMMON_PASSWORDS: tuple[str, ...] = (
    # Classic top-25
    "123456",
    "password",
    "123456789",
    "12345678",
    "12345",
    "1234567",
    "1234567890",
    "qwerty",
    "abc123",
    "111111",
    "123123",
    "admin",
    "letmein",
    "welcome",
    "monkey",
    "login",
    "princess",
    "dragon",
    "sunshine",
    "master",
    "football",
    "baseball",
    "superman",
    "iloveyou",
    "trustno1",
    # Keyboard walks
    "qwertyuiop",
    "asdfghjkl",
    "zxcvbnm",
    "qazwsx",
    "1qaz2wsx",
    "qwerty123",
    "1q2w3e4r",
    "1q2w3e4r5t",
    "poiuytrewq",
    # Composition-rule survivors: these pass every strength check we had
    "password1",
    "password123",
    "passw0rd",
    "p@ssword",
    "p@ssw0rd",
    "welcome1",
    "welcome123",
    "admin123",
    "administrator",
    "letmein123",
    "changeme",
    "changeme123",
    "secret",
    "secret123",
    "temporary",
    "temppassword",
    "newpassword",
    "myp@ssword",
    "abcd1234",
    "test1234",
    "root1234",
    "pass1234",
    # Product- and domain-flavoured guesses
    "devlink",
    "devlink123",
    "developer",
    "developer123",
    "github",
    "github123",
    "opensource",
    "hacktoberfest",
    "localhost",
    "django",
    "fastapi",
    # Dates and sequences people pick when forced to add digits
    "january1",
    "summer2024",
    "summer2025",
    "winter2024",
    "winter2025",
    "spring2025",
    "autumn2025",
)

# Character swaps people use to satisfy a symbol requirement without actually
# picking a different word. Folding them lets "P@ssw0rd!" collapse onto
# "password".
_LEET_SUBSTITUTIONS = str.maketrans(
    {
        "@": "a",
        "4": "a",
        "8": "b",
        "(": "c",
        "3": "e",
        "6": "g",
        "1": "i",
        "!": "i",
        "|": "i",
        "0": "o",
        "$": "s",
        "5": "s",
        "7": "t",
        "+": "t",
        "2": "z",
    }
)

# Trailing decoration that adds no entropy: "password" -> "password2024!!"
_TRAILING_NOISE = re.compile(r"[\d\W_]+$")

_NON_ALNUM = re.compile(r"[^a-z0-9]")

# Below this length a substring match against the username is meaningless --
# almost every password contains some two-letter run from some identifier.
MIN_CONTEXT_TOKEN_LENGTH = 4


def normalise_password(password: str) -> str:
    """
    Fold a password down to its recognisable core.

    Lowercases, applies Unicode NFKD folding, strips trailing digits and
    punctuation, then undoes common leetspeak. ``P@ssw0rd2024!`` and
    ``password`` both come out as ``password``.

    Order matters: the trailing noise has to go first. Leetspeak folding maps
    digits onto letters, so running it first would turn the ``2025`` in
    ``Password2025!`` into letters and leave nothing for the trailing-noise
    pattern to strip.
    """
    folded = unicodedata.normalize("NFKD", password).lower()
    folded = _TRAILING_NOISE.sub("", folded)
    folded = folded.translate(_LEET_SUBSTITUTIONS)
    return folded


def _build_blocklist() -> Set[str]:
    """Normalise the raw list once at import time."""
    entries: Set[str] = set()
    for raw in _RAW_COMMON_PASSWORDS:
        entries.add(raw.lower())
        entries.add(normalise_password(raw))
    # Normalisation can strip an entry down to nothing (a purely numeric
    # password like "123456"); keeping "" would reject every password whose
    # core folds away.
    entries.discard("")
    return entries


COMMON_PASSWORDS: Set[str] = _build_blocklist()


def is_common_password(password: str) -> bool:
    """
    Whether a password is on the local blocklist.

    Both the literal lowercase form and the normalised form are checked, so
    ``PASSWORD``, ``password``, ``P@ssw0rd`` and ``Password2025!`` are all
    caught by the single ``password`` entry.
    """
    if not password:
        return False

    if password.lower() in COMMON_PASSWORDS:
        return True

    return normalise_password(password) in COMMON_PASSWORDS


def _context_tokens(values: Iterable[Optional[str]]) -> Set[str]:
    """
    Break identifying values into comparable tokens.

    An email contributes its local-part, and any value is additionally split on
    non-alphanumeric boundaries so ``alex.rivera`` yields ``alex`` and
    ``rivera`` as well as ``alexrivera``.
    """
    tokens: Set[str] = set()

    for value in values:
        if not value:
            continue

        candidate = value.strip().lower()
        if "@" in candidate:
            candidate = candidate.split("@", 1)[0]

        for part in re.split(r"[^a-z0-9]+", candidate):
            if len(part) >= MIN_CONTEXT_TOKEN_LENGTH:
                tokens.add(part)

        collapsed = _NON_ALNUM.sub("", candidate)
        if len(collapsed) >= MIN_CONTEXT_TOKEN_LENGTH:
            tokens.add(collapsed)

    return tokens


def contains_personal_information(
    password: str,
    username: Optional[str] = None,
    email: Optional[str] = None,
) -> bool:
    """
    Whether the password is built out of the user's own identifiers.

    ``alexrivera`` / ``alex@devlink.app`` picking ``Alex.Rivera2025!`` is a
    password an attacker guesses on the first page of a targeted list, so it is
    rejected even though it satisfies every composition rule.
    """
    if not password:
        return False

    haystack = _NON_ALNUM.sub("", normalise_password(password))
    if not haystack:
        return False

    return any(token in haystack for token in _context_tokens([username, email]))
