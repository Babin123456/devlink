from __future__ import annotations

import uuid
from datetime import datetime, time
from enum import Enum
from typing import Optional

# pyrefly: ignore [missing-import]
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    HttpUrl,
    model_validator,
)
from app.core.validation import NameStr, UsernameStr, ValidEmail, HeadlineStr, BioStr, ValidURL, SanitizedStr


class AvailabilitySlot(BaseModel):
    day: str
    start_time: time
    end_time: time

    @model_validator(mode="after")
    def validate_times(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class PrivacyVisibility(str, Enum):
    PUBLIC = "public"
    FOLLOWERS = "followers"
    AUTHENTICATED = "authenticated"
    PRIVATE = "private"


class PrivacySettings(BaseModel):
    email: PrivacyVisibility = PrivacyVisibility.PRIVATE
    github: PrivacyVisibility = PrivacyVisibility.PUBLIC
    resume: PrivacyVisibility = PrivacyVisibility.PUBLIC
    social_links: PrivacyVisibility = PrivacyVisibility.PUBLIC
    availability: PrivacyVisibility = PrivacyVisibility.PUBLIC


class PrivacySettingsUpdate(BaseModel):
    email: Optional[PrivacyVisibility] = None
    github: Optional[PrivacyVisibility] = None
    resume: Optional[PrivacyVisibility] = None
    social_links: Optional[PrivacyVisibility] = None
    availability: Optional[PrivacyVisibility] = None


# ==========================================================
# Base User Schema
# ==========================================================


class UserBase(BaseModel):
    first_name: NameStr
    last_name: NameStr

    username: UsernameStr

    public_email: Optional[ValidEmail] = None

    headline: Optional[HeadlineStr] = None

    bio: Optional[BioStr] = None

    location: Optional[SanitizedStr] = None
    timezone: Optional[SanitizedStr] = None

    website: Optional[ValidURL] = None
    resume_url: Optional[ValidURL] = None
    portfolio_url: Optional[ValidURL] = None
    github_url: Optional[ValidURL] = None
    linkedin_url: Optional[ValidURL] = None

    role: Optional[SanitizedStr] = None
    experience_level: Optional[SanitizedStr] = None
    company: Optional[SanitizedStr] = None

    open_to_work: bool = True
    is_private: bool = False
    privacy_settings: Optional[PrivacySettings] = Field(default_factory=PrivacySettings)
    availability: list[AvailabilitySlot] = Field(default_factory=list)


# ==========================================================
# Create User
# ==========================================================


class UserCreate(UserBase):
    email: ValidEmail
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "first_name": "Jane",
                "last_name": "Doe",
                "username": "janedoe",
                "email": "jane.doe@example.com",
                "password": "StrongPassword123!",
                "open_to_work": True
            }
        }
    )


# ==========================================================
# Update User
# ==========================================================


class UserUpdate(BaseModel):
    first_name: Optional[NameStr] = None
    last_name: Optional[NameStr] = None

    headline: Optional[HeadlineStr] = None
    bio: Optional[BioStr] = None

    location: Optional[SanitizedStr] = None
    timezone: Optional[SanitizedStr] = None
    public_email: Optional[ValidEmail] = None

    website: Optional[ValidURL] = None
    resume_url: Optional[ValidURL] = None
    portfolio_url: Optional[ValidURL] = None
    github_url: Optional[ValidURL] = None
    linkedin_url: Optional[ValidURL] = None

    role: Optional[SanitizedStr] = None
    experience_level: Optional[SanitizedStr] = None
    company: Optional[SanitizedStr] = None

    open_to_work: Optional[bool] = None
    is_private: Optional[bool] = None
    privacy_settings: Optional[PrivacySettingsUpdate] = None
    availability: Optional[list[AvailabilitySlot]] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "first_name": "Jane",
                "last_name": "Smith",
                "headline": "Senior Full-Stack Developer",
                "bio": "I love building scalable web applications.",
                "location": "San Francisco, CA",
                "github_url": "https://github.com/janesmith"
            }
        }
    )


# ==========================================================
# Public User Response
# ==========================================================


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID

    profile_image: Optional[str] = None
    cover_image: Optional[str] = None
    badges: list[str] = Field(default_factory=list)

    is_active: bool
    is_verified: bool
    premium: bool = False
    is_superuser: bool

    last_seen: Optional[datetime] = Field(
        default=None,
        description="The date and time when the user was last active.",
    )
    is_online: bool = Field(
        default=False,
        description="Whether the user is currently online based on the active threshold.",
    )
    last_active_at: Optional[datetime] = None

    created_at: datetime
    updated_at: datetime

    deleted_at: Optional[datetime] = None
    deleted_by_id: Optional[uuid.UUID] = None


# ==========================================================
# Private User Response
# ==========================================================


class CurrentUser(UserResponse):
    email: ValidEmail
    email_verified_at: Optional[datetime] = None
    last_login: Optional[datetime] = None


# ==========================================================
# Profile Statistics
# ==========================================================


class UserStats(BaseModel):
    projects: int = 0
    followers: int = 0
    following: int = 0
    applications: int = 0
    accepted: int = 0


# ==========================================================
# Developer Profile
# ==========================================================


class DeveloperProfile(BaseModel):
    user: UserResponse
    stats: UserStats


# ==========================================================
# Generic API Response
# ==========================================================


class UserMessage(BaseModel):
    message: str


# ==========================================================
# Username Availability
# ==========================================================


class UsernameAvailabilityResponse(BaseModel):
    available: bool
    message: str


# ==========================================================
# Profile Completion Response
# ==========================================================


class ProfileCompletionResponse(BaseModel):
    completion: int = Field(
        ...,
        ge=0,
        le=100,
        description="Profile completion percentage (0-100)",
    )
    missing: list[str] = Field(
        ...,
        description="List of missing profile factors",
    )
    completed_factors: list[str] = Field(
        default_factory=list,
        description="List of completed profile factors",
    )
    reward_unlocked: bool = Field(
        default=False,
        description="Whether the profile completion reward is unlocked",
    )
    reward_badge: Optional[str] = Field(
        default=None,
        description="Badge awarded for 100% profile completion",
    )
