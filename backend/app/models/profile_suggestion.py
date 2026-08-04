from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class ProfileSuggestionDismissal(Base):
    """
    Tracks AI profile improvement suggestions dismissed by users.
    """

    __tablename__ = "profile_suggestion_dismissals"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "suggestion_id",
            name="uq_user_suggestion_dismissal",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    suggestion_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    dismissed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user = relationship(
        "User",
        foreign_keys=[user_id],
        backref="dismissed_profile_suggestions",
    )

    def __repr__(self) -> str:
        return f"<ProfileSuggestionDismissal(user_id={self.user_id}, suggestion_id='{self.suggestion_id}')>"
