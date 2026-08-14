"""Response shapes for the calendar endpoints."""

from __future__ import annotations

from pydantic import BaseModel, Field


class CalendarFeedTokenResponse(BaseModel):
    """
    A feed token and the URL built from it.

    Both are returned because the client needs the URL to show the user, and
    the token on its own to build a different URL if it ever needs to.
    """

    token: str = Field(
        description="Opaque, signed, scoped to the calendar feed and nothing else."
    )
    feed_url: str = Field(
        description="Paste this into a calendar client's 'subscribe to calendar' box."
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "token": "v1.PVCyXH2GTP6vHTF6vNPVKw.1785312000.9Ku2r0m2Rjk",
                "feed_url": "https://api.devlink.dev/api/calendar/events.ics?token=v1.PVCyXH2GTP6vHTF6vNPVKw.1785312000.9Ku2r0m2Rjk",
            }
        }
    }
