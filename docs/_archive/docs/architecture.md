# Arquitetura — Visão Geral

> [!NOTE]
> Este documento resume os componentes principais, limites de contexto e integrações do ZapPro MVP.

## Diagrama (alto nível)

```text
          +--------------------+
          |   Next.js 15 UI    |
          |  (App Router SSR)  |
          +----------+---------+
                     |
                     | HTTP (REST, JSON)
                     v
          +-------------------------+
          |       FastAPI API       |
          |  Auth, Projects, Tasks  |
          +----+-------------+------+
               |             |
           SQLAlchemy     Webhooks (N8N/Kestra)
               |             |
               v             v
        +-------------+   +-----------+
        |  PostgreSQL |   |  Workers  |
        +-------------+   +-----------+
```

## Módulos
- Backend: `src/` (FastAPI, middleware de segurança, rotas `api/v1/*`)
- Frontend: `frontend/` (Next.js 15, shadcn/ui, TanStack Query)
- Infra: `docker/`, `docker-compose.yml` (dev), GitHub Actions (CI/CD)
- Automação: N8N (workflows), Kestra (schedules), Chatwoot (suporte)

## Decisões-chave
- Autenticação JWT (RS256), RBAC por papel
- SQLAlchemy 2.x + Alembic para migrações
- CSP/CORS rigorosos no frontend/backend
- Matriz DECISION (`docs/DECISION.md`) para refactor vs rewrite

## Referências
- `PRD.md` — visão de produto e dados
- `docs/SECURITY.md` — políticas de segurança
- `docs/WORKFLOW.md` — fluxo de Git/PR
