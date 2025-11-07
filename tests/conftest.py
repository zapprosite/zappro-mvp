import sys
from pathlib import Path
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from src.main import app

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def _auth_headers(client: TestClient, role: str) -> dict[str, str]:
    email = f"rbac-{role}-{uuid4().hex[:8]}@example.com"
    payload = {
        "email": email,
        "name": f"{role.title()} User",
        "password": "secret123",
        "role": role,
    }
    register = client.post("/api/v1/auth/register", json=payload)
    assert register.status_code == 201
    login = client.post("/api/v1/auth/login", json={"email": email, "password": "secret123"})
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def client_admin() -> tuple[TestClient, dict[str, str]]:
    client = TestClient(app)
    return client, _auth_headers(client, "admin")


@pytest.fixture
def client_gestor() -> tuple[TestClient, dict[str, str]]:
    client = TestClient(app)
    return client, _auth_headers(client, "gestor")


@pytest.fixture
def client_operador() -> tuple[TestClient, dict[str, str]]:
    client = TestClient(app)
    return client, _auth_headers(client, "operador")
