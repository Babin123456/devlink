import uuid
from typing import Any
from sqlalchemy.orm import Session
from app.models.notification import Notification, NotificationType, NotificationPriority
from app.models.user import User
from app.services.email_service import EmailService
from app.services.notifications.channels.base import NotificationChannel

class EmailChannel(NotificationChannel):
    @property
    def name(self) -> str:
        return "email"

    def send(
        self,
        db: Session,
        recipient_id: uuid.UUID,
        sender_id: uuid.UUID | None,
        notification_type: NotificationType,
        title: str,
        message: str,
        priority: NotificationPriority,
        metadata_info: dict[str, Any] | None = None,
        action_url: str | None = None,
        image_url: str | None = None,
    ) -> Notification | None:
        
        user = db.get(User, recipient_id)
        if not user or not user.email:
            return None

        # Call EmailService
        success = EmailService.send_notification_email(
            to_email=user.email,
            title=title,
            message=message,
            action_url=action_url,
        )

        # We typically don't create a Notification database record for the email channel itself
        # since DatabaseChannel handles the persistence, but we could log it.
        return None
