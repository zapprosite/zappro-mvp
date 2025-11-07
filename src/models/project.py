"""Project model and status enumeration."""

import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database import Base


class ProjectStatus(str, enum.Enum):
    planning = "planning"
    active = "active"
    completed = "completed"
    paused = "paused"


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String)
    status = Column(
        Enum(ProjectStatus),
        default=ProjectStatus.planning,
        server_default=ProjectStatus.planning.value,
        nullable=False,
        index=True,
    )
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
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

    owner = relationship("User", back_populates="projects")
    tasks = relationship(
        "Task",
        back_populates="project",
        cascade="all,delete-orphan",
    )
    materials = relationship(
        "Material",
        back_populates="project",
        cascade="all,delete-orphan",
    )
    documents = relationship(
        "Document",
        back_populates="project",
        cascade="all,delete-orphan",
    )
