from __future__ import annotations

from typing import Any, Optional
from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    code: str = Field(
        ...,
        description="Machine-readable error code in UPPER_SNAKE_CASE",
        examples=["PROJECT_NOT_FOUND", "UNAUTHORIZED", "VALIDATION_ERROR"],
    )
    message: str = Field(
        ...,
        description="Human-readable error message",
        examples=["Project not found.", "Invalid authentication credentials."],
    )
    details: Optional[Any] = Field(
        None,
        description="Optional additional error context or validation details",
    )


class ErrorResponse(BaseModel):
    error: ErrorDetail
