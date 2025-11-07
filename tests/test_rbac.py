from fastapi.testclient import TestClient


def _create_project(client: TestClient, headers: dict[str, str]) -> int:
    response = client.post(
        "/api/v1/projects",
        headers=headers,
        json={"name": "RBAC Obras", "description": "Controle", "status": "active"},
    )
    assert response.status_code == 201
    return response.json()["id"]


def _create_task(client: TestClient, headers: dict[str, str], project_id: int) -> int:
    response = client.post(
        "/api/v1/tasks",
        headers=headers,
        json={"title": "Checklist", "project_id": project_id, "status": "todo"},
    )
    assert response.status_code == 201
    return response.json()["id"]


def test_materials_role_enforcement(client_gestor, client_admin, client_operador):
    gestor_client, gestor_headers = client_gestor
    admin_client, admin_headers = client_admin
    operador_client, operador_headers = client_operador

    project_id = _create_project(gestor_client, gestor_headers)

    gestor_resp = gestor_client.post(
        "/api/v1/materials",
        headers=gestor_headers,
        json={"name": "Cabo de aço", "project_id": project_id, "stock": 5},
    )
    assert gestor_resp.status_code == 201

    admin_resp = admin_client.post(
        "/api/v1/materials",
        headers=admin_headers,
        json={"name": "Painel solar", "project_id": project_id, "stock": 12},
    )
    assert admin_resp.status_code == 201

    operador_resp = operador_client.post(
        "/api/v1/materials",
        headers=operador_headers,
        json={"name": "Cimento comum", "project_id": project_id, "stock": 3},
    )
    assert operador_resp.status_code == 403


def test_documents_role_enforcement(client_gestor, client_admin, client_operador):
    gestor_client, gestor_headers = client_gestor
    admin_client, admin_headers = client_admin
    operador_client, operador_headers = client_operador

    project_id = _create_project(gestor_client, gestor_headers)
    task_id = _create_task(gestor_client, gestor_headers, project_id)

    gestor_doc = gestor_client.post(
        "/api/v1/documents",
        headers=gestor_headers,
        json={
            "project_id": project_id,
            "task_id": task_id,
            "url": "https://cdn.example.com/gestor.pdf",
            "type": "brief",
        },
    )
    assert gestor_doc.status_code == 201

    admin_doc = admin_client.post(
        "/api/v1/documents",
        headers=admin_headers,
        json={
            "project_id": project_id,
            "url": "https://cdn.example.com/admin.pdf",
            "type": "policy",
        },
    )
    assert admin_doc.status_code == 201

    operador_doc = operador_client.post(
        "/api/v1/documents",
        headers=operador_headers,
        json={
            "project_id": project_id,
            "url": "https://cdn.example.com/operador.pdf",
            "type": "risk",
        },
    )
    assert operador_doc.status_code == 403


def test_project_update_delete_permissions(
    client_gestor, client_admin, client_operador
):
    gestor_client, gestor_headers = client_gestor
    admin_client, admin_headers = client_admin
    operador_client, operador_headers = client_operador

    project_id = _create_project(gestor_client, gestor_headers)

    update_owner = gestor_client.put(
        f"/api/v1/projects/{project_id}",
        headers=gestor_headers,
        json={"description": "Atualizado pelo gestor"},
    )
    assert update_owner.status_code == 200

    update_admin = admin_client.put(
        f"/api/v1/projects/{project_id}",
        headers=admin_headers,
        json={"status": "paused"},
    )
    assert update_admin.status_code == 200

    update_operador = operador_client.put(
        f"/api/v1/projects/{project_id}",
        headers=operador_headers,
        json={"status": "completed"},
    )
    assert update_operador.status_code == 403

    delete_operador = operador_client.delete(
        f"/api/v1/projects/{project_id}",
        headers=operador_headers,
    )
    assert delete_operador.status_code == 403

    delete_admin = admin_client.delete(
        f"/api/v1/projects/{project_id}",
        headers=admin_headers,
    )
    assert delete_admin.status_code == 204
