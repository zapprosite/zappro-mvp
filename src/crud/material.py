"""CRUD helpers for Material entity with ownership checks."""

from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.material import Material
from src.models.project import Project
from src.schemas.material import MaterialCreate, MaterialUpdate


def _project_accessible(
    db: Session, project_id: int, owner_id: int, is_admin: bool
) -> Optional[Project]:
    query = db.query(Project).filter(Project.id == project_id)
    if not is_admin:
        query = query.filter(Project.owner_id == owner_id)
    return query.first()


def create_material(
    db: Session, material: MaterialCreate, owner_id: int, is_admin: bool
) -> Optional[Material]:
    project = _project_accessible(db, material.project_id, owner_id, is_admin)
    if not project:
        return None

    db_material = Material(**material.dict())
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material


def get_material(
    db: Session, material_id: int, owner_id: int, is_admin: bool
) -> Optional[Material]:
    query = db.query(Material).filter(Material.id == material_id)
    if not is_admin:
        query = query.join(Project).filter(Project.owner_id == owner_id)
    return query.first()


def list_materials_by_project(
    db: Session, project_id: int, owner_id: int, is_admin: bool
) -> List[Material]:
    project = _project_accessible(db, project_id, owner_id, is_admin)
    if not project:
        return []
    return (
        db.query(Material)
        .filter(Material.project_id == project_id)
        .order_by(Material.created_at.desc())
        .all()
    )


def list_materials(db: Session, owner_id: int, is_admin: bool) -> List[Material]:
    query = db.query(Material).order_by(Material.created_at.desc())
    if not is_admin:
        query = query.join(Project).filter(Project.owner_id == owner_id)
    return query.all()


def update_material(
    db: Session,
    material_id: int,
    material_update: MaterialUpdate,
    owner_id: int,
    is_admin: bool,
) -> Optional[Material]:
    db_material = get_material(db, material_id, owner_id, is_admin)
    if not db_material:
        return None

    for field, value in material_update.dict(exclude_unset=True).items():
        setattr(db_material, field, value)

    db.commit()
    db.refresh(db_material)
    return db_material


def delete_material(
    db: Session, material_id: int, owner_id: int, is_admin: bool
) -> bool:
    db_material = get_material(db, material_id, owner_id, is_admin)
    if not db_material:
        return False

    db.delete(db_material)
    db.commit()
    return True
