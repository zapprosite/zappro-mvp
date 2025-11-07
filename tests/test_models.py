from src.models import Document, Material, Project, ProjectStatus, Task, TaskStatus, User, UserRole


def test_project_relationships_and_defaults() -> None:
    owner = User(email="owner@example.com", name="Owner", hashed_password="hashed")
    project = Project(name="Projeto Teste", owner=owner)

    task = Task(title="Configurar ambiente", project=project, assignee=owner)
    material = Material(name="Cimento", project=project)
    document = Document(project=project, url="https://example.com/doc", type="pdf", task=task)

    assert project.owner is owner
    assert project in owner.projects
    assert task in project.tasks
    assert material in project.materials
    assert document in project.documents
    assert document.task is task
    assert task in owner.assigned_tasks


def test_enum_values() -> None:
    assert {role.value for role in UserRole} == {"admin", "gestor", "operador"}
    assert {status.value for status in ProjectStatus} == {"planning", "active", "completed", "paused"}
    assert {status.value for status in TaskStatus} == {"todo", "in_progress", "done"}
