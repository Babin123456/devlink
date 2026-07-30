from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.audit_log import (
    AuditAction,
    AuditLog,
)
from app.middleware.audit_context import (
    audit_ip_address,
    audit_user_agent,
    audit_request_method,
    audit_request_path,
)

class AuditLogService:
    """
    Business logic for audit logging.
    """

    @staticmethod
    def create_log(
        db: Session,
        *,
        actor_id: uuid.UUID | None,
        action: AuditAction,
        entity_type: str,
        entity_id: str | None = None,
        target_user_id: uuid.UUID | None = None,
        project_id: uuid.UUID | None = None,
        organization_id: uuid.UUID | None = None,
        old_values: dict | None = None,
        new_values: dict | None = None,
        metadata_info: dict | None = None,
        description: str | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
        request_method: str | None = None,
        request_path: str | None = None,
        success: bool = True,
        status_code: int | None = None,
        error_message: str | None = None,
    ) -> AuditLog:

        log = AuditLog(
            actor_id=actor_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            target_user_id=target_user_id,
            project_id=project_id,
            organization_id=organization_id,
            old_values=old_values,
            new_values=new_values,
            metadata_info=metadata_info,
            description=description,
            ip_address=ip_address or audit_ip_address.get(),
            user_agent=user_agent or audit_user_agent.get(),
            request_method=request_method or audit_request_method.get(),
            request_path=request_path or audit_request_path.get(),
            success=success,
            status_code=status_code,
            error_message=error_message,
        )

        db.add(log)
        db.flush()
        db.refresh(log)

        return log

    @staticmethod
    def get_log(
        db: Session,
        log_id: uuid.UUID,
    ) -> AuditLog | None:

        return db.get(AuditLog, log_id)

    @staticmethod
    def list_logs(
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        actor_id: uuid.UUID | None = None,
        project_id: uuid.UUID | None = None,
        organization_id: uuid.UUID | None = None,
        action: AuditAction | None = None,
        entity_type: str | None = None,
    ) -> list[AuditLog]:

        stmt = select(AuditLog)

        if actor_id:
            stmt = stmt.where(AuditLog.actor_id == actor_id)
        if project_id:
            stmt = stmt.where(AuditLog.project_id == project_id)
        if organization_id:
            stmt = stmt.where(AuditLog.organization_id == organization_id)
        if action:
            stmt = stmt.where(AuditLog.action == action)
        if entity_type:
            stmt = stmt.where(AuditLog.entity_type == entity_type)

        stmt = stmt.order_by(AuditLog.created_at.desc()).offset(skip).limit(limit)

        return list(db.scalars(stmt))

    @staticmethod
    def list_actor_logs(
        db: Session,
        actor_id: uuid.UUID,
    ) -> list[AuditLog]:

        stmt = (
            select(AuditLog)
            .where(AuditLog.actor_id == actor_id)
            .order_by(AuditLog.created_at.desc())
        )

        return list(db.scalars(stmt))

    @staticmethod
    def list_project_logs(
        db: Session,
        project_id: uuid.UUID,
    ) -> list[AuditLog]:

        stmt = (
            select(AuditLog)
            .where(AuditLog.project_id == project_id)
            .order_by(AuditLog.created_at.desc())
        )

        return list(db.scalars(stmt))

    @staticmethod
    def list_organization_logs(
        db: Session,
        organization_id: uuid.UUID,
    ) -> list[AuditLog]:

        stmt = (
            select(AuditLog)
            .where(AuditLog.organization_id == organization_id)
            .order_by(AuditLog.created_at.desc())
        )

        return list(db.scalars(stmt))

    @staticmethod
    def list_action_logs(
        db: Session,
        action: AuditAction,
    ) -> list[AuditLog]:

        stmt = (
            select(AuditLog)
            .where(AuditLog.action == action)
            .order_by(AuditLog.created_at.desc())
        )

        return list(db.scalars(stmt))

    @staticmethod
    def list_failed_logs(
        db: Session,
    ) -> list[AuditLog]:

        stmt = (
            select(AuditLog)
            .where(AuditLog.success.is_(False))
            .order_by(AuditLog.created_at.desc())
        )

        return list(db.scalars(stmt))

    @staticmethod
    def delete_log(
        db: Session,
        log: AuditLog,
    ) -> None:

        db.delete(log)
        db.flush()

    @staticmethod
    def delete_actor_logs(
        db: Session,
        actor_id: uuid.UUID,
    ) -> None:

        stmt = select(AuditLog).where(AuditLog.actor_id == actor_id)

        logs = list(db.scalars(stmt))

        for log in logs:
            db.delete(log)

        db.flush()
