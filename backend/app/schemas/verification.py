from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class VerificationRequestCreate(BaseModel):
    method: str
    evidence: str | None = None


class VerificationRequestResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    user_id: str
    method: str
    evidence: str | None = None
    status: str
    reviewed_by: str | None = None
    reviewed_at: datetime | None = None
    review_notes: str | None = None


class VerificationReview(BaseModel):
    status: str
    review_notes: str | None = None


class VerificationStatusResponse(BaseModel):
    status: str
    verified_at: datetime | None = None
