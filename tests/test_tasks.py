from uuid import uuid4

from fastapi.testclient import TestClient

from src.main import app


def register_and_login(client: TestClient) -> tuple[dict[str, str], int]:
    email = f"tasker-{uuid4().hex[:8]}@example.com"
    password = "secret123"
    register_payload = {
        "email": email,
        "name": "Task Owner",
        "password": password,
        "role": "gestor",
    }
    client.post("/api/v1/auth/register", json=register_payload)
    login_resp = client.post(
        "/api/v1/auth/login", json={"email": email, "password": password}
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    project_resp = client.post(
        "/api/v1/projects",
        headers=headers,
        json={"name": "Kanban", "description": "Board", "status": "active"},
    )
    project_id = project_resp.json()["id"]
    return headers, project_id


def test_task_crud_flow():
    client = TestClient(app)
    headers, project_id = register_and_login(client)

    create_resp = client.post(
        "/api/v1/tasks",
        headers=headers,
        json={
            "title": "Planejar sprint",
            "description": "Definir backlog",
            "project_id": project_id,
            "status": "todo",
        },
    )
    assert create_resp.status_code == 201
    task = create_resp.json()

    list_resp = client.get(f"/api/v1/projects/{project_id}/tasks", headers=headers)
    assert list_resp.status_code == 200
    assert any(item["id"] == task["id"] for item in list_resp.json())

    update_resp = client.put(
        f"/api/v1/tasks/{task['id']}",
        headers=headers,
        json={"status": "in_progress"},
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "in_progress"

    delete_resp = client.delete(f"/api/v1/tasks/{task['id']}", headers=headers)
    assert delete_resp.status_code == 204
    list_after = client.get(f"/api/v1/projects/{project_id}/tasks", headers=headers)
    assert all(item["id"] != task["id"] for item in list_after.json())
