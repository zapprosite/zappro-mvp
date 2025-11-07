from uuid import uuid4

from fastapi.testclient import TestClient

from src.main import app


def test_register_and_login_flow():
    client = TestClient(app)

    email = f"user-{uuid4().hex[:8]}@example.com"
    payload = {
        "email": email,
        "name": "Tester",
        "password": "secret123",
        "role": "gestor",
    }

    r = client.post("/api/v1/auth/register", json=payload)
    assert r.status_code in (201, 400)

    r2 = client.post(
        "/api/v1/auth/login", json={"email": email, "password": "secret123"}
    )
    assert r2.status_code == 200
    body = r2.json()
    assert body["token_type"] == "bearer"
    assert body["user"]["email"] == email
