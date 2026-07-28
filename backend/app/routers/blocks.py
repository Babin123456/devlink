from __future__ import annotations

import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_database
from app.models.user import User
from app.schemas.user import UserResponse
from app.schemas.user_block import BlockStatusResponse, UserBlockResponse
from app.services.block_service import BlockService

router = APIRouter(
    tags=["User Blocks"],
)


@router.post(
    "/{user_id}",
    response_model=UserBlockResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Block a User",
)
def block_user(
    user_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_database),
):
    """
    Block a user. Automatically removes any active follow relationship.
    """
    return BlockService.block_user(
        db=db,
        blocker_id=current_user.id,
        blocked_id=user_id,
    )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Unblock a User",
)
def unblock_user(
    user_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_database),
):
    """
    Unblock a previously blocked user.
    """
    BlockService.unblock_user(
        db=db,
        blocker_id=current_user.id,
        blocked_id=user_id,
    )
    return None


@router.get(
    "/",
    response_model=List[UserResponse],
    summary="List Blocked Users",
)
def list_blocked_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_database),
):
    """
    Get all users blocked by the current authenticated user.
    """
    return BlockService.get_blocked_users(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/{user_id}/status",
    response_model=BlockStatusResponse,
    summary="Get Block Status",
)
def get_block_status(
    user_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_database),
):
    """
    Check if current user has blocked target user or target user has blocked current user.
    """
    is_blocked_by_me = BlockService.has_blocked(db, current_user.id, user_id)
    is_blocking_me = BlockService.has_blocked(db, user_id, current_user.id)

    return BlockStatusResponse(
        is_blocked_by_me=is_blocked_by_me,
        is_blocking_me=is_blocking_me,
        has_block_relationship=is_blocked_by_me or is_blocking_me,
    )
