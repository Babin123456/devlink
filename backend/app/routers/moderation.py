"""
Moderation preview endpoint.

The service is meant to be called inline from write paths -- message send,
project create, profile update -- rather than over HTTP. This endpoint exists
so that:

* the frontend can warn somebody *before* they hit send, which is a far better
  experience than a rejection afterwards, and
* moderators can check why a particular piece of text scored the way it did
  without reading the source.

It scores text and returns nothing about anybody else, so it is safe for any
authenticated user to call about their own draft.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request

from app.dependencies import get_current_user
from app.middleware.rate_limit import limiter
from app.models.user import User
from app.schemas.moderation import (
    ModerationCheckRequest,
    ModerationCheckResponse,
    ModerationSignalResponse,
)
from app.services.moderation_service import AuthorContext, moderation_service

router = APIRouter(
    prefix="/moderation",
    tags=["Moderation"],
)

MODERATION_LIMIT = "60/minute"


@router.post(
    "/check",
    response_model=ModerationCheckResponse,
    summary="Score a piece of text for abuse and spam",
)
@limiter.limit(MODERATION_LIMIT)
def check_text(
    request: Request,
    body: ModerationCheckRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Score text and recommend an action.

    Returns a recommendation, not a decision: the caller chooses what to do
    with it, because a profile bio and a direct message do not warrant the same
    threshold.
    """
    result = moderation_service.check(
        body.text,
        author=AuthorContext(
            account_age_days=body.account_age_days,
            prior_flags=body.prior_flags,
            is_verified=body.is_verified,
        ),
    )

    return ModerationCheckResponse(
        action=result.action.value,
        score=result.score,
        signals=[
            ModerationSignalResponse(
                category=s.category.value,
                rule=s.rule,
                weight=s.weight,
                detail=s.detail,
            )
            for s in result.signals
        ],
        explanation=result.explain(),
    )
