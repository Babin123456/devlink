from __future__ import annotations

# pyrefly: ignore [missing-import]
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    status,
)

import httpx
from app.core.config import settings

# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session

from app.middleware.rate_limit import (
    limiter,
    LOGIN_LIMIT,
    REGISTER_LIMIT,
)
from app.dependencies import get_database
from app.schemas.auth import (
    AuthResponse,
    LoginRequest,
    RegisterRequest,
    GitHubLoginRequest,
)
from app.schemas.user import CurrentUser
from app.services.auth_service import AuthService

router = APIRouter(
    tags=["Authentication"],
)

# ==========================================================
# Register
# ==========================================================


@router.post(
    "/register",
    response_model=CurrentUser,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
@limiter.limit(REGISTER_LIMIT)
def register(
    request: Request,
    payload: RegisterRequest,
    db: Session = Depends(get_database),
):
    """
    Create a new DevLink account.
    """

    auth_service = AuthService(db)

    user = auth_service.register(payload)

    return user


# ==========================================================
# Login
# ==========================================================


@router.post(
    "/login",
    response_model=AuthResponse,
    summary="Login",
)
@limiter.limit(LOGIN_LIMIT)
def login(
    request: Request,
    payload: LoginRequest,
    db: Session = Depends(get_database),
):
    """
    Authenticate a user.
    """

    auth_service = AuthService(db)

    return auth_service.login(payload)


@router.post(
    "/github",
    response_model=AuthResponse,
    summary="GitHub OAuth Login",
)
async def github_login(
    payload: GitHubLoginRequest,
    db: Session = Depends(get_database),
):
    """
    Authenticate a user via GitHub OAuth.
    """
    if not settings.GITHUB_CLIENT_ID or not settings.GITHUB_CLIENT_SECRET:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="GitHub OAuth is not configured.",
        )

    # 1. Exchange code for access token
    token_url = "https://github.com/login/oauth/access_token"
    headers = {"Accept": "application/json"}
    data = {
        "client_id": settings.GITHUB_CLIENT_ID,
        "client_secret": settings.GITHUB_CLIENT_SECRET,
        "code": payload.code,
    }

    async with httpx.AsyncClient() as client:
        token_res = await client.post(token_url, json=data, headers=headers)
        if token_res.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Failed to exchange code for GitHub token.",
            )

        token_data = token_res.json()
        if "error" in token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=token_data.get("error_description", "Invalid GitHub code."),
            )

        access_token = token_data["access_token"]

        # 2. Fetch user profile
        user_res = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        if user_res.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Failed to fetch GitHub profile.",
            )
        github_user = user_res.json()

        # 3. Fetch user emails
        emails_res = await client.get(
            "https://api.github.com/user/emails",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        primary_email = None
        if emails_res.status_code == 200:
            emails = emails_res.json()
            for email_obj in emails:
                if email_obj.get("primary") and email_obj.get("verified"):
                    primary_email = email_obj.get("email")
                    break

            if not primary_email:
                for email_obj in emails:
                    if email_obj.get("verified"):
                        primary_email = email_obj.get("email")
                        break

    if not primary_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A verified primary email is required for GitHub login.",
        )

    auth_service = AuthService(db)
    return auth_service.github_login(github_user, primary_email)


# pyrefly: ignore [missing-import]
