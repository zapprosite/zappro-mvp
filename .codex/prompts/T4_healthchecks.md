[Docker healthchecks]

## Critical Fixes
1. docker-compose.yml: healthcheck da API usando /healthz.
2. Definir dependências saudáveis para ordem de start.

## Validation Steps
- shell: docker compose up -d && docker compose ps
- shell: docker inspect api --format='{{json .State.Health}}' | jq .Status=="healthy"

## MCP Usage Priority
filesystem → shell → git → github

Commit: ci(docker): add healthchecks and deps order
