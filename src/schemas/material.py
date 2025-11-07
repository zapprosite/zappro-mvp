"""Pydantic schemas for Material endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MaterialBase(BaseModel):
    name: str
    stock: int = 0
    supplier: Optional[str] = None


class MaterialCreate(MaterialBase):
    project_id: int


class MaterialUpdate(BaseModel):
    name: Optional[str] = None
    stock: Optional[int] = None
    supplier: Optional[str] = None


class Material(MaterialBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
