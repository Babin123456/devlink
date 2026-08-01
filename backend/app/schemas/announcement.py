from __future__ import annotations

import uuid
from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.user import UserResponse


class AnnouncementCreate(BaseModel):
    title: str = Field(..., max_length=200, description="Title of the announcement")
    content: str = Field(..., description="Content text of the announcement")


class AnnouncementResponse(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    author_id: uuid.UUID
    title: str
    content: str
    created_at: datetime
    author: UserResponse

    class Config:
        from_attributes = True
