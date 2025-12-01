from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from src.models.user import UserRole


class UserBase(BaseModel):
    email: str
    name: str
    role: UserRole = UserRole.operador


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class User(UserBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: User


class TokenData(BaseModel):
    email: Optional[str] = None


class RefreshRequest(BaseModel):
    refresh_token: Optional[str] = None


class RefreshResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
