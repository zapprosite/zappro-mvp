from __future__ import annotations

import enum

from sqlalchemy import Column, DateTime, Enum, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database import Base


class UserRole(str, enum.Enum):
    admin = "admin"
    gestor = "gestor"
    operador = "operador"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(
        Enum(UserRole),
        default=UserRole.operador,
        server_default=UserRole.operador.value,
        nullable=False,
    )
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    projects = relationship(
        "Project",
        back_populates="owner",
        cascade="all,delete-orphan",
    )
    assigned_tasks = relationship("Task", back_populates="assignee")
