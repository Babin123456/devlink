from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy import (
    Enum as SqlEnum,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class PluginType(str, Enum):
    INTEGRATION = "integration"
    WIDGET = "widget"
    WORKFLOW = "workflow"


class PluginStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DEPRECATED = "deprecated"


class Plugin(Base):
    """
    DevLink Plugin & Extension Registry Model (#582)
    Stores registered third-party and official extensions, widgets, and workflow integrations.
    """

    __tablename__ = "plugins"

    # ==========================================================
    # Primary Key
    # ==========================================================

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # ==========================================================
    # Identity & Details
    # ==========================================================

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
        index=True,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    version: Mapped[str] = mapped_column(
        String(50),
        default="1.0.0",
        nullable=False,
    )

    author_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    plugin_type: Mapped[PluginType] = mapped_column(
        SqlEnum(PluginType),
        default=PluginType.INTEGRATION,
        nullable=False,
        index=True,
    )

    status: Mapped[PluginStatus] = mapped_column(
        SqlEnum(PluginStatus),
        default=PluginStatus.ACTIVE,
        nullable=False,
        index=True,
    )

    # ==========================================================
    # Extension API Manifest Payload
    # Contains: extension_points, webhook_url, permissions, widget_config, config_schema
    # ==========================================================

    manifest: Mapped[dict] = mapped_column(
        JSONB().with_variant(JSON, "sqlite"),
        nullable=False,
        default=dict,
    )

    api_key_hash: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_official: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    install_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    # ==========================================================
    # Relationships
    # ==========================================================

    author = relationship(
        "User",
        backref="created_plugins",
    )

    # ==========================================================
    # Audit Timestamps
    # ==========================================================

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Plugin(id={self.id}, slug='{self.slug}', type='{self.plugin_type.value}')>"


class PluginInstallation(Base):
    """
    Tracks installed plugins per User or Organization (#582).
    """

    __tablename__ = "plugin_installations"

    __table_args__ = (
        UniqueConstraint("plugin_id", "user_id", name="uq_plugin_user_install"),
        UniqueConstraint("plugin_id", "organization_id", name="uq_plugin_org_install"),
    )

    # ==========================================================
    # Primary Key
    # ==========================================================

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # ==========================================================
    # Foreign Keys
    # ==========================================================

    plugin_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("plugins.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    organization_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    # ==========================================================
    # Config & State
    # ==========================================================

    is_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    config: Mapped[dict] = mapped_column(
        JSONB().with_variant(JSON, "sqlite"),
        nullable=False,
        default=dict,
    )

    # ==========================================================
    # Relationships
    # ==========================================================

    plugin = relationship(
        "Plugin",
        backref="installations",
    )

    user = relationship(
        "User",
        backref="installed_plugins",
    )

    organization = relationship(
        "Organization",
        backref="installed_plugins",
    )

    # ==========================================================
    # Audit Timestamps
    # ==========================================================

    installed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<PluginInstallation(id={self.id}, plugin_id={self.plugin_id}, enabled={self.is_enabled})>"
