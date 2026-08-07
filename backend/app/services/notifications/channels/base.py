import abc
import uuid
from typing import Any
from sqlalchemy.orm import Session
from app.models.notification import Notification, NotificationType, NotificationPriority


class NotificationChannel(abc.ABC):
    """
    Abstract base class for notification delivery channels.
    """

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Name of the channel (e.g., 'email', 'database', 'websocket')."""
        pass

    @abc.abstractmethod
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
        """
        Send a notification through this channel.

        Returns:
            The created Notification database object if applicable, or None.
        """
        pass
