from __future__ import annotations

import uuid
from typing import List

from pydantic import BaseModel, ConfigDict, Field


class DailyViewMetric(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: str = Field(..., description="Date string in YYYY-MM-DD format")
    views: int = Field(..., description="Total views for the day")
    unique_views: int = Field(..., description="Unique viewers for the day")


class ProjectAnalyticsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    project_id: uuid.UUID
    total_views: int = Field(
        ..., description="Total page views accumulated by the project"
    )
    unique_viewers: int = Field(..., description="Total distinct viewers recorded")
    daily_views: List[DailyViewMetric] = Field(
        default_factory=list,
        description="Daily breakdown of page views for the specified timeframe",
    )
