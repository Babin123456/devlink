from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status

# pyrefly: ignore [missing-import]

# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session

from app.dependencies import get_database, get_current_user, require_project_permission
from app.middleware.rate_limit import limiter, PROJECT_LIMIT
from app.models.user import User
from app.schemas.duplicate_detection import (
    DuplicateProjectCheckRequest,
    DuplicateProjectCheckResponse,
)
from app.schemas.project import (
    ProjectCreate,
    ProjectResponse,
    ProjectStatsResponse,
    ProjectUpdate,
    SimilarProjectWarning,
)
from app.services.project_service import ProjectService
from app.core.cache import cached

from app.middleware.idempotency import IdempotentRoute

router = APIRouter(
    tags=["Projects"],
    route_class=IdempotentRoute,
)


@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit(PROJECT_LIMIT)
def create_project(
    request: Request,
    project: ProjectCreate,
    db: Session = Depends(get_database),
    current_user: User = Depends(get_current_user),
):

    if ProjectService.get_by_slug(db, project.slug):
        raise HTTPException(
            status_code=400,
            detail="Project slug already exists",
        )

    new_project = ProjectService.create_project(
        db=db,
        owner_id=current_user.id,
        project=project,
    )

    from app.services.audit_log_service import AuditLogService
    from app.models.audit_log import AuditAction

    AuditLogService.create_log(
        db=db,
        actor_id=current_user.id,
        action=AuditAction.PROJECT_CREATED,
        entity_type="project",
        entity_id=str(new_project.id),
        project_id=new_project.id,
        new_values=project.model_dump(exclude_unset=True),
    )

    return new_project


@router.post(
    "/check-duplicate",
    response_model=DuplicateProjectCheckResponse,
    summary="Check AI-based duplicate projects",
    description="Compare project title, description, and tags against existing projects using semantic embedding and token similarity.",
)
def check_duplicate_project(
    req: DuplicateProjectCheckRequest,
    db: Session = Depends(get_database),
) -> DuplicateProjectCheckResponse:
    from app.services.duplicate_detection_service import DuplicateDetectionService
    return DuplicateDetectionService.find_duplicate_projects(
        db,
        title=req.title,
        description=req.description,
        tags=req.tags,
        threshold=req.similarity_threshold,
        limit=req.limit,
    )


@router.post(
    "/check-similarity",
    response_model=list[SimilarProjectWarning],
)
def check_project_similarity(
    project: ProjectCreate,
    db: Session = Depends(get_database),
    current_user: User = Depends(get_current_user),
):
    return ProjectService.find_similar_projects(
        db,
        title=project.title,
        description=project.description,
    )


from app.dependencies import (
    get_database,
    get_current_user,
    get_optional_current_user,
    require_project_permission,
)
from app.schemas.project_analytics import ProjectAnalyticsResponse
from app.services.project_analytics_service import ProjectAnalyticsService


