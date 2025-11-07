"""ZapPro API entrypoint with security hardening middleware."""

import logging
from typing import Any, Dict, List

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette.middleware import Middleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from . import __version__
from .config import Settings, get_settings
from .crud import project as project_crud
from .crud import task as task_crud
from .database import get_db, init_db
from .models.user import UserRole
from .routers import auth as auth_router
from .routers import documents, materials
from .schemas.project import Project as ProjectSchema
from .schemas.project import ProjectCreate, ProjectUpdate
from .schemas.task import Task as TaskSchema
from .schemas.task import TaskCreate, TaskUpdate
from .security import (
    FixedWindowRateLimiter,
    RequestIdTracker,
    build_request_id,
    resolve_client_ip,
)
from .utils.auth import get_current_user

LOGGER = logging.getLogger("zappro.api")


def _build_middlewares(settings: Settings) -> list[Middleware]:
    middlewares: list[Middleware] = []

    if settings.enable_cors:
        middlewares.append(
            Middleware(
                CORSMiddleware,
                allow_origins=settings.cors.allow_origins,
                allow_credentials=settings.cors.allow_credentials,
                allow_methods=settings.cors.allow_methods,
                allow_headers=settings.cors.allow_headers,
                expose_headers=settings.cors.expose_headers,
            )
        )

    middlewares.append(
        Middleware(
            TrustedHostMiddleware,
            allowed_hosts=settings.allowed_hosts,
        )
    )

    return middlewares


