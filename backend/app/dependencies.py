from __future__ import annotations

# pyrefly: ignore [missing-import]
from uuid import UUID

# pyrefly: ignore [missing-import]
from fastapi import Depends, HTTPException, status

# pyrefly: ignore [missing-import]
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.database.session import get_db
from app.models.user import User
from app.services.auth_service import AuthService

# ---------------------------------------------------------------------
# JWT Security Scheme
# ---------------------------------------------------------------------

security = HTTPBearer(auto_error=True)
optional_security = HTTPBearer(auto_error=False)


# ---------------------------------------------------------------------
# Database Dependency
# ---------------------------------------------------------------------


def get_database():
    yield from get_db()


def get_optional_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(optional_security),
    db: Session = Depends(get_database),
) -> User | None:
    """
    Returns the currently authenticated user if token is valid, else None.
    """
    if not credentials:
        return None

    try:
        payload = decode_token(credentials.credentials)
        user_id = payload.get("sub")
        if not user_id:
            return None
        user_uuid = UUID(user_id)
        auth_service = AuthService(db)
        return auth_service.get_current_user(user_uuid)
    except Exception:
        return None


# ---------------------------------------------------------------------
# Current User
# ---------------------------------------------------------------------


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_database),
) -> User:
    """
    Returns the currently authenticated user.

    Raises:
        401 Unauthorized if token is invalid.
    """

    try:
        payload = decode_token(credentials.credentials)

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token.",
            )

        user_id = UUID(user_id)

    except Exception:
        # Try authenticating as a workspace API Token
        from app.services.workspace_api_token_service import WorkspaceApiTokenService

        token_info = WorkspaceApiTokenService.authenticate_api_token(
            db, credentials.credentials
        )
        if token_info:
            auth_service = AuthService(db)
            user = auth_service.get_current_user(token_info.created_by_id)
            if user:
                user._authenticated_via_token = True
                user._token_organization_id = token_info.organization_id
                user._token_scopes = [
                    s.strip() for s in token_info.scopes.split(",") if s.strip()
                ]
                return user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials.",
        )

    auth_service = AuthService(db)

    user = auth_service.get_current_user(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
        )

    return user


def get_optional_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(optional_security),
    db: Session = Depends(get_database),
) -> User | None:
    """
    Returns currently authenticated user if token present, or None if unauthenticated.
    """
    if not credentials:
        return None
    try:
        payload = decode_token(credentials.credentials)
        user_id = payload.get("sub")
        if not user_id:
            return None
        auth_service = AuthService(db)
        return auth_service.get_current_user(UUID(user_id))
    except Exception:
        # Try authenticating as a workspace API Token
        from app.services.workspace_api_token_service import WorkspaceApiTokenService

        token_info = WorkspaceApiTokenService.authenticate_api_token(
            db, credentials.credentials
        )
        if token_info:
            auth_service = AuthService(db)
            user = auth_service.get_current_user(token_info.created_by_id)
            if user:
                user._authenticated_via_token = True
                user._token_organization_id = token_info.organization_id
                user._token_scopes = [
                    s.strip() for s in token_info.scopes.split(",") if s.strip()
                ]
                return user
        return None


# ---------------------------------------------------------------------
# Current User ID
# ---------------------------------------------------------------------


def get_current_user_id(current_user: User = Depends(get_current_user)) -> str:
    """
    Returns the currently authenticated user's ID as a string.
    """
    return str(current_user.id)


# ---------------------------------------------------------------------
# Active User
# ---------------------------------------------------------------------


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Returns only active users.
    """

    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive account.",
        )

    return current_user


# ---------------------------------------------------------------------
# Verified User
# ---------------------------------------------------------------------


def get_current_verified_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Returns only verified users.
    """

    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email verification required.",
        )

    return current_user


# ---------------------------------------------------------------------
# Admin User
# ---------------------------------------------------------------------


def get_current_admin(
    current_user: User = Depends(get_current_verified_user),
) -> User:
    """
    Returns only administrators.
    """

    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required.",
        )

    return current_user


# ---------------------------------------------------------------------
# RBAC Permission Guards
# ---------------------------------------------------------------------

from app.core.rbac import has_org_permission, has_project_permission  # noqa: E402


def require_org_permission(action: str):
    """
    Dependency factory to check organization level permissions.
    Raises 404 if the org doesn't exist, 403 if the user lacks permission.
    """

    def dependency(
        organization_id: UUID,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_database),
    ) -> User:
        from app.models.organization import Organization as OrgModel

        org = db.get(OrgModel, organization_id)
        if not org:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found.",
            )

        # Check API token constraints
        if getattr(current_user, "_authenticated_via_token", False):
            if current_user._token_organization_id != organization_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Token not authorized for this organization.",
                )

            token_scopes = current_user._token_scopes
            if "org:admin" not in token_scopes:
                if action in ("org:update", "org:manage_members", "org:manage_tokens"):
                    if action == "org:update" and "org:write" in token_scopes:
                        pass
                    else:
                        raise HTTPException(
                            status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Scope required for action: {action}",
                        )
                elif "org:read" not in token_scopes:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Scope 'org:read' required.",
                    )
            return current_user

        if not has_org_permission(db, current_user.id, organization_id, action):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied.",
            )
        return current_user

    return dependency


def require_project_permission(action: str):
    """
    Dependency factory to check project level permissions.
    Raises 404 if the project doesn't exist, 403 if the user lacks permission.
    """

    def dependency(
        project_id: UUID,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_database),
    ) -> User:
        from app.models.project import Project as ProjectModel

        project = db.get(ProjectModel, project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found.",
            )

        # Check API token constraints
        if getattr(current_user, "_authenticated_via_token", False):
            if project.organization_id != current_user._token_organization_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Token not authorized for this project's organization.",
                )

            token_scopes = current_user._token_scopes
            if "org:admin" not in token_scopes:
                if action == "project:view":
                    if not any(
                        s in token_scopes for s in ("project:read", "project:write")
                    ):
                        raise HTTPException(
                            status_code=status.HTTP_403_FORBIDDEN,
                            detail="Scope 'project:read' required.",
                        )
                else:
                    if "project:write" not in token_scopes:
                        raise HTTPException(
                            status_code=status.HTTP_403_FORBIDDEN,
                            detail="Scope 'project:write' required.",
                        )
            return current_user

        if not has_project_permission(db, current_user.id, project_id, action):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied.",
            )
        return current_user

    return dependency
