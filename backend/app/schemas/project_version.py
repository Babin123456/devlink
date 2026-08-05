from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class ProjectVersionResponse(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    version_number: int
    title: str
    tagline: Optional[str] = None
    description: str
    tech_stack: Optional[str] = None
    requirements: Optional[str] = None
    language: Optional[str] = None
    experience: Optional[str] = None
    stage: str
    visibility: str
    team_roles: Optional[Any] = None
    change_summary: Optional[str] = None
    created_by_id: Optional[uuid.UUID] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FieldDiff(BaseModel):
    old: Optional[Any] = None
    new: Optional[Any] = None


class ProjectVersionCompareResponse(BaseModel):
    project_id: uuid.UUID
    v1_version_number: int
    v2_version_number: str | int  # Version number or 'current'
    v1_snapshot: ProjectVersionResponse
    v2_snapshot: dict[str, Any]
    diff: dict[str, FieldDiff] = Field(
        ...,
        description="Field level diff map showing changes between the selected versions",
    )


class PaginatedProjectVersionsResponse(BaseModel):
    items: list[ProjectVersionResponse]
    total: int
    page: int
    limit: int
    pages: int
