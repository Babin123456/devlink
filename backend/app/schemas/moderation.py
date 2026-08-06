"""Request and response shapes for the moderation preview endpoint."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

MAX_TEXT_LENGTH = 20000


class ModerationCheckRequest(BaseModel):
    """Text to score, plus optional context about who wrote it."""

    text: str = Field(min_length=1, max_length=MAX_TEXT_LENGTH)

    account_age_days: Optional[int] = Field(
        default=None,
        ge=0,
        description="Age of the author's account. Changes the weighting; a new account posting links is not the same event as an old one doing it.",
    )
    prior_flags: int = Field(
        default=0,
        ge=0,
        description="How many of the author's previous submissions were flagged.",
    )
    is_verified: bool = False


class ModerationSignalResponse(BaseModel):
    """One rule that fired."""

    category: str
    rule: str
    weight: float
    detail: str = ""


class ModerationCheckResponse(BaseModel):
    """
    The recommendation, and every rule behind it.

    The signals are always returned. A moderation decision nobody can explain
    is a moderation decision nobody can appeal, and somebody will eventually
    have to answer a "why was my post blocked" ticket.
    """

    action: str = Field(description="One of: allow, flag, review, block.")
    score: float
    signals: list[ModerationSignalResponse]
    explanation: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "action": "review",
                "score": 0.75,
                "signals": [
                    {
                        "category": "spam",
                        "rule": "url_shortener",
                        "weight": 0.4,
                        "detail": "bit.ly",
                    },
                    {
                        "category": "spam",
                        "rule": "spam_phrase",
                        "weight": 0.3,
                        "detail": "guaranteed returns",
                    },
                ],
                "explanation": "review @ 0.75: url_shortener (+0.40), spam_phrase (+0.30)",
            }
        }
    }
