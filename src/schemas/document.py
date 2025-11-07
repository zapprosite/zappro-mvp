"""Pydantic schemas for Document endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl


class DocumentBase(BaseModel):
    url: HttpUrl
    type: str
    description: Optional[str] = None
    task_id: Optional[int] = None


class DocumentCreate(DocumentBase):
    project_id: int


class DocumentUpdate(BaseModel):
    url: Optional[HttpUrl] = None
    description: Optional[str] = None
    type: Optional[str] = None


class Document(DocumentBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
