"""Shared FastAPI dependencies."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Callable, Set

from fastapi import Depends, HTTPException, status

from src.models.user import User, UserRole
from src.utils.auth import get_current_user


def require_role(required_roles: Sequence[str | UserRole]) -> Callable[..., User]:
    """Ensure the current user has one of the expected roles."""

    allowed: Set[str] = {
        role.value if isinstance(role, UserRole) else role for role in required_roles
    }

    async def _dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role.value not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user

    return _dependency
