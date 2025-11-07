"""CRUD helpers for document management with ownership rules."""

from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.document import Document
from src.models.project import Project
from src.models.task import Task
from src.schemas.document import DocumentCreate, DocumentUpdate


def _project_accessible(
    db: Session, project_id: int, owner_id: int, is_admin: bool
) -> Optional[Project]:
    query = db.query(Project).filter(Project.id == project_id)
    if not is_admin:
        query = query.filter(Project.owner_id == owner_id)
    return query.first()


def _task_accessible(
    db: Session, task_id: int, owner_id: int, is_admin: bool
) -> Optional[Task]:
    query = db.query(Task).filter(Task.id == task_id)
    if not is_admin:
        query = query.join(Project).filter(Project.owner_id == owner_id)
    return query.first()


def _validate_task_project(
    db: Session, task_id: Optional[int], project_id: int
) -> bool:
    if task_id is None:
        return True
    return (
        db.query(Task).filter(Task.id == task_id, Task.project_id == project_id).first()
        is not None
    )


def create_document(
    db: Session, document: DocumentCreate, owner_id: int, is_admin: bool
) -> Optional[Document]:
    project = _project_accessible(db, document.project_id, owner_id, is_admin)
    if not project or not _validate_task_project(
        db, document.task_id, document.project_id
    ):
        return None

    db_document = Document(**document.model_dump(mode="json"))
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


def get_document(
    db: Session, document_id: int, owner_id: int, is_admin: bool
) -> Optional[Document]:
    query = db.query(Document).filter(Document.id == document_id)
    if not is_admin:
        query = query.join(Project).filter(Project.owner_id == owner_id)
    return query.first()


def list_documents_by_project(
    db: Session, project_id: int, owner_id: int, is_admin: bool
) -> List[Document]:
    project = _project_accessible(db, project_id, owner_id, is_admin)
    if not project:
        return []

    return (
        db.query(Document)
        .filter(Document.project_id == project_id)
        .order_by(Document.created_at.desc())
        .all()
    )


def list_documents_by_task(
    db: Session, task_id: int, owner_id: int, is_admin: bool
) -> List[Document]:
    task = _task_accessible(db, task_id, owner_id, is_admin)
    if not task:
        return []

    return (
        db.query(Document)
        .filter(Document.task_id == task_id)
        .order_by(Document.created_at.desc())
        .all()
    )


def list_documents(db: Session, owner_id: int, is_admin: bool) -> List[Document]:
    query = db.query(Document).order_by(Document.created_at.desc())
    if not is_admin:
        query = query.join(Project).filter(Project.owner_id == owner_id)
    return query.all()


def update_document(
    db: Session,
    document_id: int,
    document_update: DocumentUpdate,
    owner_id: int,
    is_admin: bool,
) -> Optional[Document]:
    db_document = get_document(db, document_id, owner_id, is_admin)
    if not db_document:
        return None

    for field, value in document_update.model_dump(
        exclude_unset=True, mode="json"
    ).items():
        setattr(db_document, field, value)

    db.commit()
    db.refresh(db_document)
    return db_document


def delete_document(
    db: Session, document_id: int, owner_id: int, is_admin: bool
) -> bool:
    db_document = get_document(db, document_id, owner_id, is_admin)
    if not db_document:
        return False

    db.delete(db_document)
    db.commit()
    return True