@router.get(
    "/{project_id}/analytics",
    response_model=ProjectAnalyticsResponse,
    summary="Get Project View Analytics",
)
def get_project_analytics(
    project_id: uuid.UUID,
    days: int = Query(
        30, ge=1, le=365, description="Number of days for daily views breakdown"
    ),
    db: Session = Depends(get_database),
):
    """
    Get project view analytics including total views, unique viewers, and daily views.
    """
    return ProjectAnalyticsService.get_analytics(db, project_id, days=days)


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
)
@cached(ttl=60, key_prefix="projects:get")
def get_project(
    request: Request,
    project_id: uuid.UUID,
    db: Session = Depends(get_database),
    current_user: User | None = Depends(get_optional_current_user),
):

    project = ProjectService.get_project(
        db,
        project_id,
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    viewer_id = current_user.id if current_user else None

    ProjectAnalyticsService.record_view(
        db=db,
        project_id=project_id,
        viewer_id=viewer_id,
        ip_address=ip_address,
        user_agent=user_agent,
    )

    return project


@router.get(
    "/slug/{slug}",
    response_model=ProjectResponse,
)
@cached(ttl=60, key_prefix="projects:slug")
def get_project_by_slug(
    request: Request,
    slug: str,
    db: Session = Depends(get_database),
    current_user: User | None = Depends(get_optional_current_user),
):

    project = ProjectService.get_by_slug(
        db,
        slug,
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    viewer_id = current_user.id if current_user else None

    ProjectAnalyticsService.record_view(
        db=db,
        project_id=project.id,
        viewer_id=viewer_id,
        ip_address=ip_address,
        user_agent=user_agent,
    )

    return project


@router.get(
    "/",
    response_model=list[ProjectResponse],
)
@cached(ttl=120, key_prefix="projects:list")
def list_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    language: str | None = Query(None),
    experience: str | None = Query(None),
    remote: bool | None = Query(None),
    paid: bool | None = Query(None),
    opensource: bool | None = Query(None),
    tech: str | None = Query(None),
    db: Session = Depends(get_database),
):

    return ProjectService.list_projects(
        db,
        skip=skip,
        limit=limit,
        language=language,
        experience=experience,
        remote=remote,
        paid=paid,
        opensource=opensource,
        tech=tech,
    )


@router.get(
    "/me/list",
    response_model=list[ProjectResponse],
)
def my_projects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_database),
):

    return ProjectService.list_owner_projects(
        db,
        current_user.id,
    )


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
)
@limiter.limit("30/minute")
def update_project(
    request: Request,
    project_id: uuid.UUID,
    project: ProjectUpdate,
    db: Session = Depends(get_database),
    current_user: User = Depends(require_project_permission("project:update")),
):

    db_project = ProjectService.get_project(
        db,
        project_id,
    )

    if db_project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    old_values = {}
    for key in project.model_dump(exclude_unset=True).keys():
        old_values[key] = getattr(db_project, key, None)

    updated_project = ProjectService.update_project(
        db,
        db_project,
        project,
    )

    from app.services.audit_log_service import AuditLogService
    from app.models.audit_log import AuditAction

    AuditLogService.create_log(
        db=db,
        actor_id=current_user.id,
        action=AuditAction.PROJECT_UPDATED,
        entity_type="project",
        entity_id=str(updated_project.id),
        project_id=updated_project.id,
        old_values=old_values,
        new_values=project.model_dump(exclude_unset=True),
    )

    return updated_project


