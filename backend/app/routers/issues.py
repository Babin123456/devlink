from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from app.dependencies import get_database, get_current_user
from app.middleware.idempotency import IdempotentRoute
from app.middleware.rate_limit import limiter
from app.models.issue import IssueStatus
from app.models.user import User
from app.schemas.issue import (
    DifficultyEstimateResponse,
    DifficultyOverride,
    DuplicateCheckRequest,
    DuplicateCheckResponse,
    IssueCreate,
    IssueDetailResponse,
    IssueResponse,
    IssueUpdate,
)
from app.services.issue_difficulty_service import IssueDifficultyService
from app.services.issue_service import IssueService

router = APIRouter(
    tags=["Issues"],
    route_class=IdempotentRoute,
)


# ------------------------------------------------------------------
# Issue CRUD
# ------------------------------------------------------------------


@router.post(
    "/projects/{project_id}/issues",
    response_model=IssueResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("30/minute")
def create_issue(
    request: Request,
    project_id: uuid.UUID,
    issue: IssueCreate,
    db: Session = Depends(get_database),
    current_user: User = Depends(get_current_user),
):
    """Create a new issue in a project (AI difficulty is auto-estimated)."""
    return IssueService.create_issue(
        db=db,
        project_id=project_id,
        author_id=current_user.id,
        issue=issue,
    )


# ------------------------------------------------------------------
# AI Difficulty Estimation
# ------------------------------------------------------------------


@router.post(
    "/projects/{project_id}/issues/{issue_id}/estimate",
    response_model=DifficultyEstimateResponse,
)
@limiter.limit("10/minute")
def estimate_difficulty(
    request: Request,
    project_id: uuid.UUID,
    issue_id: uuid.UUID,
    db: Session = Depends(get_database),
    current_user: User = Depends(get_current_user),
):
    """
    Re-run AI difficulty estimation on an existing issue.

    Returns the estimated difficulty level (beginner/intermediate/advanced/
    expert), a 0.0-1.0 confidence score, and the reasoning behind the
    estimate. The issue is updated with the new estimate.
    """
    issue = IssueService.get_issue(db, issue_id)

    if issue is None or issue.project_id != project_id:
        raise HTTPException(
            status_code=404,
            detail="Issue not found",
        )

    result = IssueDifficultyService.estimate_difficulty(
        title=issue.title,
        description=issue.description,
        labels=issue.labels,
    )

    issue.difficulty = result.difficulty
    issue.difficulty_confidence = result.confidence
    issue.difficulty_manual_override = False

    db.add(issue)
    db.flush()
    db.refresh(issue)

    return DifficultyEstimateResponse(
        difficulty=result.difficulty,
        confidence=result.confidence,
        reasoning=result.reasoning,
    )


@router.patch(
    "/projects/{project_id}/issues/{issue_id}/difficulty",
    response_model=IssueResponse,
)
@limiter.limit("20/minute")
def override_difficulty(
    request: Request,
    project_id: uuid.UUID,
    issue_id: uuid.UUID,
    body: DifficultyOverride,
    db: Session = Depends(get_database),
    current_user: User = Depends(get_current_user),
):
    """
    Manually override the AI-estimated difficulty for an issue.

    The override is persisted with a confidence of 1.0 and flagged as a
    manual override so it is not replaced by future AI estimations.
    """
    issue = IssueService.get_issue(db, issue_id)

    if issue is None or issue.project_id != project_id:
        raise HTTPException(
            status_code=404,
            detail="Issue not found",
        )

    if issue.author_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Only the issue author can update it",
        )

    issue.difficulty = body.difficulty
    issue.difficulty_confidence = 1.0
    issue.difficulty_manual_override = True

    db.add(issue)
    db.flush()
    db.refresh(issue)

    return issue


