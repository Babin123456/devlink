"""
Feature flag definitions and evaluation.

The config already carries a handful of static ``ENABLE_*`` booleans. Those are
build-time switches: changing one means editing the environment and restarting.
This module adds the runtime layer on top -- flags that can be flipped without a
deploy, targeted at a subset of users, and rolled out gradually.

Evaluation is pure: given a definition, an optional override and a user id, the
result is deterministic and needs no I/O. The service in
``app/services/feature_flag_service.py`` supplies the overrides.

This is first-party toggling, distinct from the third-party extensibility
discussed in #582.
"""

import hashlib
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class FlagStrategy(str, Enum):
    """How a flag decides whether it is on for a given user."""

    #: On for everyone.
    ON = "on"

    #: Off for everyone. The kill switch.
    OFF = "off"

    #: On for a stable percentage of users, keyed on user id.
    PERCENTAGE = "percentage"

    #: On only for an explicit list of user ids.
    ALLOWLIST = "allowlist"


@dataclass(frozen=True)
class FlagDefinition:
    """
    A single feature flag.

    ``description`` is surfaced in the API response so an operator flipping a
    flag can see what it does without reading the source.
    """

    key: str
    description: str
    strategy: FlagStrategy = FlagStrategy.OFF
    percentage: int = 0
    allowlist: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not 0 <= self.percentage <= 100:
            raise ValueError(
                f"Flag '{self.key}' has percentage {self.percentage}; "
                "must be between 0 and 100."
            )


# The flag registry. Adding a flag here is all that is needed for it to appear
# in the API and be usable with require_flag().
#
# Everything incomplete is defined OFF, so merging work behind a flag is safe by
# default: a flag someone forgot to configure stays dark.
FLAG_DEFINITIONS: Dict[str, FlagDefinition] = {
    definition.key: definition
    for definition in (
        FlagDefinition(
            key="graph_view",
            description="Interactive collaboration graph on /graph.",
            strategy=FlagStrategy.OFF,
        ),
        FlagDefinition(
            key="hackathons",
            description="Hackathon listings, teams, and submissions.",
            strategy=FlagStrategy.OFF,
        ),
        FlagDefinition(
            key="ai_recommendation_panel",
            description="AI-generated project and teammate suggestions.",
            strategy=FlagStrategy.PERCENTAGE,
            percentage=0,
        ),
        FlagDefinition(
            key="design_system_route",
            description="Internal component gallery at /design-system.",
            strategy=FlagStrategy.ALLOWLIST,
        ),
        FlagDefinition(
            key="duplicate_project_detection",
            description="Warn on likely-duplicate projects at creation time.",
            strategy=FlagStrategy.OFF,
        ),
    )
}


@dataclass(frozen=True)
class FlagOverride:
    """
    A runtime override for a flag, normally loaded from Redis.

    Fields left as ``None`` fall through to the definition, so an operator can
    bump a rollout percentage without restating the strategy.
    """

    strategy: Optional[FlagStrategy] = None
    percentage: Optional[int] = None
    allowlist: Optional[List[str]] = None

    def apply_to(self, definition: FlagDefinition) -> FlagDefinition:
        """Produce the effective definition for this evaluation."""
        return FlagDefinition(
            key=definition.key,
            description=definition.description,
            strategy=self.strategy or definition.strategy,
            percentage=(
                self.percentage
                if self.percentage is not None
                else definition.percentage
            ),
            allowlist=(
                self.allowlist if self.allowlist is not None else definition.allowlist
            ),
        )


def bucket_for(flag_key: str, user_id: str) -> int:
    """
    Map a user onto a stable bucket in ``[0, 100)`` for one flag.

    The hash includes the flag key so a user who lands in bucket 3 for one flag
    is not automatically in bucket 3 for every other flag -- otherwise the same
    unlucky cohort would receive every single rollout.

    Deterministic across processes and restarts, which is the whole point: a
    user must not see a feature flicker on and off between requests. That rules
    out Python's built-in ``hash()``, which is salted per process.
    """
    digest = hashlib.sha256(f"{flag_key}:{user_id}".encode("utf-8")).digest()
    return int.from_bytes(digest[:4], "big") % 100


def evaluate(
    definition: FlagDefinition,
    user_id: Optional[str] = None,
    override: Optional[FlagOverride] = None,
) -> bool:
    """
    Decide whether a flag is on.

    Anonymous callers (``user_id is None``) cannot be bucketed or matched
    against an allowlist, so they resolve to the flag's unconditional state:
    on only for ``ON``.
    """
    effective = override.apply_to(definition) if override else definition

    if effective.strategy is FlagStrategy.ON:
        return True

    if effective.strategy is FlagStrategy.OFF:
        return False

    if user_id is None:
        return False

    if effective.strategy is FlagStrategy.ALLOWLIST:
        return user_id in effective.allowlist

    if effective.strategy is FlagStrategy.PERCENTAGE:
        # An allowlisted user is always in, whatever the percentage. This lets
        # the team dogfood a feature that is still at 0%.
        if user_id in effective.allowlist:
            return True
        if effective.percentage <= 0:
            return False
        if effective.percentage >= 100:
            return True
        return bucket_for(effective.key, user_id) < effective.percentage

    # Unreachable while FlagStrategy is exhaustive, but a new strategy that
    # forgets a branch here should fail closed rather than silently enable.
    return False
