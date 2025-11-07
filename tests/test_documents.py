from uuid import uuid4

from fastapi.testclient import TestClient

from src.main import app


def _register_user(client: TestClient, role: str = "gestor") -> dict[str, str]:
    email = f"doc-{uuid4().hex[:8]}@example.com"
    password = "secret123"
    payload = {
        "email": email,
        "name": "Document Owner",
        "password": password,
        "role": role,
    }
    register = client.post("/api/v1/auth/register", json=payload)
    assert register.status_code == 201
    login = client.post(
        "/api/v1/auth/login", json={"email": email, "password": password}
    )
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _create_project(client: TestClient, headers: dict[str, str]) -> int:
    response = client.post(
        "/api/v1/projects",
        headers=headers,
        json={"name": "Complexo Logístico", "description": "Docs", "status": "active"},
    )
    assert response.status_code == 201
    return response.json()["id"]


def _create_task(client: TestClient, headers: dict[str, str], project_id: int) -> int:
    response = client.post(
        "/api/v1/tasks",
        headers=headers,
        json={
            "title": "Revisar contrato",
            "description": "Coletar assinaturas",
            "project_id": project_id,
            "status": "todo",
        },
    )
    assert response.status_code == 201
    return response.json()["id"]


def _create_document(
    client: TestClient,
    headers: dict[str, str],
    *,
    project_id: int,
    task_id: int | None = None,
    url: str = "https://cdn.example.com/doc.pdf",
) -> dict:
    payload = {
        "project_id": project_id,
        "url": url,
        "type": "contract",
        "description": "Contrato de prestação",
    }
    if task_id is not None:
        payload["task_id"] = task_id
    response = client.post("/api/v1/documents", headers=headers, json=payload)
    assert response.status_code == 201
    return response.json()


def test_create_document_with_task_and_project_and_unauthorized():
    client = TestClient(app)
    owner_headers = _register_user(client, role="gestor")
    project_id = _create_project(client, owner_headers)
    task_id = _create_task(client, owner_headers, project_id)

    doc_with_task = client.post(
        "/api/v1/documents",
        headers=owner_headers,
        json={
            "project_id": project_id,
            "task_id": task_id,
            "url": "https://cdn.example.com/checklist.pdf",
            "type": "checklist",
        },
    )
    assert doc_with_task.status_code == 201
    assert doc_with_task.json()["task_id"] == task_id

    doc_without_task = client.post(
        "/api/v1/documents",
        headers=owner_headers,
        json={
            "project_id": project_id,
            "url": "https://cdn.example.com/planta.pdf",
            "type": "blueprint",
        },
    )
    assert doc_without_task.status_code == 201

    outsider_headers = _register_user(client, role="operador")
    unauthorized = client.post(
        "/api/v1/documents",
        headers=outsider_headers,
        json={
            "project_id": project_id,
            "url": "https://cdn.example.com/unauthorized.pdf",
            "type": "risk",
        },
    )
    assert unauthorized.status_code == 403


def test_list_documents_by_project_and_task():
    client = TestClient(app)
    owner_headers = _register_user(client)
    project_id = _create_project(client, owner_headers)
    task_id = _create_task(client, owner_headers, project_id)
    document = _create_document(
        client,
        owner_headers,
        project_id=project_id,
        task_id=task_id,
        url="https://cdn.example.com/procurement.pdf",
    )

    project_list = client.get(
        f"/api/v1/projects/{project_id}/documents",
        headers=owner_headers,
    )
    assert project_list.status_code == 200
    assert any(item["id"] == document["id"] for item in project_list.json())

    task_list = client.get(
        f"/api/v1/tasks/{task_id}/documents",
        headers=owner_headers,
    )
    assert task_list.status_code == 200
    assert task_list.json()[0]["task_id"] == task_id


def test_get_update_delete_document_flow():
    client = TestClient(app)
    owner_headers = _register_user(client)
    project_id = _create_project(client, owner_headers)
    document = _create_document(
        client,
        owner_headers,
        project_id=project_id,
        url="https://cdn.example.com/report.pdf",
    )

    detail = client.get(
        f"/api/v1/documents/{document['id']}",
        headers=owner_headers,
    )
    assert detail.status_code == 200
    assert detail.json()["url"].endswith("report.pdf")

    update_resp = client.put(
        f"/api/v1/documents/{document['id']}",
        headers=owner_headers,
        json={"url": "https://cdn.example.com/report-v2.pdf"},
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["url"].endswith("report-v2.pdf")

    outsider_headers = _register_user(client, role="operador")
    outsider_update = client.put(
        f"/api/v1/documents/{document['id']}",
        headers=outsider_headers,
        json={"url": "https://cdn.example.com/hack.pdf"},
    )
    assert outsider_update.status_code == 403

    delete_resp = client.delete(
        f"/api/v1/documents/{document['id']}",
        headers=owner_headers,
    )
    assert delete_resp.status_code == 204

    after_delete = client.get(
        f"/api/v1/documents/{document['id']}",
        headers=owner_headers,
    )
    assert after_delete.status_code == 404
