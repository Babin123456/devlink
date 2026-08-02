from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.dependencies import get_database, get_current_user
from app.models.user import User
from app.schemas.mfa import (
    MFASetupResponse,
    MFAEnableRequest,
    MFAEnableResponse,
    MFADisableRequest,
    MFARecoveryCodesRequest,
    MFARecoveryCodesResponse,
    MFAStatusResponse,
    MFAVerifyLoginRequest,
)
from app.services.mfa_service import MFAService
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth/mfa",
    tags=["Multi-Factor Authentication"],
)


@router.get(
    "/status",
    response_model=MFAStatusResponse,
    summary="Get MFA status for current user",
)
def get_mfa_status(
    current_user: User = Depends(get_current_user),
):
    return MFAStatusResponse(mfa_enabled=current_user.mfa_enabled)


@router.post(
    "/setup",
    response_model=MFASetupResponse,
    summary="Generate TOTP setup secret and QR code URI",
)
def setup_mfa(
    current_user: User = Depends(get_current_user),
):
    if current_user.mfa_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA is already enabled on your account.",
        )
    return MFAService.generate_setup(user=current_user)


@router.post(
    "/enable",
    response_model=MFAEnableResponse,
    summary="Verify TOTP code and enable MFA",
)
def enable_mfa(
    payload: MFAEnableRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_database),
):
    res = MFAService.enable_mfa(
        db=db,
        user=current_user,
        secret=payload.secret,
        code=payload.code,
    )
    return MFAEnableResponse(**res)


@router.post(
    "/disable",
    summary="Disable MFA",
)
def disable_mfa(
    payload: MFADisableRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_database),
):
    MFAService.disable_mfa(db=db, user=current_user, code=payload.code)
    return {"message": "MFA disabled successfully"}


@router.post(
    "/recovery-codes",
    response_model=MFARecoveryCodesResponse,
    summary="Regenerate single-use recovery codes",
)
def regenerate_recovery_codes(
    payload: MFARecoveryCodesRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_database),
):
    codes = MFAService.regenerate_backup_codes(
        db=db,
        user=current_user,
        code=payload.code,
    )
    return MFARecoveryCodesResponse(backup_codes=codes)


@router.post(
    "/verify-login",
    summary="Complete 2FA login using TOTP code or recovery code",
)
def verify_mfa_login(
    payload: MFAVerifyLoginRequest,
    request: Request,
    db: Session = Depends(get_database),
):
    auth_service = AuthService(db=db)
    user_agent = request.headers.get("user-agent")
    ip_address = request.client.host if request.client else None

    return auth_service.complete_mfa_login(
        mfa_token=payload.mfa_token,
        code=payload.code,
        user_agent=user_agent,
        ip_address=ip_address,
    )
