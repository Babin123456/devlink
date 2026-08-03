from __future__ import annotations

import uuid
from datetime import datetime

# pyrefly: ignore [missing-import]
from sqlalchemy import func, select

# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.schemas.notification import (
    NotificationCreate,
    NotificationUpdate,
)
from app.core.cache import cached


class NotificationService:
    """
    Business logic for notifications.
    """

    @staticmethod
    def notify(
        db: Session,
        recipient_id,
        sender_id,
        type,
        title,
        message,
        action_url=None,
        image_url=None,
        project_id=None,
        conversation_id=None,
        message_id=None,
        application_id=None,
        channels=None,
        priority=None,
    ):
        if sender_id is not None and recipient_id == sender_id:
            return None

        from app.services.notifications import dispatcher
        from app.models.notification import NotificationType, NotificationPriority

        if not isinstance(type, NotificationType):
            try:
                type = NotificationType(type)
            except ValueError:
                pass

        if not priority:
            priority = NotificationPriority.NORMAL

        metadata_info = {
            "project_id": str(project_id) if project_id else None,
            "conversation_id": str(conversation_id) if conversation_id else None,
            "message_id": str(message_id) if message_id else None,
            "application_id": str(application_id) if application_id else None,
        }

        return dispatcher.dispatch(
            db=db,
            recipient_id=recipient_id,
            sender_id=sender_id,
            notification_type=type,
            title=title,
            message=message,
            channels=channels,
            priority=priority,
            metadata_info=metadata_info,
            action_url=action_url,
            image_url=image_url,
        )

    @staticmethod
    def create_notification(
        db: Session,
        recipient_id: uuid.UUID,
        sender_id: uuid.UUID | None,
        notification: NotificationCreate,
    ) -> Notification:
        db_notification = Notification(sender_id=sender_id, **notification.model_dump())
        db.add(db_notification)
        db.flush()
        db.refresh(db_notification)
        return db_notification

    @staticmethod
    def get_notification(
        db: Session,
        notification_id: uuid.UUID,
    ) -> Notification | None:

        return db.get(Notification, notification_id)

    @staticmethod
    def list_notifications(
        db: Session,
        recipient_id: uuid.UUID,
    ) -> list[Notification]:

        stmt = (
            select(Notification)
            .where(Notification.recipient_id == recipient_id)
            .order_by(Notification.created_at.desc())
        )

        return list(db.scalars(stmt))

    @staticmethod
    def list_unread_notifications(
        db: Session,
        recipient_id: uuid.UUID,
    ) -> list[Notification]:

        stmt = (
            select(Notification)
            .where(
                Notification.recipient_id == recipient_id,
                Notification.is_read.is_(False),
            )
            .order_by(Notification.created_at.desc())
        )

        return list(db.scalars(stmt))

    @staticmethod
    @cached(ttl=30, key_prefix="notifications:unread_count")
    def unread_count(
        db: Session,
        recipient_id: uuid.UUID,
    ) -> int:
        stmt = (
            select(func.count())
            .select_from(Notification)
            .where(
                Notification.recipient_id == recipient_id,
                Notification.is_read.is_(False),
            )
        )

        return db.scalar(stmt) or 0

    @staticmethod
    def mark_as_read(
        db: Session,
        db_notification: Notification,
    ) -> Notification:

        db_notification.is_read = True
        db_notification.read_at = datetime.utcnow()

        db.flush()
        db.refresh(db_notification)

        return db_notification

    @staticmethod
    def mark_all_as_read(
        db: Session,
        recipient_id: uuid.UUID,
    ) -> None:

        stmt = select(Notification).where(
            Notification.recipient_id == recipient_id,
            Notification.is_read.is_(False),
        )

        notifications = list(db.scalars(stmt))

        for notification in notifications:
            notification.is_read = True
            notification.read_at = datetime.utcnow()

        db.flush()

    @staticmethod
    def update_notification(
        db: Session,
        db_notification: Notification,
        notification: NotificationUpdate,
    ) -> Notification:

        data = notification.model_dump(exclude_unset=True)

        for key, value in data.items():
            setattr(db_notification, key, value)

        db.flush()
        db.refresh(db_notification)

        return db_notification

    @staticmethod
    def delete_notification(
        db: Session,
        db_notification: Notification,
    ) -> None:

        db.delete(db_notification)
        db.flush()

    @staticmethod
    def enqueue(
        db: Session,
        recipient_id,
        sender_id,
        type,
        title,
        message,
        action_url=None,
        image_url=None,
        project_id=None,
        conversation_id=None,
        message_id=None,
        application_id=None,
    ):
        from app.tasks.notification_tasks import send_notification_task

        payload = {
            "recipient_id": str(recipient_id) if recipient_id else None,
            "sender_id": str(sender_id) if sender_id else None,
            "type": type.value if hasattr(type, "value") else type,
            "title": title,
            "message": message,
            "action_url": action_url,
            "image_url": image_url,
            "project_id": str(project_id) if project_id else None,
            "conversation_id": str(conversation_id) if conversation_id else None,
            "message_id": str(message_id) if message_id else None,
            "application_id": str(application_id) if application_id else None,
        }

        send_notification_task.delay(payload)
