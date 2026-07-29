from __future__ import annotations

import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class MilestoneCreate(BaseModel):
    title: str = Field(..., max_length=200, description="Title of the milestone")
    description: str | None = Field(default=None, description="Detailed description")
    due_date: datetime | None = Field(
        default=None, description="When the milestone is due"
    )


class MilestoneUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=200)
    description: str | None = Field(default=None)
    due_date: datetime | None = Field(default=None)
    is_completed: bool | None = Field(default=None)


class MilestoneResponse(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    title: str
    description: str | None
    due_date: datetime | None
    is_completed: bool
    created_at: datetime

    class Config:
        from_attributes = True
