from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_database, get_current_user
from app.models.user import User
from app.schemas.project_document import (
    ProjectDocumentCreate,
    ProjectDocumentUpdate,
    ProjectDocumentResponse,
    ProjectDocumentListResponse,
)
from app.services.project_document_service import ProjectDocumentService

router = APIRouter(
    prefix="/projects/{project_id}/workspace/docs",
    tags=["Collaborative Workspace"],
)


@router.get("", response_model=ProjectDocumentListResponse)
def list_workspace_documents(
    project_id: UUID,
    db: Session = Depends(get_database),
):
    docs = ProjectDocumentService.list_project_documents(db, project_id)
    return ProjectDocumentListResponse(
        total=len(docs),
        documents=[ProjectDocumentResponse.model_validate(d) for d in docs],
    )


@router.post(
    "",
    response_model=ProjectDocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_workspace_document(
    project_id: UUID,
    payload: ProjectDocumentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_database),
):
    doc = ProjectDocumentService.create_document(
        db,
        project_id=project_id,
        user_id=current_user.id,
        title=payload.title,
        content=payload.content,
    )
    return ProjectDocumentResponse.model_validate(doc)


@router.get("/{doc_id}", response_model=ProjectDocumentResponse)
def get_workspace_document(
    project_id: UUID,
    doc_id: UUID,
    db: Session = Depends(get_database),
):
    doc = ProjectDocumentService.get_document(db, doc_id)
    return ProjectDocumentResponse.model_validate(doc)


@router.put("/{doc_id}", response_model=ProjectDocumentResponse)
def update_workspace_document(
    project_id: UUID,
    doc_id: UUID,
    payload: ProjectDocumentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_database),
):
    doc, is_conflict = ProjectDocumentService.update_document(
        db,
        doc_id=doc_id,
        user_id=current_user.id,
        title=payload.title,
        content=payload.content,
        base_version=payload.base_version,
    )
    res = ProjectDocumentResponse.model_validate(doc)
    res.conflict = is_conflict
    return res


@router.delete("/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workspace_document(
    project_id: UUID,
    doc_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_database),
):
    ProjectDocumentService.delete_document(db, doc_id)
    return None
