from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class ProjectDocumentBase(BaseModel):
    title: str = Field(default="Untitled Document", max_length=255)
    content: str = Field(default="")


class ProjectDocumentCreate(ProjectDocumentBase):
    pass


class ProjectDocumentUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=255)
    content: str | None = Field(default=None)
    base_version: int | None = Field(
        default=None,
        description="Base version for optimistic concurrency conflict resolution",
    )


class ProjectDocumentResponse(ProjectDocumentBase):
    id: UUID
    project_id: UUID
    version: int
    created_by_id: UUID | None = None
    last_edited_by_id: UUID | None = None
    created_at: datetime
    updated_at: datetime
    conflict: bool = False

    model_config = ConfigDict(from_attributes=True)


class ProjectDocumentListResponse(BaseModel):
    total: int
    documents: list[ProjectDocumentResponse]
