"""
Feature flag endpoints.

``GET /api/feature-flags`` is the one the frontend cares about: it returns the
whole evaluated flag map for the caller in a single request, so the UI does not
need a round trip per flag.

The override endpoints are administrator-only and exist so a flag can be
flipped during an incident without waiting for a deploy.
"""

from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.core.feature_flags import FLAG_DEFINITIONS, FlagStrategy
from app.dependencies import get_current_admin, get_optional_current_user
from app.models.user import User
from app.services.feature_flag_service import feature_flag_service

router = APIRouter()


# ----------------------------------------------------------------------
# Schemas
# ----------------------------------------------------------------------


class FeatureFlagStateResponse(BaseModel):
    """The evaluated flag map for the calling user."""

    flags: Dict[str, bool]


class FeatureFlagDetail(BaseModel):
    key: str
    description: str
    strategy: str
    percentage: int
    allowlist_size: int
    overridden: bool
    enabled: bool


class FeatureFlagOverrideRequest(BaseModel):
    """
    A runtime override. Omitted fields fall through to the flag's definition,
    so bumping a rollout percentage does not require restating the strategy.
    """

    strategy: Optional[FlagStrategy] = None
    percentage: Optional[int] = Field(default=None, ge=0, le=100)
    allowlist: Optional[List[str]] = None


# ----------------------------------------------------------------------
# Endpoints
# ----------------------------------------------------------------------


@router.get(
    "/feature-flags",
    response_model=FeatureFlagStateResponse,
    tags=["Feature Flags"],
)
def get_feature_flags(
    current_user: User | None = Depends(get_optional_current_user),
):
    """
    Evaluate every flag for the caller.

    Deliberately open to anonymous callers -- the landing page needs to know
    which sections to render before anyone has logged in. Unauthenticated
    callers cannot be bucketed, so they see only flags that are on for
    everyone.
    """
    user_id = str(current_user.id) if current_user else None
    return FeatureFlagStateResponse(flags=feature_flag_service.evaluate_all(user_id))


@router.get(
    "/admin/feature-flags",
    response_model=List[FeatureFlagDetail],
    tags=["Feature Flags"],
)
def list_feature_flags(
    current_admin: User = Depends(get_current_admin),
):
    """Full detail for every flag, including whether it is overridden."""
    return feature_flag_service.describe_all(str(current_admin.id))


@router.put(
    "/admin/feature-flags/{key}",
    response_model=FeatureFlagDetail,
    tags=["Feature Flags"],
)
def override_feature_flag(
    key: str,
    payload: FeatureFlagOverrideRequest,
    current_admin: User = Depends(get_current_admin),
):
    """Apply a runtime override to a flag."""
    if key not in FLAG_DEFINITIONS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unknown feature flag: {key}",
        )

    persisted = feature_flag_service.set_override(
        key,
        strategy=payload.strategy,
        percentage=payload.percentage,
        allowlist=payload.allowlist,
    )

    if not persisted:
        # Without a cache backend the override would vanish immediately.
        # Better to say so than to report a success that does not hold.
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "Feature flag overrides require a cache backend, which is "
                "not currently available."
            ),
        )

    return _detail_for(key, str(current_admin.id))


@router.delete(
    "/admin/feature-flags/{key}",
    response_model=FeatureFlagDetail,
    tags=["Feature Flags"],
)
def clear_feature_flag_override(
    key: str,
    current_admin: User = Depends(get_current_admin),
):
    """Remove an override, reverting the flag to its definition."""
    if key not in FLAG_DEFINITIONS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unknown feature flag: {key}",
        )

    feature_flag_service.clear_override(key)
    return _detail_for(key, str(current_admin.id))


def _detail_for(key: str, user_id: str) -> dict:
    """Re-read a single flag's detail after mutating it."""
    for detail in feature_flag_service.describe_all(user_id):
        if detail["key"] == key:
            return detail

    # describe_all covers every registered key and the caller already checked
    # membership, so this is unreachable.
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Unknown feature flag: {key}",
    )
