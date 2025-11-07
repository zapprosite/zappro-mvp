"""SQLAlchemy database setup with SQLite fallback for local dev/tests.

Reads DATABASE_URL from environment. If not set, defaults to
sqlite:///./zappro.db. Provides SessionLocal and get_db dependency.
"""

from __future__ import annotations

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./zappro.db")

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, future=True, echo=False, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)

Base = declarative_base()


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Create tables for SQLite/dev environments when needed.

    In production, prefer Alembic migrations. This convenience initializer
    enables local development without a running Postgres by creating tables
    when using SQLite.
    """
    # Import all models so SQLAlchemy metadata is populated before create_all.
    from .models import document  # noqa: F401
    from .models import material  # noqa: F401
    from .models import project  # noqa: F401
    from .models import task  # noqa: F401
    from .models import user  # noqa: F401

    if engine.url.get_backend_name() == "sqlite":
        Base.metadata.create_all(bind=engine)
