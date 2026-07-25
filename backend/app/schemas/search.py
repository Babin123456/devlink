from __future__ import annotations

from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------
# Search Categories
# ---------------------------------------------------------------------


class SearchCategory(str, Enum):
    """Supported global search categories."""

    DEVELOPERS = "developers"
    PROJECTS = "projects"
    ORGANIZATIONS = "organizations"
    SKILLS = "skills"
    TAGS = "tags"


# ---------------------------------------------------------------------
# Suggestion (lightweight autocomplete) models
# ---------------------------------------------------------------------


class SearchSuggestionUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    username: str
    role: Optional[str] = None
    profile_image: Optional[str] = None


class SearchSuggestionProject(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    icon: Optional[str] = None  # Will map logo_url if any
    tagline: Optional[str] = None


class SearchSuggestionOrganization(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    slug: str
    logo_url: Optional[str] = None
    organization_type: Optional[str] = None
    verified: bool = False


class SearchSuggestionSkill(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    category: Optional[str] = None


class SearchSuggestionTag(BaseModel):
    """A tag aggregated from project.tags JSON arrays."""

    name: str
    project_count: int = 0


class SearchAutocompleteResponse(BaseModel):
    users: List[SearchSuggestionUser] = Field(default_factory=list)
    projects: List[SearchSuggestionProject] = Field(default_factory=list)
    organizations: List[SearchSuggestionOrganization] = Field(default_factory=list)
    skills: List[SearchSuggestionSkill] = Field(default_factory=list)
    tags: List[SearchSuggestionTag] = Field(default_factory=list)


# ---------------------------------------------------------------------
# Full search result models (richer than suggestions)
# ---------------------------------------------------------------------


class SearchResultUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    username: str
    role: Optional[str] = None
    headline: Optional[str] = None
    profile_image: Optional[str] = None
    location: Optional[str] = None


class SearchResultProject(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    slug: str
    tagline: Optional[str] = None
    description: str = ""
    logo_url: Optional[str] = None
    stage: Optional[str] = None
    stars: int = 0
    tags: List[str] = Field(default_factory=list)


class SearchResultOrganization(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    slug: str
    description: Optional[str] = None
    logo_url: Optional[str] = None
    organization_type: Optional[str] = None
    location: Optional[str] = None
    members_count: int = 0
    verified: bool = False
    hiring: bool = False


class SearchResultSkill(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    slug: str
    category: Optional[str] = None
    description: Optional[str] = None


class SearchResultTag(BaseModel):
    name: str
    project_count: int = 0


class SearchCounts(BaseModel):
    """Per-category counts for the active query (used for tab badges)."""

    developers: int = 0
    projects: int = 0
    organizations: int = 0
    skills: int = 0
    tags: int = 0
    total: int = 0


class SearchResponse(BaseModel):
    """Full paginated search response."""

    query: str
    category: Optional[str] = None
    page: int = 1
    limit: int = 20
    counts: SearchCounts
    users: List[SearchResultUser] = Field(default_factory=list)
    projects: List[SearchResultProject] = Field(default_factory=list)
    organizations: List[SearchResultOrganization] = Field(default_factory=list)
    skills: List[SearchResultSkill] = Field(default_factory=list)
    tags: List[SearchResultTag] = Field(default_factory=list)