@router.get(
    "/projects/{project_id}/issues",
    response_model=list[IssueResponse],
)
def list_issues(
    project_id: uuid.UUID,
    status_filter: IssueStatus | None = Query(None, alias="status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_database),
):
    """List all issues in a project."""
    return IssueService.list_project_issues(
        db=db,
        project_id=project_id,
        status=status_filter,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/projects/{project_id}/issues/{issue_id}",
    response_model=IssueDetailResponse,
)
def get_issue(
    project_id: uuid.UUID,
    issue_id: uuid.UUID,
    db: Session = Depends(get_database),
):
    """Get a single issue with details and duplicate suggestions."""
    issue = IssueService.get_issue(db, issue_id)

    if issue is None or issue.project_id != project_id:
        raise HTTPException(
            status_code=404,
            detail="Issue not found",
        )

    # Get duplicate suggestions
    suggestions = IssueService.get_duplicate_suggestions(db, issue_id)

    return IssueDetailResponse(
        id=issue.id,
        project_id=issue.project_id,
        author_id=issue.author_id,
        title=issue.title,
        description=issue.description,
        status=issue.status,
        priority=issue.priority,
        labels=issue.labels,
        difficulty=issue.difficulty,
        difficulty_confidence=issue.difficulty_confidence,
        difficulty_manual_override=issue.difficulty_manual_override,
        is_duplicate_checked=issue.is_duplicate_checked,
        created_at=issue.created_at,
        updated_at=issue.updated_at,
        author=issue.author,
        duplicate_suggestions=suggestions,
    )


@router.put(
    "/projects/{project_id}/issues/{issue_id}",
    response_model=IssueResponse,
)
@limiter.limit("30/minute")
def update_issue(
    request: Request,
    project_id: uuid.UUID,
    issue_id: uuid.UUID,
    issue: IssueUpdate,
    db: Session = Depends(get_database),
    current_user: User = Depends(get_current_user),
):
    """Update an issue."""
    db_issue = IssueService.get_issue(db, issue_id)

    if db_issue is None or db_issue.project_id != project_id:
        raise HTTPException(
            status_code=404,
            detail="Issue not found",
        )

    if db_issue.author_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Only the issue author can update it",
        )

    return IssueService.update_issue(db, db_issue, issue)


@router.delete(
    "/projects/{project_id}/issues/{issue_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@limiter.limit("20/minute")
def delete_issue(
    request: Request,
    project_id: uuid.UUID,
    issue_id: uuid.UUID,
    db: Session = Depends(get_database),
    current_user: User = Depends(get_current_user),
):
    """Delete an issue."""
    db_issue = IssueService.get_issue(db, issue_id)

    if db_issue is None or db_issue.project_id != project_id:
        raise HTTPException(
            status_code=404,
            detail="Issue not found",
        )

    if db_issue.author_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Only the issue author can delete it",
        )

    IssueService.delete_issue(db, db_issue)


# ------------------------------------------------------------------
# Duplicate Detection
# ------------------------------------------------------------------


@router.post(
    "/projects/{project_id}/issues/check-duplicates",
    response_model=DuplicateCheckResponse,
)
@limiter.limit("10/minute")
def check_duplicates(
    request: Request,
    project_id: uuid.UUID,
    check_request: DuplicateCheckRequest,
    db: Session = Depends(get_database),
    current_user: User = Depends(get_current_user),
):
    """
    Check for duplicate issues before creating a new one.

    Uses AI embeddings to find semantically similar issues
    within the same project.
    """
    return IssueService.check_duplicates(
        db=db,
        project_id=project_id,
        request=check_request,
    )


@router.post(
    "/projects/{project_id}/issues/{issue_id}/mark-duplicate/{duplicate_of_id}",
    response_model=IssueResponse,
)
@limiter.limit("20/minute")
def mark_as_duplicate(
    request: Request,
    project_id: uuid.UUID,
    issue_id: uuid.UUID,
    duplicate_of_id: uuid.UUID,
    db: Session = Depends(get_database),
    current_user: User = Depends(get_current_user),
):
    """Mark an issue as a duplicate of another issue."""
    issue = IssueService.get_issue(db, issue_id)
    if issue is None or issue.project_id != project_id:
        raise HTTPException(status_code=404, detail="Issue not found")

    duplicate_of = IssueService.get_issue(db, duplicate_of_id)
    if duplicate_of is None or duplicate_of.project_id != project_id:
        raise HTTPException(status_code=404, detail="Duplicate target issue not found")

    if issue.author_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Only the issue author can mark it as duplicate",
        )

    return IssueService.mark_as_duplicate(db, issue_id, duplicate_of_id)
