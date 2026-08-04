"""
Have I Been Pwned breach lookup.

Uses the range API, which is a k-anonymity scheme: we SHA-1 the password and
send only the first five hex characters of the digest. The service answers with
every suffix it holds under that prefix -- several hundred entries -- and the
comparison happens locally. The password, and even its full hash, never leave
this process.

The check is advisory. A network problem must never stop somebody registering,
so every failure path fails open and is logged.
"""

import hashlib
import logging
from typing import Optional

import httpx

from app.core.cache import cache_manager
from app.core.config import settings

logger = logging.getLogger(__name__)

_CACHE_PREFIX = "hibp:range:"


class PasswordBreachService:
    """
    Look up how often a password appears in known breach corpora.

    Stateless apart from the shared cache, so it is cheap to instantiate per
    request; a module-level singleton is provided below for convenience.
    """

    def __init__(
        self,
        api_url: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> None:
        self.api_url = api_url or settings.HIBP_API_URL
        self.timeout = timeout if timeout is not None else settings.HIBP_TIMEOUT_SECONDS

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def breach_count(self, password: str) -> int:
        """
        Number of times the password appears in the breach corpus.

        Returns ``0`` both when the password is genuinely absent and when the
        lookup could not be completed -- callers must not treat ``0`` as proof
        of safety, only as "no reason to reject".
        """
        if not settings.ENABLE_HIBP_CHECK or not password:
            return 0

        prefix, suffix = self._hash_parts(password)

        body = self._fetch_range(prefix)
        if body is None:
            return 0

        return self._count_from_range(body, suffix)

    def is_compromised(self, password: str) -> bool:
        """
        Whether the password appears often enough to be worth rejecting.

        ``HIBP_MIN_BREACH_COUNT`` exists because a handful of the corpus
        entries are one-off artefacts rather than passwords in active use on
        credential-stuffing lists.
        """
        return self.breach_count(password) >= settings.HIBP_MIN_BREACH_COUNT

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    @staticmethod
    def _hash_parts(password: str) -> tuple[str, str]:
        """
        Split the SHA-1 of the password into the prefix we send and the suffix
        we match locally.

        SHA-1 is not a security choice here -- it is the digest the range API
        is keyed on. The value being protected is the password, and it is
        protected by only ever transmitting five characters of the digest.
        """
        digest = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
        return digest[:5], digest[5:]

    def _fetch_range(self, prefix: str) -> Optional[str]:
        """
        Fetch (or reuse) the suffix list for a hash prefix.

        Range responses are effectively static, so caching them cuts the
        request count substantially: five hex characters means only 1,048,576
        possible buckets, and real traffic clusters hard.
        """
        cache_key = f"{_CACHE_PREFIX}{prefix}"

        cached = cache_manager.get(cache_key)
        if cached is not None:
            return cached

        try:
            response = httpx.get(
                f"{self.api_url}/{prefix}",
                timeout=self.timeout,
                headers={
                    # Opting in to padded responses means every reply contains
                    # a similar number of entries, so an observer cannot infer
                    # anything from the response size.
                    "Add-Padding": "true",
                    "User-Agent": "DevLink-Password-Screening",
                },
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            # Fail open. An outage at a third party must not become an outage
            # of our signup form.
            logger.warning("HIBP range lookup failed for prefix %s: %s", prefix, exc)
            return None
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning("Unexpected HIBP lookup error: %s", exc)
            return None

        body = response.text
        cache_manager.set(cache_key, body, ttl=settings.HIBP_CACHE_TTL_SECONDS)
        return body

    @staticmethod
    def _count_from_range(body: str, suffix: str) -> int:
        """
        Find our suffix in a range response.

        Each line is ``<SUFFIX>:<COUNT>``. Padded responses include synthetic
        entries with a count of zero, which fall out naturally: either they do
        not match our suffix, or the count they carry is zero anyway.
        """
        target = suffix.upper()

        for line in body.splitlines():
            candidate, _, count = line.partition(":")
            if candidate.strip().upper() != target:
                continue
            try:
                return int(count.strip())
            except ValueError:
                logger.warning("Malformed count in HIBP response: %r", line)
                return 0

        return 0


password_breach_service = PasswordBreachService()
