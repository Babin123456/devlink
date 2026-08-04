from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.issue import DuplicateSuggestion, Issue, IssueStatus
from app.schemas.issue import (
    DuplicateCheckRequest,
    DuplicateCheckResponse,
    DuplicateSuggestionResponse,
    IssueCreate,
    IssueResponse,
    IssueUpdate,
)
from app.services.duplicate_detection_service import DuplicateDetectionService
from app.services.issue_difficulty_service import IssueDifficultyService


class IssueService:
    """
    Business logic for Issue operations.
    """

    @staticmethod
    def create_issue(
        db: Session,
        project_id: uuid.UUID,
        author_id: uuid.UUID,
        issue: IssueCreate,
    ) -> Issue:
        """
        Create a new issue, estimate its difficulty, and generate its
        embedding for future duplicate detection.
        """
        # Run AI difficulty estimation
        difficulty_result = IssueDifficultyService.estimate_difficulty(
            title=issue.title,
            description=issue.description,
            labels=issue.labels,
        )

        # Generate embedding for the issue text
        embedding_text = f"{issue.title}\n\n{issue.description}"
        embedding = DuplicateDetectionService.generate_embedding(embedding_text)

        db_issue = Issue(
            project_id=project_id,
            author_id=author_id,
            title=issue.title,
            description=issue.description,
            priority=issue.priority,
            labels=issue.labels,
            difficulty=difficulty_result.difficulty,
            difficulty_confidence=difficulty_result.confidence,
            difficulty_manual_override=False,
            embedding=(
                DuplicateDetectionService.embedding_to_json(embedding)
                if embedding
                else None
            ),
            is_duplicate_checked=False,
        )

        db.add(db_issue)
        db.flush()
        db.refresh(db_issue)

        return db_issue

    @staticmethod
    def get_issue(
        db: Session,
        issue_id: uuid.UUID,
    ) -> Issue | None:
        """Get a single issue by ID with author loaded."""
        stmt = (
            select(Issue)
            .options(selectinload(Issue.author))
            .where(Issue.id == issue_id)
        )
        return db.scalar(stmt)

    @staticmethod
    def list_project_issues(
        db: Session,
        project_id: uuid.UUID,
        status: IssueStatus | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Issue]:
        """List issues for a project with optional status filter."""
        stmt = (
            select(Issue)
            .options(selectinload(Issue.author))
            .where(Issue.project_id == project_id)
        )

        if status:
            stmt = stmt.where(Issue.status == status)

        stmt = stmt.order_by(Issue.created_at.desc()).offset(skip).limit(limit)

        return list(db.scalars(stmt))

    @staticmethod
    def update_issue(
        db: Session,
        db_issue: Issue,
        issue: IssueUpdate,
    ) -> Issue:
        """Update an issue."""
        data = issue.model_dump(exclude_unset=True)

        for key, value in data.items():
            setattr(db_issue, key, value)

        db.flush()
        db.refresh(db_issue)

        return db_issue

    @staticmethod
    def delete_issue(
        db: Session,
        db_issue: Issue,
    ) -> None:
        """Delete an issue."""
        db.delete(db_issue)
        db.flush()

    @staticmethod
    def check_duplicates(
        db: Session,
        project_id: uuid.UUID,
        request: DuplicateCheckRequest,
    ) -> DuplicateCheckResponse:
        """
        Check for duplicate issues in a project.

        Uses AI embeddings when available and falls back to keyword
        similarity otherwise. Results are returned transiently and are
        never persisted to the database.

        Args:
            db: Database session
            project_id: Project to search within
            request: Contains title, description, and threshold

        Returns:
            DuplicateCheckResponse with suggestions and metadata
        """
        embedding_text = f"{request.title}\n\n{request.description}"
        embedding = DuplicateDetectionService.generate_embedding(embedding_text)

        # Find similar issues (embedding similarity with keyword fallback)
        similar_issues = DuplicateDetectionService.find_duplicates(
            db=db,
            project_id=project_id,
            embedding=embedding,
            text=embedding_text,
            threshold=request.threshold,
            limit=5,
        )

        checked_count = (
            db.scalar(
                select(func.count()).select_from(Issue).where(
                    Issue.project_id == project_id
                )
            )
            or 0
        )

        # Build transient suggestion responses
        now = datetime.now(timezone.utc)
        suggestions: list[DuplicateSuggestionResponse] = []
        for result in similar_issues:
            issue = result["issue"]
            suggestions.append(
                DuplicateSuggestionResponse(
                    id=uuid.uuid4(),
                    source_issue_id=uuid.uuid4(),
                    duplicate_issue_id=issue.id,
                    similarity_score=result["similarity_score"],
                    created_at=now,
                    issue=IssueResponse.model_validate(issue),
                )
            )

        return DuplicateCheckResponse(
            has_duplicates=len(suggestions) > 0,
            suggestions=suggestions,
            checked_count=checked_count,
            threshold=request.threshold,
        )

    @staticmethod
    def get_duplicate_suggestions(
        db: Session,
        issue_id: uuid.UUID,
    ) -> list[DuplicateSuggestion]:
        """Get duplicate suggestions for a specific issue."""
        stmt = (
            select(DuplicateSuggestion)
            .options(selectinload(DuplicateSuggestion.duplicate_issue))
            .where(
                DuplicateSuggestion.source_issue_id == issue_id,
            )
            .order_by(DuplicateSuggestion.similarity_score.desc())
        )
        return list(db.scalars(stmt))

    @staticmethod
    def mark_as_duplicate(
        db: Session,
        issue_id: uuid.UUID,
        duplicate_of_id: uuid.UUID,
    ) -> Issue:
        """Mark an issue as a duplicate of another issue."""
        db_issue = db.get(Issue, issue_id)
        if not db_issue:
            raise ValueError("Issue not found")

        db_issue.status = IssueStatus.DUPLICATE
        db_issue.is_duplicate_checked = True

        # Persist the relationship so it can be surfaced later
        existing = db.scalar(
            select(DuplicateSuggestion).where(
                DuplicateSuggestion.source_issue_id == issue_id,
                DuplicateSuggestion.duplicate_issue_id == duplicate_of_id,
            )
        )
        if not existing:
            db.add(
                DuplicateSuggestion(
                    source_issue_id=issue_id,
                    duplicate_issue_id=duplicate_of_id,
                    similarity_score=1.0,
                )
            )

        db.flush()
        db.refresh(db_issue)

        return db_issue
