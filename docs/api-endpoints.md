# Catálogo de Endpoints (ZapPro API)

Este documento descreve as rotas FastAPI expostas por `src.main` e seus contratos JSON. Use-o sempre que precisar atualizar clientes, Playwright/E2E ou documentar integrações.

## Contrato de Resposta

- **Sucesso:** o corpo contém o recurso solicitado (Pydantic models serializados) e os cabeçalhos `X-API-Version`, `X-Request-Id`. Os endpoints que retornam listas entregam o array diretamente.
- **Erros:** o FastAPI lança `HTTPException`, gerando respostas como:

```json
{"detail": "Project not found"}
```

> A equipe prioriza que os consumidores tratem o campo `detail` e exibam mensagens amigáveis; registros internos são logados com trace_id, rota e duração.

## Cabeçalhos Relevantes

- `Authorization: Bearer <token>` — obrigatório para rotas protegidas (projetos, tarefas, documentos, materiais).
- `X-API-Version` — versão (`src.__version__`) enviada em todas as respostas.
- `X-Request-Id` — identifica a requisição para rastreio.

## Health & Liveness

### `GET /healthz`

- **Objetivo:** prontidão para orquestradores
- **Resposta (200):**

```json
{"status": "ok"}
```

### `GET /health`

Rotina adicional (para debug) que também retorna metadados de rate limit.

## Autenticação JWT

### `POST /api/v1/auth/register`

- **Body:**

```json
{ "email": "ops@zappro.site", "password": "Segredo#123", "name": "Operador", "role": "gestor" }
```

- **Resposta (201):** propaga o usuário criado (sem senha).

### `POST /api/v1/auth/login`

- **Body:**

```json
{ "email": "ops@zappro.site", "password": "Segredo#123" }
```

- **Resposta (200):**

```json
{
  "access_token": "<jwt>",
  "refresh_token": "<jwt-refresh>",
  "token_type": "bearer",
  "user": { "id": 1, "email": "ops@zappro.site", "name": "Operador", "role": "gestor" }
}
```

### `POST /api/v1/auth/refresh`

- **Body:** `{"refresh_token": "<jwt-refresh>"}` ou use o cabeçalho `Authorization: Bearer <refresh>`
- **Resposta (200):** `{"access_token": "<new jwt>"}`

## Projetos (`/api/v1/projects`)

> Todas as rotas exigem `Authorization` com token válido.

### `GET /api/v1/projects`

- Lista projetos do usuário (ou todos se for admin).
- **Resposta (200):** array de objetos com campos `id`, `name`, `description`, `status`, `owner_id`, `created_at`, `updated_at`.

### `POST /api/v1/projects`

- Cria novo projeto.
- **Body:**

```json
{ "name": "Obra Alpha", "description": "Expansão", "status": "planning" }
```

- **Resposta (201):** projeto criado.
- **Erros:** 403 (sem permissão), 400 (dados faltantes).

### `GET /api/v1/projects/{project_id}`

- Retorna projeto por `id`.
- **Erros:** 404 quando não encontrado.

### `PUT /api/v1/projects/{project_id}`

- Atualiza metadata (nome, descrição, status).
- **Body:** quaisquer campos a atualizar.
- **Erros:** 403 ou 404.

### `DELETE /api/v1/projects/{project_id}`

- Remove projeto (admin ou dono).
- **Resposta (204):** sem corpo.

### `GET /api/v1/projects/{project_id}/tasks`

- Retorna tarefas associadas ao projeto.
- Usa a mesma resposta do endpoint de tarefas (veja abaixo).

## Tarefas (`/api/v1/tasks`)

### `POST /api/v1/tasks`

- **Body:**

```json
{ "title": "Instalar fôrmas", "description": "Etapa 1", "project_id": 1, "status": "todo" }
```

- **Resposta (201):** tarefa criada.

### `PUT /api/v1/tasks/{task_id}`

- Atualiza título, descrição, status, `assignee_id`, `due_date`.

### `DELETE /api/v1/tasks/{task_id}`

- Remove a tarefa (401 se não autenticado, 404 se não encontrada).

## Documentos (`/api/v1/documents`)

### `GET /api/v1/documents`

- Lista todos os documentos acessíveis ao usuário (admin ou proprietário).

### `POST /api/v1/documents`

- Cria documento ligado a `project_id` (e opcionalmente `task_id`).

### `GET /api/v1/documents/{document_id}`

- Retorna documento específico.

### `PUT /api/v1/documents/{document_id}` / `DELETE /api/v1/documents/{document_id}`

- Atualizam ou removem o documento com validações RBAC.

### `GET /api/v1/projects/{project_id}/documents` & `/tasks/{task_id}/documents`

- Filtros que garantem escopo por projeto/tarefa.

## Materiais (`/api/v1/materials`)

- Mesma estrutura de CRUD e escopo RBAC do documento.
- Exemplos:
  - `GET /api/v1/materials` (lista)
  - `POST /api/v1/materials` com `{ "name": "Aço", "project_id": 1, "stock": 10 }`
  - `GET /api/v1/materials/{material_id}`, `PUT`, `DELETE`
  - `GET /api/v1/projects/{project_id}/materials`

## Observações Gerais

- A validação de JWT usa o algoritmo RS256 configurado via variáveis de ambiente (`ZAPPRO_JWT_PUBLIC`/`PRIVATE`).
- Requisições falhas retornam `detail` com motivos (403/404/400) e são registradas com trace_id no log.
- Testes e Playwright usam `http://127.0.0.1:8000` para a API; use o arquivo `frontend/src/lib/api-client.ts` como referência para autenticação e headers.
