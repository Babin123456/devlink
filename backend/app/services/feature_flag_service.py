"""
Feature flag service.

Joins the static definitions in ``app/core/feature_flags.py`` with any runtime
overrides stored in Redis, so an operator can flip a flag or bump a rollout
percentage without a deploy.

Redis is optional. With no cache available the service falls back to the
definitions, which means local development and CI need no extra infrastructure.
"""

import json
import logging
from typing import Dict, List, Optional

from app.core.cache import cache_manager
from app.core.feature_flags import (
    FLAG_DEFINITIONS,
    FlagDefinition,
    FlagOverride,
    FlagStrategy,
    evaluate,
)

logger = logging.getLogger(__name__)

_OVERRIDE_PREFIX = "feature_flag:override:"

# Overrides are operator actions, not derived data, so they should not silently
# expire and revert. A week is long enough to be effectively permanent for an
# incident kill switch while still cleaning up flags nobody remembers setting.
_OVERRIDE_TTL_SECONDS = 60 * 60 * 24 * 7


class FeatureFlagService:
    """
    Evaluate feature flags for a user.

    Stateless apart from the shared cache; a module-level singleton is provided
    at the bottom of this file.
    """

    # ------------------------------------------------------------------
    # Evaluation
    # ------------------------------------------------------------------

    def is_enabled(self, key: str, user_id: Optional[str] = None) -> bool:
        """
        Whether a flag is on for a user.

        An unknown key returns ``False`` rather than raising. A typo in a flag
        name should leave a feature dark, not take down the endpoint that
        checks it.
        """
        definition = FLAG_DEFINITIONS.get(key)
        if definition is None:
            logger.warning("Checked unknown feature flag %r", key)
            return False

        return evaluate(definition, user_id=user_id, override=self._get_override(key))

    def evaluate_all(self, user_id: Optional[str] = None) -> Dict[str, bool]:
        """
        Evaluate every registered flag for a user.

        Backs the ``GET /api/feature-flags`` endpoint so the frontend can gate
        its UI from a single request instead of one per flag.
        """
        return {
            key: evaluate(definition, user_id=user_id, override=self._get_override(key))
            for key, definition in FLAG_DEFINITIONS.items()
        }

    def describe_all(self, user_id: Optional[str] = None) -> List[dict]:
        """
        Full detail for every flag: state, strategy, and whether it is
        currently overridden. Used by the admin view.
        """
        described = []

        for key, definition in FLAG_DEFINITIONS.items():
            override = self._get_override(key)
            effective = override.apply_to(definition) if override else definition

            described.append(
                {
                    "key": key,
                    "description": definition.description,
                    "strategy": effective.strategy.value,
                    "percentage": effective.percentage,
                    "allowlist_size": len(effective.allowlist),
                    "overridden": override is not None,
                    "enabled": evaluate(definition, user_id=user_id, override=override),
                }
            )

        return described

    # ------------------------------------------------------------------
    # Overrides
    # ------------------------------------------------------------------

    def set_override(
        self,
        key: str,
        strategy: Optional[FlagStrategy] = None,
        percentage: Optional[int] = None,
        allowlist: Optional[List[str]] = None,
    ) -> bool:
        """
        Store a runtime override.

        Returns ``False`` when there is no cache backend to write to, so the
        caller can tell the operator their change did not stick rather than
        reporting a success that evaporates on the next request.
        """
        if key not in FLAG_DEFINITIONS:
            raise KeyError(f"Unknown feature flag: {key}")

        if percentage is not None and not 0 <= percentage <= 100:
            raise ValueError("percentage must be between 0 and 100")

        payload = {
            "strategy": strategy.value if strategy else None,
            "percentage": percentage,
            "allowlist": allowlist,
        }

        try:
            cache_manager.set(
                f"{_OVERRIDE_PREFIX}{key}",
                json.dumps(payload),
                ttl=_OVERRIDE_TTL_SECONDS,
            )
        except Exception as exc:  # pragma: no cover - defensive
            logger.error("Failed to persist override for flag %s: %s", key, exc)
            return False

        logger.info("Feature flag %s overridden: %s", key, payload)
        return True

    def clear_override(self, key: str) -> None:
        """Drop a runtime override, reverting the flag to its definition."""
        if key not in FLAG_DEFINITIONS:
            raise KeyError(f"Unknown feature flag: {key}")

        try:
            cache_manager.delete(f"{_OVERRIDE_PREFIX}{key}")
        except Exception as exc:  # pragma: no cover - defensive
            logger.error("Failed to clear override for flag %s: %s", key, exc)

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _get_override(self, key: str) -> Optional[FlagOverride]:
        """
        Load a stored override, if any.

        A malformed or unreadable entry is discarded rather than raised: a bad
        value in the cache must degrade to "no override", not break every
        request that evaluates the flag.
        """
        try:
            raw = cache_manager.get(f"{_OVERRIDE_PREFIX}{key}")
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning("Feature flag override lookup failed for %s: %s", key, exc)
            return None

        if raw is None:
            return None

        if isinstance(raw, str):
            try:
                raw = json.loads(raw)
            except (TypeError, ValueError):
                logger.warning("Discarding malformed override for flag %s", key)
                return None

        if not isinstance(raw, dict):
            logger.warning("Discarding non-object override for flag %s", key)
            return None

        strategy_value = raw.get("strategy")
        try:
            strategy = FlagStrategy(strategy_value) if strategy_value else None
        except ValueError:
            logger.warning(
                "Discarding override for flag %s: unknown strategy %r",
                key,
                strategy_value,
            )
            return None

        percentage = raw.get("percentage")
        if percentage is not None and not isinstance(percentage, int):
            logger.warning("Discarding override for flag %s: bad percentage", key)
            return None

        allowlist = raw.get("allowlist")
        if allowlist is not None and not isinstance(allowlist, list):
            logger.warning("Discarding override for flag %s: bad allowlist", key)
            return None

        if strategy is None and percentage is None and allowlist is None:
            return None

        return FlagOverride(
            strategy=strategy,
            percentage=percentage,
            allowlist=[str(entry) for entry in allowlist] if allowlist else None,
        )


feature_flag_service = FeatureFlagService()


def get_flag_definition(key: str) -> FlagDefinition:
    """Look up a definition, raising ``KeyError`` for an unknown key."""
    return FLAG_DEFINITIONS[key]
