from __future__ import annotations

import uuid

# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, HTTPException, status

# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_database
from app.models.user import User
from app.schemas.notification import (
    NotificationCreate,
    NotificationResponse,
    NotificationUpdate,
)
from app.services.notification_service import NotificationService

router = APIRouter(
    tags=["Notifications"],
)


@router.post(
    "/",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_database),
    current_user: User = Depends(get_current_user),
):

    return NotificationService.create_notification(
        db=db,
        recipient_id=notification.recipient_id,
        sender_id=current_user.id,
        notification=notification,
    )


@router.get(
    "/",
    response_model=list[NotificationResponse],
)
def list_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_database),
):

    return NotificationService.list_notifications(
        db,
        current_user.id,
    )


@router.get(
    "/unread",
    response_model=list[NotificationResponse],
)
def unread_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_database),
):

    return NotificationService.list_unread_notifications(
        db,
        current_user.id,
    )


@router.get(
    "/unread/count",
)
def unread_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_database),
):

    return {
        "count": NotificationService.unread_count(
            db,
            current_user.id,
        )
    }


@router.patch(
    "/read-all",
)
def mark_all_as_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_database),
):

    NotificationService.mark_all_as_read(
        db,
        current_user.id,
    )

    return {
        "message": "All notifications marked as read",
    }


@router.get(
    "/{notification_id}",
    response_model=NotificationResponse,
)
def get_notification(
    notification_id: uuid.UUID,
    db: Session = Depends(get_database),
):

    notification = NotificationService.get_notification(
        db,
        notification_id,
    )

    if notification is None:
        raise HTTPException(
            status_code=404,
            detail="Notification not found",
        )

    return notification


@router.patch(
    "/{notification_id}/read",
    response_model=NotificationResponse,
)
def mark_as_read(
    notification_id: uuid.UUID,
    db: Session = Depends(get_database),
):

    notification = NotificationService.get_notification(
        db,
        notification_id,
    )

    if notification is None:
        raise HTTPException(
            status_code=404,
            detail="Notification not found",
        )

    return NotificationService.mark_as_read(
        db,
        notification,
    )


@router.put(
    "/{notification_id}",
    response_model=NotificationResponse,
)
def update_notification(
    notification_id: uuid.UUID,
    notification: NotificationUpdate,
    db: Session = Depends(get_database),
):

    db_notification = NotificationService.get_notification(
        db,
        notification_id,
    )

    if db_notification is None:
        raise HTTPException(
            status_code=404,
            detail="Notification not found",
        )

    return NotificationService.update_notification(
        db,
        db_notification,
        notification,
    )


@router.delete(
    "/{notification_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_notification(
    notification_id: uuid.UUID,
    db: Session = Depends(get_database),
):

    notification = NotificationService.get_notification(
        db,
        notification_id,
    )

    if notification is None:
        raise HTTPException(
            status_code=404,
            detail="Notification not found",
        )

    NotificationService.delete_notification(
        db,
        notification,
    )


from pydantic import BaseModel
class NotificationPreferenceUpdate(BaseModel):
    email_enabled: bool | None = None
    websocket_enabled: bool | None = None
    database_enabled: bool | None = None
    project_updates: bool | None = None
    invitations: bool | None = None
    role_changes: bool | None = None
    marketing_emails: bool | None = None
    system_alerts: bool | None = None

@router.get("/preferences")
def get_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_database),
):
    from app.services.notifications import dispatcher
    return dispatcher._get_user_preferences(db, current_user.id)

@router.put("/preferences")
def update_preferences(
    prefs: NotificationPreferenceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_database),
):
    from app.services.notifications import dispatcher
    db_prefs = dispatcher._get_user_preferences(db, current_user.id)
    
    update_data = prefs.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(db_prefs, k, v)
    
    db.commit()
    db.refresh(db_prefs)
    return db_prefs
