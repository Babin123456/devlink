"""
Calendar endpoints: single-event downloads and the subscribable feed.

The feed endpoint is the odd one out. It authenticates with a token in the
query string rather than a header, because a calendar client will not send one
-- it does "GET this URL, forever" and nothing more. Everything else here is
ordinary session-authenticated API.
"""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_database
from app.middleware.rate_limit import limiter
from app.models.hackathon import Hackathon
from app.models.milestone import Milestone
from app.models.user import User
from app.schemas.calendar import CalendarFeedTokenResponse
from app.services.calendar_feed_service import (
    CalendarFeedService,
    InvalidFeedToken,
    generate_feed_token,
    parse_feed_token,
)

router = APIRouter(
    prefix="/calendar",
    tags=["Calendar"],
)

CALENDAR_LIMIT = "60/minute"

CALENDAR_MEDIA_TYPE = "text/calendar; charset=utf-8"


def _ics_response(body: str, filename: str) -> Response:
    """
    An .ics response with the headers clients actually look at.

    ``Content-Disposition: attachment`` is what makes a browser hand the file
    to the calendar application instead of rendering it as text. The feed
    endpoint deliberately does not use it -- a subscription is polled, not
    downloaded, and an attachment header there produces a download prompt every
    time somebody opens the URL in a browser to check it.
    """
    return Response(
        content=body,
        media_type=CALENDAR_MEDIA_TYPE,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get(
    "/feed-token",
    response_model=CalendarFeedTokenResponse,
    summary="Get the URL to subscribe to in a calendar client",
)
@limiter.limit(CALENDAR_LIMIT)
def get_feed_token(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    """
    Mint a feed token and return the URL built from it.

    Calling this again issues a new token. The previous one keeps working until
    it expires -- feed tokens are stateless, so there is nothing to delete. See
    ``docs/calendar_feeds.md``.
    """
    token = generate_feed_token(current_user.id)

    return CalendarFeedTokenResponse(
        token=token,
        feed_url=str(request.url_for("get_calendar_feed")) + f"?token={token}",
    )


@router.get(
    "/events.ics",
    name="get_calendar_feed",
    summary="Subscribable calendar feed",
    response_class=Response,
)
@limiter.limit(CALENDAR_LIMIT)
def get_calendar_feed(
    request: Request,
    token: str = Query(description="A feed token from /api/calendar/feed-token."),
    db: Session = Depends(get_database),
):
    """
    Every dated item for the user the token belongs to.

    A bad token gets 404, not 401. A 401 that distinguishes "wrong token" from
    "no such feed" is an oracle for guessing tokens, and a calendar client
    cannot do anything useful with a 401 anyway.
    """
    try:
        user_id = parse_feed_token(token)
    except InvalidFeedToken:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calendar feed not found.",
        )

    service = CalendarFeedService(db)
    body = service.render_feed(user_id)

    # No Content-Disposition here: this URL is polled by a subscription, and an
    # attachment header turns every manual visit into a download prompt.
    return Response(content=body, media_type=CALENDAR_MEDIA_TYPE)


@router.get(
    "/hackathons/{hackathon_id}.ics",
    summary="Download one hackathon as a calendar event",
    response_class=Response,
)
@limiter.limit(CALENDAR_LIMIT)
def download_hackathon_event(
    request: Request,
    hackathon_id: uuid.UUID,
    db: Session = Depends(get_database),
    current_user: User = Depends(get_current_user),
):
    """The "Add to calendar" button next to a hackathon."""
    hackathon = db.get(Hackathon, hackathon_id)
    if hackathon is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hackathon not found",
        )

    service = CalendarFeedService(db)
    if not service.can_read_hackathon(hackathon, current_user.id):
        # 404 rather than 403: an unpublished hackathon should not confirm its
        # own existence to somebody who cannot see it.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hackathon not found",
        )

    return _ics_response(
        service.render_hackathon(hackathon),
        f"hackathon-{hackathon.id}.ics",
    )


@router.get(
    "/milestones/{milestone_id}.ics",
    summary="Download one milestone as a calendar event",
    response_class=Response,
)
@limiter.limit(CALENDAR_LIMIT)
def download_milestone_event(
    request: Request,
    milestone_id: uuid.UUID,
    db: Session = Depends(get_database),
    current_user: User = Depends(get_current_user),
):
    """The "Add to calendar" button next to a milestone."""
    milestone = db.get(Milestone, milestone_id)
    if milestone is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Milestone not found",
        )

    if milestone.due_date is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="That milestone has no due date to add to a calendar.",
        )

    service = CalendarFeedService(db)
    if not service.can_read_milestone(milestone, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Milestone not found",
        )

    return _ics_response(
        service.render_milestone(milestone),
        f"milestone-{milestone.id}.ics",
    )
