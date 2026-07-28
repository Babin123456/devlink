from __future__ import annotations

import logging
import re
from typing import Any, Dict

from fastapi import Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("devlink")

DEFAULT_STATUS_CODES: Dict[int, str] = {
    400: "BAD_REQUEST",
    401: "UNAUTHORIZED",
    403: "FORBIDDEN",
    404: "NOT_FOUND",
    405: "METHOD_NOT_ALLOWED",
    408: "REQUEST_TIMEOUT",
    409: "CONFLICT",
    422: "VALIDATION_ERROR",
    429: "RATE_LIMIT_EXCEEDED",
    500: "INTERNAL_SERVER_ERROR",
    502: "BAD_GATEWAY",
    503: "SERVICE_UNAVAILABLE",
}


def generate_error_code(status_code: int, message: str | None) -> str:
    """
    Generate a machine-readable UPPER_SNAKE_CASE code from message or status code.
    Example: "Project not found." -> "PROJECT_NOT_FOUND"
    Example: "Invalid email or password." -> "INVALID_EMAIL_OR_PASSWORD"
    """
    if not message or not isinstance(message, str):
        return DEFAULT_STATUS_CODES.get(status_code, "ERROR")

    cleaned = re.sub(r"[^a-zA-Z0-9\s_]", "", message).strip()
    if not cleaned:
        return DEFAULT_STATUS_CODES.get(status_code, "ERROR")

    words = cleaned.split()
    if len(words) > 6:
        return "_".join(words[:5]).upper()

    return "_".join(words).upper()


def format_error_response(
    code: str,
    message: str,
    details: Any = None,
) -> Dict[str, Any]:
    """
    Build standardized JSON response payload:
    {
        "error": {
            "code": "PROJECT_NOT_FOUND",
            "message": "Project not found."
        }
    }
    """
    error_dict: Dict[str, Any] = {
        "code": code,
        "message": message,
    }
    if details is not None:
        error_dict["details"] = details

    return {"error": error_dict}


async def http_exception_handler(
    request: Request,
    exc: HTTPException | StarletteHTTPException,
) -> JSONResponse:
    """
    Handle HTTP exceptions raised in route handlers.
    """
    status_code = exc.status_code

    if isinstance(exc.detail, dict):
        code = exc.detail.get("code") or DEFAULT_STATUS_CODES.get(status_code, "ERROR")
        message = (
            exc.detail.get("message")
            or exc.detail.get("detail")
            or "An error occurred."
        )
        details = exc.detail.get("details")
    elif isinstance(exc.detail, str):
        message = exc.detail
        code = generate_error_code(status_code, message)
        details = None
    else:
        message = str(exc.detail) if exc.detail else "An error occurred."
        code = DEFAULT_STATUS_CODES.get(status_code, "ERROR")
        details = exc.detail

    payload = format_error_response(code=code, message=message, details=details)
    return JSONResponse(status_code=status_code, content=payload)


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """
    Handle Pydantic / FastAPI request validation errors (422).
    """
    errors = exc.errors()
    message = "Request validation failed."
    if errors:
        first_err = errors[0]
        loc = " -> ".join(str(l) for l in first_err.get("loc", []) if l != "body")
        msg = first_err.get("msg", "Invalid value")
        if loc:
            message = f"Validation error: {loc}: {msg}"
        else:
            message = f"Validation error: {msg}"

    payload = format_error_response(
        code="VALIDATION_ERROR",
        message=message,
        details=errors,
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=payload,
    )


async def rate_limit_exception_handler(
    request: Request,
    exc: RateLimitExceeded,
) -> JSONResponse:
    """
    Handle SlowAPI rate limit exceeded exceptions (429).
    """
    payload = format_error_response(
        code="RATE_LIMIT_EXCEEDED",
        message="Rate limit exceeded. Please try again later.",
    )
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content=payload,
    )


async def global_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Catch-all unhandled exception handler (500).
    """
    logger.exception(f"Unhandled exception during request {request.url.path}: {exc}")
    payload = format_error_response(
        code="INTERNAL_SERVER_ERROR",
        message="An unexpected internal server error occurred.",
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=payload,
    )
