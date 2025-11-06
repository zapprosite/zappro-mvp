# ZapPro — Bootstrap da Plataforma

Baseline da ZapPro para a Fase 0 (Bootstrap) com backend FastAPI 3.11 e frontend Next.js 15. O objetivo é disponibilizar endpoints de saúde, pipelines de lint/test, documentação mínima e infraestrutura local via Docker Compose.

## Stack
- **Backend**: Python 3.11, FastAPI, SQLAlchemy, Alembic, Pytest, Ruff, Black, Isort
- **Frontend**: Next.js 15 (App Router), TypeScript, TailwindCSS v4, shadcn/ui, Zustand, TanStack Query
- **Banco**: PostgreSQL 16 (Docker Compose)
- **CI**: GitHub Actions executando lint, testes, format check e script `scripts/validate.sh`

## Estrutura de Pastas
- `src/` — código da API FastAPI (`src/main.py` com `/health`)
- `tests/` — testes Pytest (verificação de health/version)
- `frontend/` — aplicação Next.js (`/health` expõe mesmo JSON)
- `alembic/` — placeholders para migrations futuras
- `scripts/` — automações (`validate.sh`, `pre-commit.sh`)
- `docker/` — Dockerfiles da API e do frontend
- `docs/` — documentação complementar

## Pré-requisitos
- Python 3.11+
- Node.js 20+
- Docker / Docker Compose (opcional)
- `make`, `curl`, `git`

## Setup Rápido
```bash
make install           # cria venv e instala requirements
cd frontend && npm install
```

## Comandos Principais
```bash
make dev               # inicia API FastAPI (uvicorn --reload)
cd frontend && npm run dev

make lint              # ruff + black --check + isort --check
make fmt               # aplica formatação (ruff fix, isort, black)
make test              # pytest
bash scripts/pre-commit.sh   # lint + test + security scan
bash scripts/validate.sh     # lint, test, healthcheck automatizado
make security          # ruff --unsafe, bandit, pip-audit, secret scan, npm audit
bash scripts/dependency-watch.sh  # monitora updates (pip/npm) e registra em logs/dependency-watch.log
cd frontend && npm run test:e2e  # Playwright security smoke
```

## Docker Compose
```bash
cp .env.example .env
docker compose up --build
```
- API: `http://localhost:8000/health`
- Frontend: `http://localhost:3000` (Next dev server)
- Postgres: `postgres://zappro:change_me@localhost:5432/zappro`

## Health Endpoints
- Backend: `GET http://localhost:8000/health → {"status":"ok","version":"0.1.0"}`
- Frontend: `GET http://localhost:3000/health → {"status":"ok","version":"0.1.0"}`

## Validação Local
```bash
make lint
make test
bash scripts/validate.sh
```
O script liga a API, chama `/health` e encerra o servidor. Log detalhado fica em `logs/`.

## Segurança e Auditoria
- Middleware adiciona CSP, Referrer-Policy, Permissions-Policy, `X-Content-Type-Options`, `X-Frame-Options`, `X-API-Version`, rate-limit configurável (env `ZAPPRO_RATE_LIMIT__*` com TTL/limite) e tratamento de request-id com detecção de colisões; trusted hosts aceitam string ou JSON (`ZAPPRO_ALLOWED_HOSTS`).
- `scripts/security-scan.sh` consolida `ruff --unsafe`, `bandit`, `pip-audit`, `scripts/secret-scan.sh` e `npm audit`. Resultados ficam em `logs/security.log`.
- Playwright (`frontend/tests/security.spec.ts`) valida JSON do `/health` e cabeçalhos de segurança do Next.js.
- `scripts/backup.sh` / `scripts/restore.sh` criam snapshots em `backups/`; `scripts/daily-health.sh` monitora endpoints e ignora ambientes offline.
- `scripts/dependency-watch.sh` registra libs desatualizadas e reforça monitoramento de FastAPI/Starlette (veja `logs/dependency-watch.log`).
- Sample cron/Kestra:
  ```
  0 2 * * * cd /path/zappro && bash scripts/security-scan.sh >> logs/security.log 2>&1
  0 4 * * 1 cd /path/zappro && bash scripts/dependency-watch.sh >> logs/dependency-watch.log 2>&1
  ```
- Conhecido: `pip-audit` reporta CVEs no `starlette 0.38.6` (dependência indireta do FastAPI 0.115). A correção exige aguardar bump do FastAPI; monitore e atualize assim que possível.

## Próximos Passos (Fase 1)
1. Definir modelos de domínio e migrations iniciais.
2. Implementar autenticação/JWT e módulos de obras, equipes e materiais.
3. Conectar frontend aos endpoints reais e montar dashboards.

> ⚠️ Só adicionar variáveis sensíveis reais após configurar Vault/segredos da infra. Use `.env.example` como referência.
# zappro-mvp
