from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, Field


class SkillStat(BaseModel):
    """A single skill with the number of developers that hold it."""

    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., description="Normalized skill name")
    count: int = Field(..., description="Number of developers holding the skill")


class TechnologyStat(BaseModel):
    """A single technology with the number of projects using it."""

    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., description="Technology name (language or tag)")
    count: int = Field(..., description="Number of projects using the technology")


class CommunityStatsResponse(BaseModel):
    """Platform-wide community statistics dashboard payload."""

    model_config = ConfigDict(from_attributes=True)

    generated_at: datetime = Field(
        ..., description="Timestamp when the statistics were computed"
    )
    timeframe_days: int = Field(
        ..., description="Analysis window in days for trend-sensitive metrics"
    )

    total_developers: int = Field(..., description="Total active developer accounts")
    active_projects: int = Field(..., description="Published, non-archived projects")
    teams_formed: int = Field(..., description="Distinct projects with an active team")
    open_opportunities: int = Field(..., description="Open builder flares / roles")
    contributions_this_month: int = Field(
        ..., description="Team contributions recorded this calendar month"
    )
    new_users_this_month: int = Field(
        ..., description="New developers registered this calendar month"
    )

    most_popular_skills: List[SkillStat] = Field(
        default_factory=list,
        description="Most frequently held skills across the community",
    )
    trending_technologies: List[TechnologyStat] = Field(
        default_factory=list,
        description="Most used technologies across active projects",
    )
