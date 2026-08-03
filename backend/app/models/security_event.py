from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    JSON,
    String,
    Text,
    func,
)
from sqlalchemy import (
    Enum as SqlEnum,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class SecurityEventType(str, Enum):
    FAILED_LOGIN = "failed_login"
    PASSWORD_RESET = "password_reset"
    EMAIL_CHANGE = "email_change"
    PERMISSION_UPDATE = "permission_update"
    SUSPICIOUS_API_USAGE = "suspicious_api_usage"
    ACCOUNT_LOCKOUT = "account_lockout"


class SecurityEventSeverity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SecurityEvent(Base):
    """
    Security Event Monitoring Model (#613)
    Stores critical security-related events for alerting and administrative review.
    """

    __tablename__ = "security_events"

    # ==========================================================
    # Primary Key
    # ==========================================================

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # ==========================================================
    # Event Classification
    # ==========================================================

    event_type: Mapped[SecurityEventType] = mapped_column(
        SqlEnum(SecurityEventType),
        nullable=False,
        index=True,
    )

    severity: Mapped[SecurityEventSeverity] = mapped_column(
        SqlEnum(SecurityEventSeverity),
        default=SecurityEventSeverity.INFO,
        nullable=False,
        index=True,
    )

    risk_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # ==========================================================
    # Actor / Target References
    # ==========================================================

    actor_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    target_user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # ==========================================================
    # Context & Client Details
    # ==========================================================

    ip_address: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
        index=True,
    )

    user_agent: Mapped[str | None] = mapped_column(
        String(512),
        nullable=True,
    )

    request_method: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    request_path: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    # ==========================================================
    # Alerting & Resolution State
    # ==========================================================

    alert_triggered: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
    )

    alert_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    is_resolved: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
    )

    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    resolved_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    resolution_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ==========================================================
    # Metadata Payload
    # ==========================================================

    metadata_payload: Mapped[dict | None] = mapped_column(
        JSONB().with_variant(JSON, "sqlite"),
        nullable=True,
    )

    # ==========================================================
    # Relationships
    # ==========================================================

    actor = relationship(
        "User",
        foreign_keys=[actor_id],
        backref="triggered_security_events",
    )

    target_user = relationship(
        "User",
        foreign_keys=[target_user_id],
        backref="targeted_security_events",
    )

    resolved_by = relationship(
        "User",
        foreign_keys=[resolved_by_id],
    )

    # ==========================================================
    # Audit Timestamp
    # ==========================================================

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )

    def __repr__(self) -> str:
        return (
            f"<SecurityEvent(id={self.id}, type='{self.event_type.value}', "
            f"severity='{self.severity.value}', alert={self.alert_triggered})>"
        )
