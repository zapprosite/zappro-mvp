"""CRUD helpers for tasks within a project."""

from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.project import Project
from src.models.task import Task
from src.schemas.task import TaskCreate, TaskUpdate


def _assert_project_owner(
    db: Session, project_id: int, owner_id: int
) -> Optional[Project]:
    return (
        db.query(Project)
        .filter(Project.id == project_id, Project.owner_id == owner_id)
        .first()
    )


def get_tasks_by_project(db: Session, project_id: int, owner_id: int) -> List[Task]:
    project = _assert_project_owner(db, project_id, owner_id)
    if not project:
        return []
    return (
        db.query(Task)
        .filter(Task.project_id == project_id)
        .order_by(Task.created_at)
        .all()
    )


def get_task(db: Session, task_id: int, owner_id: int) -> Optional[Task]:
    return (
        db.query(Task)
        .join(Project)
        .filter(Task.id == task_id, Project.owner_id == owner_id)
        .first()
    )


def create_task(db: Session, task: TaskCreate, owner_id: int) -> Optional[Task]:
    project = _assert_project_owner(db, task.project_id, owner_id)
    if not project:
        return None

    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(
    db: Session, task_id: int, task_update: TaskUpdate, owner_id: int
) -> Optional[Task]:
    db_task = get_task(db, task_id, owner_id)
    if not db_task:
        return None

    for field, value in task_update.model_dump(exclude_unset=True).items():
        setattr(db_task, field, value)

    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int, owner_id: int) -> bool:
    db_task = get_task(db, task_id, owner_id)
    if not db_task:
        return False

    db.delete(db_task)
    db.commit()
    return True
