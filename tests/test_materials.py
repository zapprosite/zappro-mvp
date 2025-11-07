from uuid import uuid4

from fastapi.testclient import TestClient

from src.main import app


def _register_user(client: TestClient, role: str = "gestor") -> dict[str, str]:
    email = f"material-{uuid4().hex[:8]}@example.com"
    password = "secret123"
    payload = {
        "email": email,
        "name": "Material User",
        "password": password,
        "role": role,
    }
    register = client.post("/api/v1/auth/register", json=payload)
    assert register.status_code == 201
    login = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _create_project(client: TestClient, headers: dict[str, str]) -> int:
    response = client.post(
        "/api/v1/projects",
        headers=headers,
        json={"name": "Residencial Solar", "description": "Residencial", "status": "active"},
    )
    assert response.status_code == 201
    return response.json()["id"]


def _create_material(
    client: TestClient,
    headers: dict[str, str],
    project_id: int,
    name: str = "Concreto",
) -> dict:
    response = client.post(
        "/api/v1/materials",
        headers=headers,
        json={"name": name, "project_id": project_id, "stock": 10, "supplier": "Fornecedor"},
    )
    assert response.status_code == 201
    return response.json()


def test_create_material_authorization():
    client = TestClient(app)
    owner_headers = _register_user(client, role="gestor")
    project_id = _create_project(client, owner_headers)

    owner_resp = client.post(
        "/api/v1/materials",
        headers=owner_headers,
        json={"name": "Aço CA-50", "project_id": project_id, "stock": 15},
    )
    assert owner_resp.status_code == 201

    admin_headers = _register_user(client, role="admin")
    admin_resp = client.post(
        "/api/v1/materials",
        headers=admin_headers,
        json={"name": "Vidro temperado", "project_id": project_id, "stock": 5},
    )
    assert admin_resp.status_code == 201

    outsider_headers = _register_user(client, role="operador")
    outsider_resp = client.post(
        "/api/v1/materials",
        headers=outsider_headers,
        json={"name": "Madeira tratada", "project_id": project_id, "stock": 3},
    )
    assert outsider_resp.status_code == 403


def test_list_and_detail_materials():
    client = TestClient(app)
    owner_headers = _register_user(client, role="gestor")
    project_id = _create_project(client, owner_headers)
    material = _create_material(client, owner_headers, project_id, name="Cimento CP-II")

    list_resp = client.get(
        f"/api/v1/projects/{project_id}/materials",
        headers=owner_headers,
    )
    assert list_resp.status_code == 200
    body = list_resp.json()
    assert any(item["id"] == material["id"] for item in body)

    detail_resp = client.get(
        f"/api/v1/materials/{material['id']}",
        headers=owner_headers,
    )
    assert detail_resp.status_code == 200
    assert detail_resp.json()["name"] == "Cimento CP-II"

    outsider_headers = _register_user(client, role="operador")
    outsider_detail = client.get(
        f"/api/v1/materials/{material['id']}",
        headers=outsider_headers,
    )
    assert outsider_detail.status_code == 403


def test_update_material_requires_owner_or_admin():
    client = TestClient(app)
    owner_headers = _register_user(client, role="gestor")
    project_id = _create_project(client, owner_headers)
    material = _create_material(client, owner_headers, project_id, name="Areia fina")

    update_resp = client.put(
        f"/api/v1/materials/{material['id']}",
        headers=owner_headers,
        json={"stock": 42},
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["stock"] == 42

    admin_headers = _register_user(client, role="admin")
    admin_update = client.put(
        f"/api/v1/materials/{material['id']}",
        headers=admin_headers,
        json={"supplier": "Central Supply"},
    )
    assert admin_update.status_code == 200
    assert admin_update.json()["supplier"] == "Central Supply"

    outsider_headers = _register_user(client, role="operador")
    outsider_update = client.put(
        f"/api/v1/materials/{material['id']}",
        headers=outsider_headers,
        json={"stock": 1},
    )
    assert outsider_update.status_code == 403


def test_delete_material_requires_owner_or_admin():
    client = TestClient(app)
    owner_headers = _register_user(client, role="gestor")
    project_id = _create_project(client, owner_headers)
    material_owner = _create_material(client, owner_headers, project_id, name="Brita 1")
    material_admin = _create_material(client, owner_headers, project_id, name="Tijolo 8 furos")

    outsider_headers = _register_user(client, role="operador")
    outsider_delete = client.delete(
        f"/api/v1/materials/{material_owner['id']}",
        headers=outsider_headers,
    )
    assert outsider_delete.status_code == 403

    owner_delete = client.delete(
        f"/api/v1/materials/{material_owner['id']}",
        headers=owner_headers,
    )
    assert owner_delete.status_code == 204

    admin_headers = _register_user(client, role="admin")
    admin_delete = client.delete(
        f"/api/v1/materials/{material_admin['id']}",
        headers=admin_headers,
    )
    assert admin_delete.status_code == 204