@router.patch(
    "/{project_id}/archive",
    response_model=ProjectResponse,
)
@limiter.limit("20/minute")
def archive_project(
    request: Request,
    project_id: uuid.UUID,
    db: Session = Depends(get_database),
    current_user: User = Depends(require_project_permission("project:archive")),
):

    project = ProjectService.get_project(
        db,
        project_id,
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    archived_project = ProjectService.archive_project(
        db,
        project,
    )

    from app.services.audit_log_service import AuditLogService
    from app.models.audit_log import AuditAction

    AuditLogService.create_log(
        db=db,
        actor_id=current_user.id,
        action=AuditAction.PROJECT_ARCHIVED,
        entity_type="project",
        entity_id=str(archived_project.id),
        project_id=archived_project.id,
    )

    return archived_project


@router.patch(
    "/{project_id}/restore",
    response_model=ProjectResponse,
)
@limiter.limit("20/minute")
def restore_project(
    request: Request,
    project_id: uuid.UUID,
    db: Session = Depends(get_database),
    current_user: User = Depends(require_project_permission("project:restore")),
):

    project = ProjectService.get_project(
        db,
        project_id,
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    restored_project = ProjectService.restore_project(
        db,
        project,
    )

    from app.services.audit_log_service import AuditLogService
    from app.models.audit_log import AuditAction

    AuditLogService.create_log(
        db=db,
        actor_id=current_user.id,
        action=AuditAction.PROJECT_RESTORED,
        entity_type="project",
        entity_id=str(restored_project.id),
        project_id=restored_project.id,
    )

    return restored_project


@router.patch(
    "/{project_id}/feature",
    response_model=ProjectResponse,
)
@limiter.limit("20/minute")
def feature_project(
    request: Request,
    project_id: uuid.UUID,
    db: Session = Depends(get_database),
):

    project = ProjectService.get_project(
        db,
        project_id,
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    return ProjectService.feature_project(
        db,
        project,
    )


@router.post(
    "/{project_id}/star",
)
@limiter.limit("30/minute")
def star_project(
    request: Request,
    project_id: uuid.UUID,
    db: Session = Depends(get_database),
):

    project = ProjectService.get_project(
        db,
        project_id,
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    ProjectService.increment_stars(
        db,
        project,
    )

    return {
        "message": "Project starred",
    }


@router.get(
    "/{project_id}/stats",
    response_model=ProjectStatsResponse,
)
def get_project_stats(
    project_id: uuid.UUID,
    db: Session = Depends(get_database),
    current_user: User = Depends(get_current_user),
):
    project = ProjectService.get_project(db, project_id)

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")

    return ProjectService.get_project_stats(db, project_id)


@router.delete(
    "/{project_id}/star",
)
@limiter.limit("30/minute")
def unstar_project(
    request: Request,
    project_id: uuid.UUID,
    db: Session = Depends(get_database),
):

    project = ProjectService.get_project(
        db,
        project_id,
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    ProjectService.decrement_stars(
        db,
        project,
    )

    return {
        "message": "Project unstarred",
    }


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@limiter.limit("20/minute")
def delete_project(
    request: Request,
    project_id: uuid.UUID,
    db: Session = Depends(get_database),
    current_user: User = Depends(require_project_permission("project:delete")),
):

    project = ProjectService.get_project(
        db,
        project_id,
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    ProjectService.soft_delete_project(
        db,
        project,
        deleted_by_id=current_user.id,
    )

    from app.services.audit_log_service import AuditLogService
    from app.models.audit_log import AuditAction

    AuditLogService.create_log(
        db=db,
        actor_id=current_user.id,
        action=AuditAction.PROJECT_DELETED,
        entity_type="project",
        entity_id=str(project_id),
        project_id=project_id,
    )


@router.post(
    "/{project_id}/invite/{user_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=dict,
)
def invite_user(
    project_id: uuid.UUID,
    user_id: uuid.UUID,
    db: Session = Depends(get_database),
    current_user: User = Depends(get_current_user),
):

    project = ProjectService.get_project(db, project_id)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Only the project owner can invite members",
        )

    from app.models.project_member import ProjectMember, MemberRole
    from sqlalchemy import and_, select

    existing_member = db.scalar(
        select(ProjectMember).where(
            and_(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == user_id,
            )
        )
    )
    if existing_member:
        raise HTTPException(
            status_code=400,
            detail="User is already invited or a member of the project",
        )

    new_member = ProjectMember(
        project_id=project_id,
        user_id=user_id,
        role=MemberRole.MEMBER,
        is_active=False,
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    from app.models.notification import NotificationType
    from app.schemas.notification import NotificationCreate
    from app.services.notification_service import NotificationService

    notification_data = NotificationCreate(
        recipient_id=user_id,
        type=NotificationType.PROJECT_INVITE,
        title="Project Invitation",
        message=f"You have been invited to join the project '{project.title}'.",
        action_url=f"/projects/{project_id}",
        project_id=project_id,
    )
    NotificationService.create_notification(
        db=db,
        recipient_id=user_id,
        sender_id=current_user.id,
        notification=notification_data,
    )

    from app.services.audit_log_service import AuditLogService
    from app.models.audit_log import AuditAction

    AuditLogService.create_log(
        db=db,
        actor_id=current_user.id,
        action=AuditAction.INVITATION_SENT,
        entity_type="project",
        entity_id=str(project_id),
        project_id=project_id,
        target_user_id=user_id,
    )

    return {"message": "User invited successfully"}


@router.delete(
    "/{project_id}/soft",
    status_code=status.HTTP_204_NO_CONTENT,
)
def soft_delete_project(
    project_id: uuid.UUID,
    db: Session = Depends(get_database),
    current_user: User = Depends(get_current_user),
):
    project = ProjectService.get_project(db, project_id)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    if project.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Permission denied",
        )

    ProjectService.soft_delete_project(
        db,
        project,
        deleted_by_id=current_user.id,
    )


@router.patch(
    "/{project_id}/restore-soft-delete",
    response_model=ProjectResponse,
)
def restore_project_soft_delete(
    project_id: uuid.UUID,
    db: Session = Depends(get_database),
    current_user: User = Depends(get_current_user),
):
    project = ProjectService.get_project_including_deleted(db, project_id)

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    if project.deleted_at is None:
        raise HTTPException(
            status_code=400,
            detail="Project is not deleted",
        )

    if project.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Permission denied",
        )

    return ProjectService.restore_soft_deleted_project(
        db,
        project,
    )


@router.delete(
    "/{project_id}/hard",
    status_code=status.HTTP_204_NO_CONTENT,
)
def hard_delete_project(
    project_id: uuid.UUID,
    db: Session = Depends(get_database),
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Only admins can permanently delete projects",
        )

    project = ProjectService.get_project_including_deleted(db, project_id)

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    ProjectService.hard_delete_project(
        db,
        project,
    )
