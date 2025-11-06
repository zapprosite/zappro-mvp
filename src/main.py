"""ZapPro API entrypoint with security hardening middleware."""

from __future__ import annotations

import logging
from typing import Any, Dict

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware import Middleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from . import __version__
from .config import Settings, get_settings
from .security import (
    FixedWindowRateLimiter,
    RequestIdTracker,
    build_request_id,
    resolve_client_ip,
)

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
            LOGGER.exception("Unhandled exception processing request from %s", client_ip)
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

    return app


app = create_app()
