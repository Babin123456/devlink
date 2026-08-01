import asyncio
import uuid
import logging
from typing import Any
from sqlalchemy.orm import Session
from app.models.notification import Notification, NotificationType, NotificationPriority
from app.services.notifications.channels.base import NotificationChannel

# Assume we can import the global manager from websockets router
from app.routers.websockets import manager

logger = logging.getLogger(__name__)


class WebSocketChannel(NotificationChannel):
    @property
    def name(self) -> str:
        return "websocket"

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

        payload = {
            "type": "notification",
            "notification_type": notification_type.value,
            "title": title,
            "message": message,
            "priority": priority.value,
            "metadata_info": metadata_info,
            "action_url": action_url,
            "image_url": image_url,
        }

        # Send asynchronously via the existing websocket manager
        # Since we might be calling this from a sync context, we need to create a task
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(manager.send_personal_message(payload, str(recipient_id)))
        except RuntimeError:
            # We are outside of an event loop (e.g. running in a Celery task)
            # Use asyncio.run to send the message
            asyncio.run(manager.send_personal_message(payload, str(recipient_id)))
        except Exception as e:
            logger.error(
                f"Failed to send websocket notification to {recipient_id}: {e}"
            )

        # WebSockets do not create DB records on their own
        return None
