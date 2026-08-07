from __future__ import annotations

import uuid

from pydantic import BaseModel, Field


class ConversationStarterRequest(BaseModel):
    """Request to generate conversation starters."""

    target_user_id: uuid.UUID = Field(
        ..., description="ID of the user to generate starters for"
    )


class ConversationStarterSuggestion(BaseModel):
    """A single conversation starter suggestion."""

    text: str = Field(..., description="The conversation starter message")
    confidence: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Confidence score for this suggestion (0-1)",
    )


class ConversationStarterResponse(BaseModel):
    """Response containing conversation starter suggestions."""

    suggestions: list[ConversationStarterSuggestion] = Field(
        ...,
        min_length=3,
        max_length=5,
        description="3-5 context-aware conversation starter suggestions",
    )
    target_user_id: uuid.UUID
    target_user_name: str
