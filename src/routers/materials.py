"""Materials router exposing CRUD endpoints with RBAC checks."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from src.crud import material as material_crud
from src.database import get_db
from src.dependencies import require_role
from src.models.material import Material as MaterialModel
from src.models.project import Project
from src.models.user import User, UserRole
from src.schemas.material import Material as MaterialSchema
from src.schemas.material import MaterialCreate, MaterialUpdate
from src.utils.auth import get_current_user

router = APIRouter(tags=["materials"])


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


def _resolve_material_or_error(
    *,
    db: Session,
    material_id: int,
    current_user: User,
) -> MaterialModel:
    material = material_crud.get_material(
        db,
        material_id=material_id,
        owner_id=current_user.id,
        is_admin=_is_admin(current_user),
    )
    if material:
        return material

    exists = db.query(MaterialModel).filter(MaterialModel.id == material_id).first()
    if not exists:
        raise HTTPException(status_code=404, detail="Material not found")
    _ensure_project_access(db, exists.project_id, current_user)
    return exists


@router.post(
    "/materials",
    response_model=MaterialSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_material_endpoint(
    material: MaterialCreate,
    current_user: User = Depends(require_role([UserRole.admin, UserRole.gestor])),
    db: Session = Depends(get_db),
) -> MaterialSchema:
    """Create a material for a project.

    Example:
        POST /api/v1/materials {"name": "Steel Beam", "project_id": 1, "stock": 25}
    """

    _ensure_project_access(db, material.project_id, current_user)

    db_material = material_crud.create_material(
        db,
        material=material,
        owner_id=current_user.id,
        is_admin=_is_admin(current_user),
    )
    if not db_material:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_material


@router.get("/materials", response_model=List[MaterialSchema])
def list_materials_endpoint(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[MaterialSchema]:
    """List all materials accessible to the authenticated user.

    Example:
        GET /api/v1/materials
    """

    return material_crud.list_materials(
        db, owner_id=current_user.id, is_admin=_is_admin(current_user)
    )


@router.get("/projects/{project_id}/materials", response_model=List[MaterialSchema])
def list_project_materials(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[MaterialSchema]:
    """List materials for a specific project.

    Example:
        GET /api/v1/projects/1/materials
    """

    _ensure_project_access(db, project_id, current_user)
    return material_crud.list_materials_by_project(
        db,
        project_id=project_id,
        owner_id=current_user.id,
        is_admin=_is_admin(current_user),
    )


@router.get("/materials/{material_id}", response_model=MaterialSchema)
def get_material_endpoint(
    material_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MaterialSchema:
    """Retrieve a material by id.

    Example:
        GET /api/v1/materials/10
    """

    return _resolve_material_or_error(
        db=db,
        material_id=material_id,
        current_user=current_user,
    )


@router.put("/materials/{material_id}", response_model=MaterialSchema)
def update_material_endpoint(
    material_id: int,
    material_update: MaterialUpdate,
    current_user: User = Depends(require_role([UserRole.admin, UserRole.gestor])),
    db: Session = Depends(get_db),
) -> MaterialSchema:
    """Update a material's stock or supplier information.

    Example:
        PUT /api/v1/materials/10 {"stock": 40}
    """

    _ = _resolve_material_or_error(
        db=db, material_id=material_id, current_user=current_user
    )
    updated = material_crud.update_material(
        db,
        material_id=material_id,
        material_update=material_update,
        owner_id=current_user.id,
        is_admin=_is_admin(current_user),
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Material not found")
    return updated


@router.delete(
    "/materials/{material_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def delete_material_endpoint(
    material_id: int,
    current_user: User = Depends(require_role([UserRole.admin, UserRole.gestor])),
    db: Session = Depends(get_db),
) -> Response:
    """Delete a material.

    Example:
        DELETE /api/v1/materials/10
    """

    _ = _resolve_material_or_error(
        db=db, material_id=material_id, current_user=current_user
    )
    success = material_crud.delete_material(
        db,
        material_id=material_id,
        owner_id=current_user.id,
        is_admin=_is_admin(current_user),
    )
    if not success:
        raise HTTPException(status_code=404, detail="Material not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
