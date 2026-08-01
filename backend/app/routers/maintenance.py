import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies import get_current_user
from app.dependencies import get_current_user, get_database as get_db
from app.models.maintenance import MaintenanceWindow
from app.models.user import User, UserRole
from app.schemas.maintenance import (
    MaintenanceWindowCreate,
    MaintenanceWindowResponse,
    MaintenanceWindowUpdate,
)

router = APIRouter(prefix="/maintenance", tags=["maintenance"])


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can manage maintenance windows",
        )
    return current_user


@router.post("/", response_model=MaintenanceWindowResponse)
def create_maintenance_window(
    window: MaintenanceWindowCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    if window.start_time >= window.end_time:
        raise HTTPException(
            status_code=400, detail="Start time must be before end time"
        )

    db_window = MaintenanceWindow(
        start_time=window.start_time,
        end_time=window.end_time,
        message=window.message,
        is_active=window.is_active,
        created_by=current_user.id,
    )
    db.add(db_window)
    db.commit()
    db.refresh(db_window)
    return db_window


@router.get("/", response_model=List[MaintenanceWindowResponse])
def get_maintenance_windows(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    stmt = select(MaintenanceWindow).order_by(MaintenanceWindow.start_time.desc())
    windows = db.scalars(stmt).all()
    return windows


@router.get("/active", response_model=MaintenanceWindowResponse)
def get_active_maintenance_window(
    db: Session = Depends(get_db),
):
    # Publicly accessible endpoint to check if maintenance is currently scheduled/active
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc)
    stmt = (
        select(MaintenanceWindow)
        .where(
            MaintenanceWindow.is_active == True,
            MaintenanceWindow.start_time <= now,
            MaintenanceWindow.end_time >= now,
        )
        .order_by(MaintenanceWindow.start_time.desc())
        .limit(1)
    )
    window = db.scalar(stmt)
    if not window:
        raise HTTPException(status_code=404, detail="No active maintenance")
    return window


@router.patch("/{window_id}", response_model=MaintenanceWindowResponse)
def update_maintenance_window(
    window_id: uuid.UUID,
    window_update: MaintenanceWindowUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    window = db.get(MaintenanceWindow, window_id)
    if not window:
        raise HTTPException(status_code=404, detail="Maintenance window not found")

    update_data = window_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(window, field, value)

    if window.start_time >= window.end_time:
        raise HTTPException(
            status_code=400, detail="Start time must be before end time"
        )

    db.commit()
    db.refresh(window)
    return window


@router.delete("/{window_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_maintenance_window(
    window_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    window = db.get(MaintenanceWindow, window_id)
    if not window:
        raise HTTPException(status_code=404, detail="Maintenance window not found")

    db.delete(window)
    db.commit()
    return None
