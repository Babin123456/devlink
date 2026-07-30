from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.dependencies import get_database, get_current_user
from app.middleware.rate_limit import limiter
from app.models.user import User
from app.schemas.project_tag import (
    PredefinedTagsResponse,
    ProjectTagRequest,
    ProjectTagResponse,
)
from app.services.project_tag_service import ProjectTagService

router = APIRouter(
    tags=["Project Tags"],
)

PROJECT_TAG_LIMIT = "10/minute"


@router.get(
    "/predefined",
    response_model=PredefinedTagsResponse,
    summary="Get predefined project tags and categories",
)
@router.get(
    "/project-tags/predefined",
    response_model=PredefinedTagsResponse,
    summary="Get predefined project tags and categories",
    include_in_schema=False,
)
def get_predefined_tags():
    """
    Get the list of predefined project tags/categories.

    Includes core categories like AI, Web, Mobile, Open Source, Blockchain, Cybersecurity, etc.
    """
    tags = ProjectTagService.get_predefined_tags()
    return PredefinedTagsResponse(tags=tags)


@router.post(
    "/project-tags",
    response_model=ProjectTagResponse,
)
@router.post(
    "/generate",
    response_model=ProjectTagResponse,
    include_in_schema=False,
)
@limiter.limit(PROJECT_TAG_LIMIT)
def generate_project_tags(
    request: Request,
    body: ProjectTagRequest,
    db: Session = Depends(get_database),
    current_user: User = Depends(get_current_user),
):
    """
    Generate AI-powered tag suggestions for a project.

    Analyzes the project title, description, and tech stack to suggest
    relevant tags with confidence scores.
    """
    tags = ProjectTagService.generate_tags(
        title=body.title,
        description=body.description,
        tech_stack=body.tech_stack,
    )

    return ProjectTagResponse(tags=tags)
