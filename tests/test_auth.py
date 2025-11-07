from datetime import timedelta
from uuid import uuid4

from fastapi.testclient import TestClient

from src.main import app
from src.utils.auth import generate_refresh_token


def _register_user(client: TestClient) -> tuple[str, str]:
    email = f"auth-{uuid4().hex[:8]}@example.com"
    password = "secret123"
    payload = {
        "email": email,
        "name": "Auth Tester",
        "password": password,
        "role": "gestor",
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    return email, password


def _login(client: TestClient, email: str, password: str) -> dict:
    response = client.post(
        "/api/v1/auth/login", json={"email": email, "password": password}
    )
    assert response.status_code == 200
    return response.json()


def test_login_returns_access_and_refresh_tokens():
    client = TestClient(app)
    email, password = _register_user(client)

    login_response = _login(client, email, password)

    assert "access_token" in login_response
    assert "refresh_token" in login_response
    assert login_response["token_type"] == "bearer"
    assert login_response["user"]["email"] == email


def test_refresh_with_valid_token_returns_new_access_token():
    client = TestClient(app)
    email, password = _register_user(client)
    login_response = _login(client, email, password)

    refresh_token = login_response["refresh_token"]
    refresh_response = client.post(
        "/api/v1/auth/refresh",
        headers={"Authorization": f"Bearer {refresh_token}"},
    )

    assert refresh_response.status_code == 200
    body = refresh_response.json()
    assert body["access_token"]
    assert body["token_type"] == "bearer"


def test_refresh_with_expired_token_returns_401():
    client = TestClient(app)
    email, _ = _register_user(client)
    expired_refresh = generate_refresh_token(
        {"sub": email},
        expires_delta=timedelta(seconds=-5),
    )

    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": expired_refresh},
    )
    assert response.status_code == 401


def test_refresh_with_invalid_token_returns_401():
    client = TestClient(app)
    _register_user(client)

    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": "not-a-valid-token"},
    )
    assert response.status_code == 401
