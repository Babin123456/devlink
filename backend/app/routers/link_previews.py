"""
Link preview endpoints.

Both are authenticated and rate limited. That is not incidental: this is an
endpoint whose whole job is to make our server fetch a URL somebody else chose,
which makes it an outbound-request amplifier. Anonymous access would turn it
into an open proxy, and an unlimited rate would turn it into a way to point our
egress bandwidth at a third party.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status

from app.dependencies import get_current_user
from app.middleware.rate_limit import limiter
from app.models.user import User
from app.schemas.link_preview import (
    LinkPreviewBatchItem,
    LinkPreviewBatchRequest,
    LinkPreviewBatchResponse,
    LinkPreviewResponse,
)
from app.services.link_preview_service import link_preview_service
from app.utils.url_safety import UnsafeURL

router = APIRouter(
    prefix="/link-previews",
    tags=["Link Previews"],
)

# Deliberately tighter than the general read limit. Each call is an outbound
# request to a third party, and the batch endpoint multiplies that by ten.
LINK_PREVIEW_LIMIT = "30/minute"
LINK_PREVIEW_BATCH_LIMIT = "10/minute"


@router.get(
    "",
    response_model=LinkPreviewResponse,
    summary="Preview a single URL",
)
@limiter.limit(LINK_PREVIEW_LIMIT)
def get_link_preview(
    request: Request,
    url: str = Query(description="The http(s) URL to fetch metadata for."),
    current_user: User = Depends(get_current_user),
):
    """
    Fetch Open Graph metadata for a URL.

    Returns 400 when the URL is one we refuse to fetch (wrong scheme, private
    address, disallowed port) and 404 when it is fetchable but yielded nothing
    usable -- it was unreachable, it timed out, or it did not serve HTML.
    """
    try:
        preview = link_preview_service.preview(url)
    except UnsafeURL as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    if preview is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No preview could be generated for that URL.",
        )

    return LinkPreviewResponse(**preview.as_dict())


@router.post(
    "/batch",
    response_model=LinkPreviewBatchResponse,
    summary="Preview several URLs at once",
)
@limiter.limit(LINK_PREVIEW_BATCH_LIMIT)
def get_link_previews(
    request: Request,
    body: LinkPreviewBatchRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Fetch metadata for up to ten URLs.

    Always 200. A URL that could not be previewed comes back with an ``error``
    string instead of a ``preview``, so one dead link in a message does not
    cost the reader every other card in it.
    """
    results: list[LinkPreviewBatchItem] = []

    for url in body.urls:
        try:
            preview = link_preview_service.preview(url)
        except UnsafeURL as exc:
            results.append(LinkPreviewBatchItem(url=url, error=str(exc)))
            continue

        if preview is None:
            results.append(
                LinkPreviewBatchItem(
                    url=url,
                    error="No preview could be generated for that URL.",
                )
            )
            continue

        results.append(
            LinkPreviewBatchItem(
                url=url,
                preview=LinkPreviewResponse(**preview.as_dict()),
            )
        )

    return LinkPreviewBatchResponse(results=results)
