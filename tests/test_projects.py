from uuid import uuid4

from fastapi.testclient import TestClient

from src.main import app


def auth_headers(client: TestClient) -> dict[str, str]:
    email = f"owner-{uuid4().hex[:8]}@example.com"
    password = "secret123"
    payload = {"email": email, "name": "Owner", "password": password, "role": "gestor"}

    register_response = client.post("/api/v1/auth/register", json=payload)
    assert register_response.status_code in (201, 400)

    login_response = client.post(
        "/api/v1/auth/login", json={"email": email, "password": password}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_projects_crud_flow():
    client = TestClient(app)
    headers = auth_headers(client)

    create_resp = client.post(
        "/api/v1/projects",
        headers=headers,
        json={
            "name": "Projeto Casa Verde",
            "description": "Construção residencial",
            "status": "active",
        },
    )
    assert create_resp.status_code == 201
    project = create_resp.json()
    project_id = project["id"]
    assert project["status"] == "active"

    list_resp = client.get("/api/v1/projects", headers=headers)
    assert list_resp.status_code == 200
    assert any(p["id"] == project_id for p in list_resp.json())

    update_resp = client.put(
        f"/api/v1/projects/{project_id}",
        headers=headers,
        json={"status": "completed"},
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "completed"

    delete_resp = client.delete(f"/api/v1/projects/{project_id}", headers=headers)
    assert delete_resp.status_code == 204

    after_delete = client.get(f"/api/v1/projects/{project_id}", headers=headers)
    assert after_delete.status_code == 404