def create_app(settings: Settings | None = None) -> FastAPI:
    """Instantiate and configure the FastAPI application."""
    settings = settings or get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=__version__,
        middleware=_build_middlewares(settings),
    )

    app.include_router(materials.router, prefix="/api/v1")
    app.include_router(documents.router, prefix="/api/v1")
    app.include_router(auth_router.router)

    if settings.rate_limit.backend != "memory":
        LOGGER.warning(
            "Rate limit backend '%s' not implemented; falling back to memory store.",
            settings.rate_limit.backend,
        )

    limiter = FixedWindowRateLimiter(
        max_requests=settings.rate_limit.max_requests,
        window_seconds=settings.rate_limit.window_seconds,
        ttl_seconds=settings.rate_limit.ttl_seconds,
        max_entries=settings.rate_limit.max_entries,
    )
    request_id_tracker = RequestIdTracker(
        ttl_seconds=settings.request_id_ttl_seconds,
        max_entries=settings.request_id_max_entries,
    )

    @app.middleware("http")
    async def add_security_headers(request: Request, call_next: Any):
        header_lookup: Dict[str, str] = {
            key.lower(): value for key, value in request.headers.items()
        }
        client_ip = resolve_client_ip(
            request.client.host if request.client else None,
            header_lookup,
            trusted_proxies=settings.trusted_proxies,
            client_ip_header=settings.client_ip_header.lower(),
        )

        allowed, retry_after = limiter.allow(client_ip)
        if not allowed:
            LOGGER.warning("Rate limit exceeded for client %s", client_ip)
            return JSONResponse(
                status_code=429,
                content={"detail": "Too Many Requests"},
                headers={"Retry-After": f"{retry_after:.0f}"},
            )

        incoming_request_id = request.headers.get(settings.request_id_header)

        trusted_source = (
            settings.trust_client_request_id
            and incoming_request_id
            and client_ip in settings.request_id_trusted_hosts
        )

        if incoming_request_id and not trusted_source:
            LOGGER.debug(
                "Ignoring external request id from untrusted source %s", client_ip
            )

        request_id = build_request_id(
            incoming_request_id,
            allow_existing=bool(trusted_source),
        )

        duplicate = request_id_tracker.register(request_id)
        if duplicate:
            LOGGER.warning(
                "Request ID collision detected: %s from %s", request_id, client_ip
            )

        try:
            response = await call_next(request)
        except Exception:  # pragma: no cover - exercised via tests
            LOGGER.exception(
                "Unhandled exception processing request from %s", client_ip
            )
            response = JSONResponse(
                status_code=500, content={"detail": "Internal Server Error"}
            )

        response.headers.setdefault(settings.api_version_header, __version__)
        response.headers.setdefault(settings.request_id_header, request_id)
        if settings.security_headers_enabled:
            response.headers.setdefault("X-Content-Type-Options", "nosniff")
            response.headers.setdefault("X-Frame-Options", "DENY")
            response.headers.setdefault("X-XSS-Protection", "1; mode=block")
            response.headers.setdefault("Cache-Control", "no-store")
            response.headers.setdefault(
                "Content-Security-Policy",
                settings.security_headers.content_security_policy,
            )
            response.headers.setdefault(
                "Referrer-Policy",
                settings.security_headers.referrer_policy,
            )
            response.headers.setdefault(
                "Permissions-Policy",
                settings.security_headers.permissions_policy,
            )
            if settings.enforce_https:
                response.headers.setdefault(
                    "Strict-Transport-Security",
                    (
                        f"max-age={settings.hsts_seconds}; includeSubDomains"
                        if settings.include_hsts_subdomains
                        else f"max-age={settings.hsts_seconds}"
                    ),
                )
                response.headers.setdefault(
                    "Expect-CT", settings.security_headers.expect_ct
                )
        return response

    @app.get("/health", tags=["health"])
    def health() -> dict[str, str]:
        """Return application status and version for liveness probes."""
        return {
            "status": "ok",
            "version": __version__,
            "rate_limit": str(settings.rate_limit.max_requests),
            "rate_limit_window": str(settings.rate_limit.window_seconds),
        }

    @app.get("/ping", tags=["health"])
    def ping() -> dict[str, str]:
        return {"pong": "ok"}

    @app.get("/api/v1/projects", response_model=List[ProjectSchema], tags=["projects"])
    def list_projects(
        skip: int = 0,
        limit: int = 100,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> List[ProjectSchema]:
        return project_crud.get_projects(
            db, owner_id=current_user.id, skip=skip, limit=limit
        )

    @app.post(
        "/api/v1/projects",
        response_model=ProjectSchema,
        status_code=status.HTTP_201_CREATED,
        tags=["projects"],
    )
    def create_project(
        project: ProjectCreate,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> ProjectSchema:
        return project_crud.create_project(
            db, project=project, owner_id=current_user.id
        )

    @app.get(
        "/api/v1/projects/{project_id}",
        response_model=ProjectSchema,
        tags=["projects"],
    )
    def get_project(
        project_id: int,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> ProjectSchema:
        db_project = project_crud.get_project(
            db,
            project_id=project_id,
            owner_id=current_user.id,
            is_admin=current_user.role == UserRole.admin,
        )
        if not db_project:
            raise HTTPException(status_code=404, detail="Project not found")
        return db_project

    @app.put(
        "/api/v1/projects/{project_id}",
        response_model=ProjectSchema,
        tags=["projects"],
    )
    def update_project(
        project_id: int,
        project_update: ProjectUpdate,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> ProjectSchema:
        is_admin = current_user.role == UserRole.admin
        db_project = project_crud.update_project(
            db,
            project_id=project_id,
            project_update=project_update,
            owner_id=current_user.id,
            is_admin=is_admin,
        )
        if not db_project:
            project_exists = project_crud.get_project(
                db, project_id=project_id, owner_id=None, is_admin=True
            )
            if project_exists:
                raise HTTPException(status_code=403, detail="Insufficient permissions")
            raise HTTPException(status_code=404, detail="Project not found")
        return db_project

    @app.delete(
        "/api/v1/projects/{project_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        tags=["projects"],
    )
    def delete_project(
        project_id: int,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> None:
        is_admin = current_user.role == UserRole.admin
        success = project_crud.delete_project(
            db,
            project_id=project_id,
            owner_id=current_user.id,
            is_admin=is_admin,
        )
        if not success:
            project_exists = project_crud.get_project(
                db, project_id=project_id, owner_id=None, is_admin=True
            )
            if project_exists:
                raise HTTPException(status_code=403, detail="Insufficient permissions")
            raise HTTPException(status_code=404, detail="Project not found")

    @app.get(
        "/api/v1/projects/{project_id}/tasks",
        response_model=List[TaskSchema],
        tags=["tasks"],
    )
    def list_tasks(
        project_id: int,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> List[TaskSchema]:
        return task_crud.get_tasks_by_project(
            db, project_id=project_id, owner_id=current_user.id
        )

    @app.post(
        "/api/v1/tasks",
        response_model=TaskSchema,
        status_code=status.HTTP_201_CREATED,
        tags=["tasks"],
    )
    def create_task_endpoint(
        task: TaskCreate,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> TaskSchema:
        db_task = task_crud.create_task(db, task=task, owner_id=current_user.id)
        if not db_task:
            raise HTTPException(status_code=404, detail="Project not found")
        return db_task

    @app.put(
        "/api/v1/tasks/{task_id}",
        response_model=TaskSchema,
        tags=["tasks"],
    )
    def update_task_endpoint(
        task_id: int,
        task_update: TaskUpdate,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> TaskSchema:
        db_task = task_crud.update_task(
            db, task_id=task_id, task_update=task_update, owner_id=current_user.id
        )
        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")
        return db_task

    @app.delete(
        "/api/v1/tasks/{task_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        tags=["tasks"],
    )
    def delete_task_endpoint(
        task_id: int,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> None:
        success = task_crud.delete_task(db, task_id=task_id, owner_id=current_user.id)
        if not success:
            raise HTTPException(status_code=404, detail="Task not found")

    # Initialize DB tables for local dev (SQLite). In production, use Alembic.
    try:
        init_db()
    except Exception:  # pragma: no cover - best-effort dev path
        LOGGER.debug("init_db skipped or failed (likely non-SQLite backend)")

    @app.on_event("startup")
    async def _log_routes() -> None:  # pragma: no cover - diagnostic
        try:
            paths = [getattr(r, "path", "<unknown>") for r in app.routes]
            LOGGER.info("Registered routes: %s", paths)
        except Exception:
            pass

    return app


app = create_app()
