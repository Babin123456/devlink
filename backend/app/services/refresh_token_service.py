from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken


class RefreshTokenService:
    """
    Business logic for refresh tokens.
    """

    @staticmethod
    def create_token(
        db: Session,
        token: RefreshToken,
    ) -> RefreshToken:

        db.add(token)
        db.flush()
        db.refresh(token)

        return token

    @staticmethod
    def get_token(
        db: Session,
        token: str,
    ) -> RefreshToken | None:

        stmt = select(RefreshToken).where(RefreshToken.token == token)

        return db.scalar(stmt)

    @staticmethod
    def list_user_tokens(
        db: Session,
        user_id: uuid.UUID,
    ) -> list[RefreshToken]:

        stmt = (
            select(RefreshToken)
            .where(RefreshToken.user_id == user_id)
            .order_by(RefreshToken.created_at.desc())
        )

        return list(db.scalars(stmt))

    @staticmethod
    def revoke_token(
        db: Session,
        db_token: RefreshToken,
    ) -> RefreshToken:

        db_token.is_revoked = True
        db_token.revoked_at = datetime.utcnow()

        db.flush()
        db.refresh(db_token)

        return db_token

    @staticmethod
    def create_token_for_user(
        db: Session,
        user_id: uuid.UUID,
        token_str: str,
        expires_at: datetime,
        user_agent: str | None = None,
        ip_address: str | None = None,
        device_name: str | None = None,
        device_type: str | None = None,
        browser: str | None = None,
        operating_system: str | None = None,
    ) -> RefreshToken:
        token = RefreshToken(
            user_id=user_id,
            token=token_str,
            expires_at=expires_at,
            user_agent=user_agent,
            ip_address=ip_address,
            device_name=device_name,
            device_type=device_type,
            browser=browser,
            operating_system=operating_system,
        )
        db.add(token)
        db.flush()
        db.refresh(token)
        return token

    @staticmethod
    def get_active_sessions(
        db: Session,
        user_id: uuid.UUID,
    ) -> list[RefreshToken]:
        stmt = (
            select(RefreshToken)
            .where(
                RefreshToken.user_id == user_id,
                RefreshToken.is_revoked.is_(False),
            )
            .order_by(RefreshToken.created_at.desc())
        )
        tokens = list(db.scalars(stmt))
        now = datetime.now(timezone.utc)
        active_tokens = []
        for token in tokens:
            exp = token.expires_at
            if exp.tzinfo is None:
                exp = exp.replace(tzinfo=timezone.utc)
            if exp > now:
                active_tokens.append(token)
        return active_tokens

    @staticmethod
    def revoke_session_by_id(
        db: Session,
        user_id: uuid.UUID,
        session_id: uuid.UUID,
    ) -> bool:
        stmt = select(RefreshToken).where(
            RefreshToken.id == session_id,
            RefreshToken.user_id == user_id,
            RefreshToken.is_revoked.is_(False),
        )
        token = db.scalar(stmt)
        if not token:
            return False
        token.is_revoked = True
        token.revoked_at = datetime.now(timezone.utc)
        db.flush()
        return True

    @staticmethod
    def revoke_all_tokens(
        db: Session,
        user_id: uuid.UUID,
    ) -> None:
        stmt = select(RefreshToken).where(
            RefreshToken.user_id == user_id,
            RefreshToken.is_revoked.is_(False),
        )
        tokens = list(db.scalars(stmt))
        now = datetime.now(timezone.utc)
        for token in tokens:
            token.is_revoked = True
            token.revoked_at = now
        db.flush()
