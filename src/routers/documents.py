"""Documents router providing CRUD operations scoped by project ownership."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from src.crud import document as document_crud
from src.database import get_db
from src.models.document import Document as DocumentModel
from src.models.project import Project
from src.models.task import Task
from src.models.user import User, UserRole
from src.dependencies import require_role
from src.schemas.document import Document as DocumentSchema
from src.schemas.document import DocumentCreate, DocumentUpdate
from src.utils.auth import get_current_user

router = APIRouter(tags=["documents"])


def _is_admin(user: User) -> bool:
    return user.role == UserRole.admin


def _ensure_project_access(
    db: Session,
    project_id: int,
    current_user: User,
) -> Project:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if not _is_admin(current_user) and project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access project")
    return project


def _ensure_task_access(
    db: Session,
    task_id: int,
    current_user: User,
) -> Task:
    task = (
        db.query(Task)
        .join(Project)
        .filter(Task.id == task_id)
        .first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not _is_admin(current_user) and task.project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access task")
    return task


def _resolve_document_or_error(
    *,
    db: Session,
    document_id: int,
    current_user: User,
) -> DocumentModel:
    document = document_crud.get_document(
        db,
        document_id=document_id,
        owner_id=current_user.id,
        is_admin=_is_admin(current_user),
    )
    if document:
        return document

    exists = db.query(DocumentModel).filter(DocumentModel.id == document_id).first()
    if not exists:
        raise HTTPException(status_code=404, detail="Document not found")
    _ensure_project_access(db, exists.project_id, current_user)
    return exists


@router.post(
    "/documents",
    response_model=DocumentSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_document_endpoint(
    document: DocumentCreate,
    current_user: User = Depends(require_role([UserRole.admin, UserRole.gestor])),
    db: Session = Depends(get_db),
) -> DocumentSchema:
    """Create a document associated with a project or task.

    Example:
        POST /api/v1/documents {"project_id": 1, "url": "https://example.com/doc.pdf", "type": "contract"}
    """

    _ensure_project_access(db, document.project_id, current_user)
    if document.task_id is not None:
        task = _ensure_task_access(db, document.task_id, current_user)
        if task.project_id != document.project_id:
            raise HTTPException(
                status_code=400, detail="Task must belong to the provided project"
            )

    db_document = document_crud.create_document(
        db,
        document=document,
        owner_id=current_user.id,
        is_admin=_is_admin(current_user),
    )
    if not db_document:
        raise HTTPException(status_code=404, detail="Project or task not found")
    return db_document


@router.get("/documents", response_model=List[DocumentSchema])
def list_documents_endpoint(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[DocumentSchema]:
    """List all documents accessible to the authenticated user.

    Example:
        GET /api/v1/documents
    """

    return document_crud.list_documents(
        db, owner_id=current_user.id, is_admin=_is_admin(current_user)
    )


@router.get("/projects/{project_id}/documents", response_model=List[DocumentSchema])
def list_project_documents(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[DocumentSchema]:
    """List documents for a specific project.

    Example:
        GET /api/v1/projects/7/documents
    """

    _ensure_project_access(db, project_id, current_user)
    return document_crud.list_documents_by_project(
        db,
        project_id=project_id,
        owner_id=current_user.id,
        is_admin=_is_admin(current_user),
    )


@router.get("/tasks/{task_id}/documents", response_model=List[DocumentSchema])
def list_task_documents(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[DocumentSchema]:
    """List documents associated with a task.

    Example:
        GET /api/v1/tasks/3/documents
    """

    _ensure_task_access(db, task_id, current_user)
    return document_crud.list_documents_by_task(
        db,
        task_id=task_id,
        owner_id=current_user.id,
        is_admin=_is_admin(current_user),
    )


@router.get("/documents/{document_id}", response_model=DocumentSchema)
def get_document_endpoint(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> DocumentSchema:
    """Retrieve a document by id.

    Example:
        GET /api/v1/documents/12
    """

    return _resolve_document_or_error(
        db=db,
        document_id=document_id,
        current_user=current_user,
    )


@router.put("/documents/{document_id}", response_model=DocumentSchema)
def update_document_endpoint(
    document_id: int,
    document_update: DocumentUpdate,
    current_user: User = Depends(require_role([UserRole.admin, UserRole.gestor])),
    db: Session = Depends(get_db),
) -> DocumentSchema:
    """Update document metadata such as URL or description.

    Example:
        PUT /api/v1/documents/12 {"url": "https://example.com/new.pdf"}
    """

    _ = _resolve_document_or_error(db=db, document_id=document_id, current_user=current_user)
    updated = document_crud.update_document(
        db,
        document_id=document_id,
        document_update=document_update,
        owner_id=current_user.id,
        is_admin=_is_admin(current_user),
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Document not found")
    return updated


@router.delete(
    "/documents/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def delete_document_endpoint(
    document_id: int,
    current_user: User = Depends(require_role([UserRole.admin, UserRole.gestor])),
    db: Session = Depends(get_db),
) -> Response:
    """Delete a document.

    Example:
        DELETE /api/v1/documents/12
    """

    _ = _resolve_document_or_error(db=db, document_id=document_id, current_user=current_user)
    success = document_crud.delete_document(
        db,
        document_id=document_id,
        owner_id=current_user.id,
        is_admin=_is_admin(current_user),
    )
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
