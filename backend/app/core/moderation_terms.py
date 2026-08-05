"""
The word lists and patterns the moderation service scores against.

Kept apart from the scoring logic on purpose: a maintainer adding a term that
keeps showing up should not have to read, or risk breaking, the scoring code.
Everything here is data.

Terms are written in ordinary spelling. The service normalises both the term
and the text before comparing, so there is no need to enumerate ``f4ck``,
``fυck`` and ``f.u.c.k`` -- see ``app/utils/text_normalize.py``.
"""

from __future__ import annotations

import re

# ----------------------------------------------------------------------
# Profanity
# ----------------------------------------------------------------------

# Coarse language. On its own this is a *flag*, not a block: plenty of
# perfectly good technical discussion is sweary, and a platform for developers
# that blocks "this API is a shitshow" is a platform nobody uses.
PROFANITY = frozenset(
    {
        "arse",
        "arsehole",
        "asshole",
        "bastard",
        "bitch",
        "bollocks",
        "bullshit",
        "cock",
        "crap",
        "cunt",
        "damn",
        "dick",
        "dickhead",
        "douchebag",
        "fuck",
        "fucker",
        "fucking",
        "motherfucker",
        "piss",
        "prick",
        "shit",
        "shite",
        "shithead",
        "slut",
        "twat",
        "wanker",
        "whore",
    }
)

# Language aimed at a person rather than a situation. Weighted much harder
# than profanity, because "this is shit" and "you are worthless" are not the
# same act even though both contain a word from a list.
HARASSMENT = frozenset(
    {
        "kill yourself",
        "kys",
        "go die",
        "hope you die",
        "nobody likes you",
        "you are worthless",
        "youre worthless",
        "you should die",
        "end yourself",
        "neck yourself",
    }
)

# Slurs are held separately and scored at the maximum. This list is
# deliberately short and non-exhaustive in the repository; deployments are
# expected to extend it, and the scoring code does not need to change when
# they do.
SLURS = frozenset(
    {
        "retard",
        "retarded",
        "tranny",
        "faggot",
        "fag",
    }
)

# ----------------------------------------------------------------------
# Spam
# ----------------------------------------------------------------------

# Phrasings that essentially never appear in a genuine project description or
# a message between collaborators.
SPAM_PHRASES = frozenset(
    {
        "act now",
        "buy followers",
        "cheap followers",
        "click here now",
        "crypto giveaway",
        "double your money",
        "dm me for",
        "earn money fast",
        "financial freedom",
        "forex signals",
        "free bitcoin",
        "free gift card",
        "guaranteed returns",
        "investment opportunity",
        "limited time offer",
        "make money online",
        "no experience needed",
        "risk free",
        "telegram me",
        "text me on whatsapp",
        "work from home",
        "100% free",
    }
)

# Shorteners hide their destination, which is the entire reason they get used
# in spam. There is no legitimate reason for one in a project description.
URL_SHORTENERS = frozenset(
    {
        "bit.ly",
        "buff.ly",
        "cutt.ly",
        "goo.gl",
        "is.gd",
        "ow.ly",
        "rb.gy",
        "rebrand.ly",
        "shorturl.at",
        "t.co",
        "tinyurl.com",
        "t.me",
        "tiny.cc",
    }
)

# Domains that are ordinary in this context and should never count toward a
# link-density score. A project description with five GitHub links is a
# thorough project description.
ALLOWED_DOMAINS = frozenset(
    {
        "github.com",
        "gitlab.com",
        "bitbucket.org",
        "npmjs.com",
        "pypi.org",
        "crates.io",
        "stackoverflow.com",
        "developer.mozilla.org",
        "docs.python.org",
        "readthedocs.io",
        "figma.com",
        "notion.so",
        "linkedin.com",
        "devlink.dev",
    }
)

# ----------------------------------------------------------------------
# Patterns
# ----------------------------------------------------------------------

URL_PATTERN = re.compile(r"https?://[^\s<>\"')]+", re.IGNORECASE)

EMAIL_PATTERN = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")

# Deliberately loose. Precision does not matter here: this is one weighted
# signal among several, and the cost of matching a version string once in a
# while is a slightly higher score, not a block.
PHONE_PATTERN = re.compile(r"(?:\+?\d[\d\s().-]{7,}\d)")

# Words that are only interesting next to a contact detail. "Reach me at" plus
# an email is somebody routing around the platform; an email on its own in a
# bug report is just an email.
CONTACT_SOLICITATION = frozenset(
    {
        "whatsapp",
        "telegram",
        "signal",
        "wechat",
        "skype",
        "dm me",
        "message me",
        "contact me at",
        "reach me at",
        "email me at",
    }
)
