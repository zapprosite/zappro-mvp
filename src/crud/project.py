"""CRUD helpers for Project entity."""

from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.project import Project
from src.schemas.project import ProjectCreate, ProjectUpdate


def get_projects(
    db: Session, owner_id: int, skip: int = 0, limit: int = 100
) -> List[Project]:
    return (
        db.query(Project)
        .filter(Project.owner_id == owner_id)
        .order_by(Project.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_project(
    db: Session, project_id: int, owner_id: Optional[int], is_admin: bool = False
) -> Optional[Project]:
    query = db.query(Project).filter(Project.id == project_id)
    if not is_admin:
        query = query.filter(Project.owner_id == owner_id)
    return query.first()


def create_project(db: Session, project: ProjectCreate, owner_id: int) -> Project:
    db_project = Project(**project.dict(), owner_id=owner_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def update_project(
    db: Session,
    project_id: int,
    project_update: ProjectUpdate,
    owner_id: int,
    is_admin: bool = False,
) -> Optional[Project]:
    db_project = get_project(db, project_id, owner_id, is_admin)
    if not db_project:
        return None

    for field, value in project_update.dict(exclude_unset=True).items():
        setattr(db_project, field, value)

    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(
    db: Session, project_id: int, owner_id: int, is_admin: bool = False
) -> bool:
    db_project = get_project(db, project_id, owner_id, is_admin)
    if not db_project:
        return False

    db.delete(db_project)
    db.commit()
    return True
