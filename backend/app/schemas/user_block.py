from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserBlockBase(BaseModel):
    blocked_id: uuid.UUID


class UserBlockCreate(UserBlockBase):
    pass


class UserBlockResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    blocker_id: uuid.UUID
    blocked_id: uuid.UUID
    created_at: datetime


class BlockStatusResponse(BaseModel):
    is_blocked_by_me: bool = Field(
        ..., description="Whether the current user has blocked the target user"
    )
    is_blocking_me: bool = Field(
        ..., description="Whether the target user has blocked the current user"
    )
    has_block_relationship: bool = Field(
        ..., description="Whether either user has blocked the other"
    )


class BlockedUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    username: str
    first_name: str
    last_name: str
    headline: Optional[str] = None
    profile_image: Optional[str] = None
    blocked_at: datetime
