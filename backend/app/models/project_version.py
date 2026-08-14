from __future__ import annotations

import uuid
from datetime import datetime
from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy import JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class ProjectVersion(Base):
    """
    Project Version History Model (#606)
    Stores snapshots of project details when edits are made.
    """

    __tablename__ = "project_versions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    version_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )

    # Tracked Details Snapshot
    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    tagline: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    tech_stack: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    requirements: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    language: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    experience: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    stage: Mapped[str] = mapped_column(
        String(50),
        default="idea",
    )

    visibility: Mapped[str] = mapped_column(
        String(50),
        default="public",
    )

    team_roles: Mapped[dict | list | None] = mapped_column(
        JSON,
        nullable=True,
    )

    change_summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True,
    )

    # Relationships
    project = relationship("Project", backref="versions")
    created_by = relationship("User", foreign_keys=[created_by_id])

    def __repr__(self):
        return f"<ProjectVersion(project_id='{self.project_id}', version_number={self.version_number})>"
