"""Request and response shapes for the link preview endpoints."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

# A batch is capped because each entry is an outbound request. Without a limit
# one authenticated caller could turn a single request to us into hundreds of
# requests to somebody else.
MAX_BATCH_SIZE = 10


class LinkPreviewResponse(BaseModel):
    """Metadata for a single URL."""

    url: str = Field(description="The URL as it was submitted.")
    final_url: str = Field(
        description="Where the URL ended up after redirects, or the page's own canonical URL if it declares one.",
    )
    title: Optional[str] = None
    description: Optional[str] = None
    site_name: Optional[str] = None
    image_url: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "url": "https://example.com/blog/shipping-faster",
                "final_url": "https://example.com/blog/shipping-faster",
                "title": "Shipping faster without breaking things",
                "description": "How we cut our deploy time from 40 minutes to 4.",
                "site_name": "Example Engineering",
                "image_url": "https://example.com/img/shipping.png",
            }
        }
    }


class LinkPreviewBatchRequest(BaseModel):
    """A handful of URLs to preview in one round trip."""

    urls: list[str] = Field(
        min_length=1,
        max_length=MAX_BATCH_SIZE,
        description=f"Between 1 and {MAX_BATCH_SIZE} URLs.",
    )


class LinkPreviewBatchItem(BaseModel):
    """
    One result within a batch.

    A batch never fails as a whole. An entry that could not be previewed --
    because the URL was refused, or the site was down, or it served something
    that was not HTML -- comes back with ``preview`` unset and a reason, so the
    client can render the remaining cards and leave that one as a plain link.
    """

    url: str
    preview: Optional[LinkPreviewResponse] = None
    error: Optional[str] = None


class LinkPreviewBatchResponse(BaseModel):
    results: list[LinkPreviewBatchItem]
