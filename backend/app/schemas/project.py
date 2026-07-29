from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.project import ProjectStage, ProjectVisibility


class ProjectBase(BaseModel):
    title: str = Field(..., max_length=200)
    tagline: Optional[str] = Field(None, max_length=255)
    description: str
    stage: ProjectStage = ProjectStage.IDEA
    visibility: ProjectVisibility = ProjectVisibility.PUBLIC
    tech_stack: Optional[str] = None
    repository_url: Optional[str] = Field(None, max_length=500)
    website_url: Optional[str] = Field(None, max_length=500)
    demo_url: Optional[str] = Field(None, max_length=500)
    team_size: int = Field(1, ge=1)
    max_team_size: int = Field(5, ge=1)
    hiring: bool = True
    logo_url: Optional[str] = Field(None, max_length=500)
    banner_url: Optional[str] = Field(None, max_length=500)


class ProjectCreate(ProjectBase):
    slug: Optional[str] = Field(None, max_length=200)


class ProjectUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    tagline: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    stage: Optional[ProjectStage] = None
    visibility: Optional[ProjectVisibility] = None
    tech_stack: Optional[str] = None
    repository_url: Optional[str] = Field(None, max_length=500)
    website_url: Optional[str] = Field(None, max_length=500)
    demo_url: Optional[str] = Field(None, max_length=500)
    team_size: Optional[int] = Field(None, ge=1)
    max_team_size: Optional[int] = Field(None, ge=1)
    hiring: Optional[bool] = None
    logo_url: Optional[str] = Field(None, max_length=500)
    banner_url: Optional[str] = Field(None, max_length=500)
    is_archived: Optional[bool] = None


class ProjectResponse(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    slug: str
    owner_id: uuid.UUID
    stars: int = 0
    views: int = 0
    applications_count: int = 0
    is_featured: bool = False
    is_archived: bool = False
    created_at: datetime
    updated_at: datetime
