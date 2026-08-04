from __future__ import annotations

"""
DevLink Validation Utilities

Reusable validation functions used across the application.
"""


import re
from urllib.parse import urlparse

from fastapi import HTTPException, status

# ==========================================================
# Username Validation
# ==========================================================

USERNAME_REGEX = re.compile(r"^[a-zA-Z0-9_.-]{3,30}$")


def validate_username(username: str) -> str:
    """
    Validate username.

    Rules:
    - 3-30 characters
    - letters
    - numbers
    - underscore
    - dash
    - period
    """

    username = username.strip()

    if not USERNAME_REGEX.fullmatch(username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Username may contain only letters, "
                "numbers, underscores (_), dashes (-), "
                "and periods (.)."
            ),
        )

    return username


# ==========================================================
# Password Validation
# ==========================================================


def validate_password(
    password: str,
    username: str | None = None,
    email: str | None = None,
) -> str:
    """
    Validate password strength.

    Runs the composition rules first, then screens the candidate against the
    local blocklist of known-guessable passwords and, when enabled, the Have I
    Been Pwned corpus. ``username`` and ``email`` are optional; passing them
    additionally rejects passwords built out of the user's own identifiers.

    The screening checks are ordered cheapest-first so the network call only
    happens for a password that has already passed everything else.
    """

    if len(password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least 8 characters.",
        )

    if len(password) > 128:
        raise HTTPException(
            status_code=400,
            detail="Password is too long.",
        )

    if not re.search(r"[A-Z]", password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain an uppercase letter.",
        )

    if not re.search(r"[a-z]", password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain a lowercase letter.",
        )

    if not re.search(r"\d", password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain a number.",
        )

    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain a special character.",
        )

    _screen_password(password, username=username, email=email)

    return password


def _screen_password(
    password: str,
    username: str | None = None,
    email: str | None = None,
) -> None:
    """
    Reject passwords that are structurally fine but known to be guessable.

    Imported lazily so that ``validators`` stays a leaf module -- the breach
    service pulls in the cache manager and httpx, neither of which every
    caller of this file needs.
    """
    from app.core.config import settings
    from app.core.password_blocklist import (
        contains_personal_information,
        is_common_password,
    )

    if settings.ENABLE_PASSWORD_BLOCKLIST:
        if is_common_password(password):
            raise HTTPException(
                status_code=400,
                detail=(
                    "This password is too common and appears on public "
                    "password lists. Please choose a different one."
                ),
            )

        if contains_personal_information(password, username=username, email=email):
            raise HTTPException(
                status_code=400,
                detail=("Password must not contain your username or email address."),
            )

    if settings.ENABLE_HIBP_CHECK:
        from app.services.password_breach_service import password_breach_service

        # Fails open on any network trouble, so this cannot lock users out.
        if password_breach_service.is_compromised(password):
            raise HTTPException(
                status_code=400,
                detail=(
                    "This password has appeared in a known data breach. "
                    "Please choose a different one."
                ),
            )


# ==========================================================
# Email Validation
# ==========================================================


EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def validate_email(email: str) -> str:
    email = email.lower().strip()

    if not EMAIL_REGEX.fullmatch(email):
        raise HTTPException(
            status_code=400,
            detail="Invalid email address.",
        )

    return email


# ==========================================================
# URL Validation
# ==========================================================


def validate_url(url: str | None) -> str | None:
    if not url:
        return None

    parsed = urlparse(url)

    if parsed.scheme not in {"http", "https"}:
        raise HTTPException(
            status_code=400,
            detail="Invalid URL.",
        )

    return url


# ==========================================================
# GitHub URL
# ==========================================================


def validate_github_url(url: str | None) -> str | None:
    if not url:
        return None

    validate_url(url)

    if "github.com" not in url.lower():
        raise HTTPException(
            status_code=400,
            detail="Invalid GitHub profile URL.",
        )

    return url


# ==========================================================
# LinkedIn URL
# ==========================================================


def validate_linkedin_url(url: str | None) -> str | None:
    if not url:
        return None

    validate_url(url)

    if "linkedin.com" not in url.lower():
        raise HTTPException(
            status_code=400,
            detail="Invalid LinkedIn profile URL.",
        )

    return url


# ==========================================================
# Portfolio URL
# ==========================================================


def validate_portfolio(url: str | None) -> str | None:
    if not url:
        return None

    return validate_url(url)


# ==========================================================
# Text Sanitization
# ==========================================================


def sanitize_text(text: str | None) -> str | None:
    """
    Basic XSS protection.

    Escapes HTML characters.
    """

    if text is None:
        return None

    replacements = {
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text.strip()


# ==========================================================
# Name Validation
# ==========================================================


NAME_REGEX = re.compile(r"^[A-Za-z\s'-]{2,100}$")


def validate_name(name: str) -> str:
    name = name.strip()

    if not NAME_REGEX.fullmatch(name):
        raise HTTPException(
            status_code=400,
            detail="Invalid name.",
        )

    return name


# ==========================================================
# Generic Length Validation
# ==========================================================


def validate_length(
    value: str,
    minimum: int,
    maximum: int,
    field: str,
) -> str:
    length = len(value)

    if length < minimum:
        raise HTTPException(
            status_code=400,
            detail=f"{field} must be at least {minimum} characters.",
        )

    if length > maximum:
        raise HTTPException(
            status_code=400,
            detail=f"{field} cannot exceed {maximum} characters.",
        )

    return value


# ==========================================================
# Allowed Image Types
# ==========================================================


ALLOWED_IMAGE_TYPES = {
    "image/png",
    "image/jpeg",
    "image/webp",
}


def validate_image_type(content_type: str) -> None:
    if content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported image type.",
        )


# ==========================================================
# Max Upload Size
# ==========================================================


MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def validate_file_size(size: int) -> None:
    if size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File exceeds maximum allowed size.",
        )


# ==========================================================
# Slugify Utility
# ==========================================================


def slugify(text: str) -> str:
    """
    Generate a URL-safe lowercase slug from text.

    Example:
    'DevLink Labs!' -> 'devlink-labs'
    """
    text = text.lower().strip()
    # Replace non-alphanumeric characters with hyphens
    text = re.sub(r"[^\w\s-]", "", text)
    # Replace whitespace and repeated hyphens with a single hyphen
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")
