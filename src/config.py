"""Application configuration helpers."""

from __future__ import annotations

import json
from functools import lru_cache
from typing import List

from pydantic import BaseModel, Field
from pydantic.functional_validators import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def _parse_sequence(value: List[str] | str) -> List[str]:
    """Accept JSON arrays or comma-delimited strings for list settings."""
    if isinstance(value, list):
        return [item.strip() for item in value if item and str(item).strip()]

    if isinstance(value, str):
        candidate = value.strip()
        if not candidate:
            return []
        if candidate.startswith("["):
            try:
                loaded = json.loads(candidate)
            except json.JSONDecodeError as exc:  # pragma: no cover - logged upstream
                raise ValueError(f"Unable to parse JSON sequence: {candidate}") from exc
            if isinstance(loaded, list):
                return [str(item).strip() for item in loaded if str(item).strip()]
            raise ValueError("Expected JSON array for sequence value.")
        return [part.strip() for part in candidate.split(",") if part.strip()]

    raise TypeError("Expected list or string value")


class CorsSettings(BaseModel):
    """CORS configuration."""

    allow_origins: List[str] = Field(default_factory=lambda: ["http://localhost:3000"])
    allow_credentials: bool = False
    allow_methods: List[str] = Field(
        default_factory=lambda: ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    )
    allow_headers: List[str] = Field(default_factory=lambda: ["*"])
    expose_headers: List[str] = Field(default_factory=list)

    _parse_allow_origins = field_validator("allow_origins", mode="before")(
        _parse_sequence
    )
    _parse_allow_methods = field_validator("allow_methods", mode="before")(
        _parse_sequence
    )
    _parse_allow_headers = field_validator("allow_headers", mode="before")(
        _parse_sequence
    )
    _parse_expose_headers = field_validator("expose_headers", mode="before")(
        _parse_sequence
    )


class RateLimitSettings(BaseModel):
    """Rate limit configuration."""

    max_requests: int = 100
    window_seconds: int = 60
    ttl_seconds: int | None = None
    max_entries: int = 10_000
    backend: str = Field(default="memory", description="memory or redis")
    redis_url: str | None = None


class SecurityHeaders(BaseModel):
    """HTTP security header values."""

    content_security_policy: str = (
        "default-src 'self'; frame-ancestors 'none'; object-src 'none'; base-uri 'self'"
    )
    referrer_policy: str = "strict-origin-when-cross-origin"
    permissions_policy: str = "geolocation=(), microphone=(), camera=()"
    expect_ct: str = "max-age=86400, enforce"


class Settings(BaseSettings):
    """ZapPro configuration sourced from environment variables."""

    model_config = SettingsConfigDict(
        env_prefix="ZAPPRO_",
        env_nested_delimiter="__",
        validate_default=True,
        extra="ignore",
    )

    app_name: str = "ZapPro API"
    allowed_hosts: List[str] = Field(
        default_factory=lambda: ["127.0.0.1", "localhost", "testserver"]
    )
    enable_cors: bool = True
    cors: CorsSettings = CorsSettings()
    rate_limit: RateLimitSettings = RateLimitSettings()
    enforce_https: bool = False
    hsts_seconds: int = 31536000
    include_hsts_subdomains: bool = True
    security_headers_enabled: bool = True
    api_version_header: str = "X-API-Version"
    request_id_header: str = "X-Request-ID"
    log_requests: bool = True
    timezone: str = "UTC"
    security_headers: SecurityHeaders = SecurityHeaders()
    trusted_proxies: List[str] = Field(default_factory=list)
    client_ip_header: str = "x-forwarded-for"
    trust_client_request_id: bool = False
    request_id_trusted_hosts: List[str] = Field(default_factory=list)
    request_id_ttl_seconds: int = 300
    request_id_max_entries: int = 20_000

    _parse_allowed_hosts = field_validator("allowed_hosts", mode="before")(
        _parse_sequence
    )
    _parse_trusted_proxies = field_validator("trusted_proxies", mode="before")(
        _parse_sequence
    )
    _parse_request_id_trusted_hosts = field_validator(
        "request_id_trusted_hosts", mode="before"
    )(_parse_sequence)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
