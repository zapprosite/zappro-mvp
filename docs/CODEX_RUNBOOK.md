# CODEX RUNBOOK — Overnight Execution (Lean)

Objetivo: executar Codex CLI (GPT-5, reasoning high) com MCPs, sem alucinação/loops, rumo ao deploy rápido.

## Guardrails
1. Ler: PRD.md, docs/INDEX.md, tutor/TUTOR_MASTER_PROMPT.md.
2. Sem placeholders.
3. Validar antes de commit: `make lint && make test`.
4. 1 mudança lógica = 1 commit = 1 PR.
5. Sem segredos no código.
6. Travou >30min → parar, `git reset --hard HEAD`, registrar em `docs/_archive/LOG.md`, seguir próxima.

## MCPs
github, git, filesystem, shell, task_manager, playwright, context7, brave_search.

## Validação
- Lint: `make lint` (0 erros)
- Unit: `make test` (26 verdes, cov ≥80%)
- E2E (se mexeu no frontend): `make test-e2e`
- Segurança (se mudou deps): `make sec-scan`

## Playlist (executar atomicamente)
### T1 — FastAPI lifespan (src/main.py)
- Fixes: migrar @app.on_event → `lifespan`; `GET /healthz` = {"status":"ok"}.
- Validar: `make lint && make test`; `curl :8000/healthz | jq .status=="ok"`.
- Commit: `refactor(api): migrate to FastAPI lifespan and add /healthz`.
- MCP: filesystem → github → git → shell.

### T2 — Auth assíncrono (src/utils/auth.py)
- Fixes: JWT async; erros Missing/Expired/Invalid token; testes `tests/test_auth.py`.
- Validar: `make lint && pytest -q tests/test_auth.py`.
- Commit: `fix(auth): rewrite JWT utils async + tests`.

### T3 — Pydantic v2 (src/models/, src/schemas/)
- Fixes: migrar p/ v2; usar `model_validate/model_dump`.
- Validar: `make lint && make test`.
- Commit: `refactor(models): migrate to Pydantic v2`.

### T4 — Docker healthchecks (docker-compose.yml)
- Fixes: healthcheck da API com /healthz; ordem de dependências saudável.
- Validar: `docker compose up -d && docker compose ps`; `docker inspect api ... | jq .Status=="healthy"`.
- Commit: `ci(docker): add healthchecks and deps order`.

### T5 — CI hardening (.github/workflows/*)
- Enhancements: Codecov ≥80% + `scripts/secret-scan.sh` no PR.
- Validar: checks verdes no PR.
- Commit: `ci(workflows): enable codecov and enforce secret-scan`.

### T6 — Frontend bootstrap (frontend/)
- Fixes: Next.js 15 App Router; “/” lista projetos via `/api/projects`.
- Validar: `make lint`; Playwright: heading “Projects”.
- Commit: `feat(web): bootstrap Next.js 15 home with projects list`.

### T7 — E2E smoke (playwright)
- Enhancements: `tests/e2e/smoke.spec.ts` valida “/” e “/healthz”; CI.
- Validar: `make test-e2e`.
- Commit: `test(e2e): add smoke test for home and healthz`.

### T8 — API docs (docs/api-endpoints.md)
- Enhancements: documentar rotas FastAPI com exemplos.
- Validar: `grep "^## " docs/api-endpoints.md`.
- Commit: `docs(api): add api-endpoints.md`.

## Orquestração overnight (tmux)
tmux new -s overnight -d
tmux send-keys -t overnight 'codex -m gpt-5 -c model.reasoning_effort=high --full-auto "[FastAPI lifespan refactor] ..."' C-m
tmux send-keys -t overnight 'codex -m gpt-5 -c model.reasoning_effort=high --full-auto "[Auth async rewrite] ..."' C-m
tmux send-keys -t overnight 'codex -m gpt-5 -c model.reasoning_effort=high --full-auto "[Pydantic v2 migration] ..."' C-m
# observar: tmux attach -t overnight

## Se travar
Parar → `git reset --hard HEAD` → logar em `docs/_archive/LOG.md` → próxima tarefa.
