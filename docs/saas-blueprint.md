# SaaS Blueprint — Checklists por Fase

Este documento orienta decisões e entregas para um SaaS full‑stack, organizado pelas fases do PRD. Use como referência ao detalhar o `PRD.md` e ao abrir PRs.

## Fase 0 — Bootstrap
- Stack definida (linguagem, framework, DB, ORM/migrações, testes, lint/format, execução).
- Skeleton `src/` + `/health` + versão; `tests/` básicos; `docs/how-to-run.md` com comandos.
- `Makefile` com `fmt`, `lint`, `test`, `dev`, `run`.
- CI verde (`scripts/validate.sh` + policy) e `.vscode/` mínimo.

## Fase 1 — MVP
- Domínio e modelos iniciais (ex.: Usuário, Organização/Conta, Plano/Assinatura).
- Autenticação (sessão/JWT/OAuth2), autorização inicial (RBAC mínimo).
- Tenancy: escolha (single-tenant; multi-tenant por schema/coluna) e implementação.
- Fluxos principais (CRUDs essenciais) com testes de integração.
- UI mínima (se full‑stack) e contratos de API documentados.

## Fase 2 — Observabilidade e Qualidade
- Logs estruturados e correlação por requisição.
- Métricas técnicas (latência p95, erro rate) e de negócio (funis-chave).
- Tracing quando necessário.
- Cobertura alvo; linters e pre-commit conforme stack.
- Scanners: SAST, segredos e vulnerabilidades (sem segredos no repo).

## Fase 3 — Infra e Deploy
- Containerização (Docker/Compose) para dev e build reproduzível.
- Banco e migrações versionadas (ex.: Prisma/Alembic).
- Staging com variáveis seguras e segredos no provider.
- Deploy e rollback documentados; backups e restauração testados.

## Fase 4 — Performance e Segurança
- Caching/paginação e limites de consulta.
- Hardening de headers, CORS e rate‑limit.
- A11y onde aplicável; otimizações de payload/latência.

## Fase 5 — Escala e DX
- Filas/jobs (ex.: Redis, Celery/BullMQ) para workloads assíncronos.
- Dashboards/alertas e documentação de API (OpenAPI/GraphQL schema).
- DX: scripts e docs consistentes; tempos de build/teste sob controle.

## Fase 6 — Release e Manutenção
- Versionamento semântico e notas de release.
- Backups/retentiva e testes periódicos de restauração.
- Revisão de SLOs e endividamento técnico.

## Segurança (transversal)
- Gestão de segredos fora do repo; rotacionar periodicamente.
- Princípio do menor privilégio; auditoria de permissões.
- Proteções OWASP (CSRF, XSS, injections) e validações no backend.

## Dicas práticas
- Mantenha PRs pequenos com escopo claro e validação listada.
- Se alterar `src/**`, atualize `tests/**` e `docs/**` no mesmo PR.
- Não altere `secrets/**` e `infra/prod/**` sem aprovação dos CODEOWNERS.

