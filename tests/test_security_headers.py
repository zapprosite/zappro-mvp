from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src import __version__
from src.config import Settings
from src.main import create_app

SECURITY_LOG = Path(__file__).resolve().parents[1] / "logs" / "security.log"


def build_client(**overrides) -> TestClient:
    settings = Settings(**overrides)
    return TestClient(create_app(settings))


def _assert_headers(response, expected_headers):
    missing = [
        header
        for header in expected_headers
        if not response.headers.get(header)
        or response.headers.get(header) == "undefined"
    ]
    if missing:
        SECURITY_LOG.parent.mkdir(parents=True, exist_ok=True)
        with SECURITY_LOG.open("a", encoding="utf-8") as log:
            log.write(
                f"{datetime.utcnow().isoformat()}Z [pytest] Missing headers {missing}. "
                f"Status={response.status_code} Body={response.text}\n"
            )
        pytest.fail(f"Missing security headers: {missing}")


def test_security_headers_present():
    client = build_client()

    response = client.get("/health")

    assert response.status_code == 200
    _assert_headers(
        response,
        [
            "X-Content-Type-Options",
            "X-Frame-Options",
            "Cache-Control",
            "X-API-Version",
            "Content-Security-Policy",
        ],
    )
    assert response.headers["X-API-Version"] == __version__
    assert "default-src 'self'" in response.headers["Content-Security-Policy"]


def test_rate_limit_blocks_after_threshold():
    client = build_client(
        rate_limit={"max_requests": 1, "window_seconds": 60, "ttl_seconds": 60}
    )

    first = client.get("/health")
    assert first.status_code == 200

    second = client.get("/health")
    assert second.status_code == 429
    assert second.headers["Retry-After"].isdigit()


def test_cors_preflight_allows_configured_origin():
    client = build_client(
        enable_cors=True,
        cors={
            "allow_origins": ["http://client.local"],
            "allow_methods": ["GET"],
            "allow_headers": ["Authorization"],
            "allow_credentials": False,
            "expose_headers": [],
        },
    )

    response = client.options(
        "/health",
        headers={
            "Origin": "http://client.local",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://client.local"


def test_allowed_hosts_parses_from_comma_string():
    settings = Settings(allowed_hosts="api.example.com,internal.local")
    assert settings.allowed_hosts == ["api.example.com", "internal.local"]


def test_trusted_request_id_is_preserved():
    client = build_client(
        trust_client_request_id=True,
        request_id_trusted_hosts=["testclient"],
    )

    response = client.get(
        "/health",
        headers={"X-Request-ID": "123e4567-e89b-12d3-a456-426614174000"},
    )

    assert response.headers["X-Request-ID"] == "123e4567-e89b-12d3-a456-426614174000"


def test_untrusted_request_id_is_regenerated():
    client = build_client(
        trust_client_request_id=False,
    )

    response = client.get(
        "/health",
        headers={"X-Request-ID": "123e4567-e89b-12d3-a456-426614174000"},
    )

    assert response.headers["X-Request-ID"] != "123e4567-e89b-12d3-a456-426614174000"


def test_error_responses_emits_security_headers():
    app = create_app()

    @app.get("/boom")
    def boom():
        raise RuntimeError("test failure")

    client = TestClient(app, raise_server_exceptions=False)

    response = client.get("/boom")
    assert response.status_code == 500
    _assert_headers(
        response,
        [
            "X-Content-Type-Options",
            "X-Frame-Options",
            "Cache-Control",
            "X-API-Version",
            "Content-Security-Policy",
        ],
    )

    not_found = client.get("/missing-route")
    assert not_found.status_code == 404
    _assert_headers(
        not_found,
        [
            "X-Content-Type-Options",
            "X-Frame-Options",
            "Cache-Control",
            "X-API-Version",
            "Content-Security-Policy",
        ],
    )
