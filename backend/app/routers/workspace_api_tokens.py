from __future__ import annotations

import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.rbac import ORG_MANAGE_TOKENS
from app.dependencies import get_database, get_current_user, require_org_permission
from app.models.user import User
from app.schemas.workspace_api_token import (
    WorkspaceApiTokenCreate,
    WorkspaceApiTokenCreateResponse,
    WorkspaceApiTokenResponse,
)
from app.services.workspace_api_token_service import WorkspaceApiTokenService

router = APIRouter(
    prefix="/organizations/{organization_id}/tokens",
    tags=["Workspace API Tokens"],
)


@router.post(
    "/",
    response_model=WorkspaceApiTokenCreateResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_org_permission(ORG_MANAGE_TOKENS))],
)
def create_token(
    organization_id: uuid.UUID,
    schema: WorkspaceApiTokenCreate,
    db: Session = Depends(get_database),
    current_user: User = Depends(get_current_user),
):
    raw_token, db_token = WorkspaceApiTokenService.create_token(
        db=db,
        organization_id=organization_id,
        user_id=current_user.id,
        schema=schema,
    )
    # Map db_token and add raw_token to response
    token_dict = {
        "id": db_token.id,
        "organization_id": db_token.organization_id,
        "name": db_token.name,
        "prefix": db_token.prefix,
        "scopes": db_token.scopes,
        "expires_at": db_token.expires_at,
        "last_used_at": db_token.last_used_at,
        "is_active": db_token.is_active,
        "created_at": db_token.created_at,
        "token": raw_token,
    }
    return WorkspaceApiTokenCreateResponse.model_validate(token_dict)


@router.get(
    "/",
    response_model=list[WorkspaceApiTokenResponse],
    dependencies=[Depends(require_org_permission(ORG_MANAGE_TOKENS))],
)
def list_tokens(
    organization_id: uuid.UUID,
    db: Session = Depends(get_database),
):
    tokens = WorkspaceApiTokenService.list_tokens(
        db=db, organization_id=organization_id
    )
    return tokens


@router.delete(
    "/{token_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_org_permission(ORG_MANAGE_TOKENS))],
)
def revoke_token(
    organization_id: uuid.UUID,
    token_id: uuid.UUID,
    db: Session = Depends(get_database),
    current_user: User = Depends(get_current_user),
):
    success = WorkspaceApiTokenService.revoke_token(
        db=db,
        organization_id=organization_id,
        token_id=token_id,
        user_id=current_user.id,
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token not found or already inactive.",
        )
    return
