from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class SessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    device_name: Optional[str] = None
    device_type: Optional[str] = None
    browser: Optional[str] = None
    operating_system: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    is_revoked: bool
    created_at: datetime
    last_used_at: Optional[datetime] = None
    expires_at: datetime
    is_current: bool = Field(
        default=False,
        description="Indicates whether this is the session used for the current request",
    )


class RevokeSessionResponse(BaseModel):
    success: bool = True
    message: str
    revoked_count: int = 1
