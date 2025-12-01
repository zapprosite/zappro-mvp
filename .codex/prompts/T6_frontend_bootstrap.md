[Frontend bootstrap]

## Critical Fixes
1. Criar Next.js 15 App Router se ausente.
2. Página "/" lista projetos consumindo /api/projects.

## Validation Steps
- shell: make lint
- playwright: abrir "/" e esperar heading "Projects" + lista

## MCP Usage Priority
filesystem → github → git → playwright

Commit: feat(web): bootstrap Next.js 15 home with projects list
