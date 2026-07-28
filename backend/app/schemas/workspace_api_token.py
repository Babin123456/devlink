from __future__ import annotations

import uuid
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class WorkspaceApiTokenCreate(BaseModel):
    name: str = Field(
        ..., max_length=200, description="Friendly name/label for the token"
    )
    scopes: list[str] = Field(
        default=[], description="Scopes associated with this token"
    )
    expires_in_days: int | None = Field(
        default=None, ge=1, description="Expiration time in days from now"
    )


class WorkspaceApiTokenResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    name: str
    prefix: str
    scopes: list[str]
    expires_at: datetime | None
    last_used_at: datetime | None
    is_active: bool
    created_at: datetime

    @field_validator("scopes", mode="before")
    @classmethod
    def parse_scopes(cls, v):
        if isinstance(v, str):
            return [s.strip() for s in v.split(",") if s.strip()]
        return v

    class Config:
        from_attributes = True


class WorkspaceApiTokenCreateResponse(WorkspaceApiTokenResponse):
    token: str = Field(
        ..., description="The generated clear-text API token. Shown only once."
    )
