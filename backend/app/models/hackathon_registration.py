from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy import (
    Enum as SqlEnum,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class RegistrationStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    WAITLISTED = "waitlisted"


class HackathonRegistration(Base):
    """
    User registration for a hackathon.
    """

    __tablename__ = "hackathon_registrations"

    __table_args__ = (
        UniqueConstraint(
            "hackathon_id",
            "user_id",
            name="uq_hackathon_registration",
        ),
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

    hackathon_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("hackathons.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    team_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("hackathon_teams.id", ondelete="SET NULL"),
    )

    # ==========================================================
    # Registration
    # ==========================================================

    status: Mapped[RegistrationStatus] = mapped_column(
        SqlEnum(RegistrationStatus),
        default=RegistrationStatus.PENDING,
        nullable=False,
        index=True,
    )

    motivation: Mapped[str | None] = mapped_column(
        Text,
    )

    experience_level: Mapped[str | None] = mapped_column(
        String(100),
    )

    # ==========================================================
    # Relationships
    # ==========================================================

    hackathon = relationship(
        "Hackathon",
        backref="registrations",
    )

    user = relationship(
        "User",
        backref="hackathon_registrations",
    )

    team = relationship(
        "HackathonTeam",
        backref="registrations",
    )

    # ==========================================================
    # Audit
    # ==========================================================

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return (
            f"<HackathonRegistration("
            f"hackathon_id={self.hackathon_id}, "
            f"user_id={self.user_id}, "
            f"status='{self.status.value}'"
            f")>"
        )
