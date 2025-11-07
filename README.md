# ZapPro — Bootstrap da Plataforma

> **Antes de iniciar:** revise o guia [`guia-secrets.md`](guia-secrets.md) para configurar variáveis de ambiente e segredos com segurança.

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

## CI/CD Automatizado
- `ci.yml` roda em matriz Python 3.11/3.12 + Node 20/22, executa lint/format, testes com cobertura, Playwright E2E e `make security`. Artifacts (`coverage.xml`, relatórios JUnit e Playwright) ficam anexados na execução para auditoria.
- `cd.yml` constrói e publica imagens no GHCR (`docker/api.Dockerfile` e `docker/frontend.Dockerfile`) e chama `scripts/deploy.sh` para materializar o manifesto do deploy. Pull Requests recebem prévia em `environment` *staging* (comentário automático com tags das imagens) e `main` dispara o deploy do *environment* `production`.
- Aprovações ou rejeições de PR disparam alertas: Slack via `SLACK_WEBHOOK_URL` (Incoming Webhook) e email via `CI_SMTP_*` (server, port, username, password, from, recipients). Configure esses segredos somente pelo GitHub Actions Secrets.
- Antes de abrir PR execute localmente `bash scripts/security-scan.sh` e `bash scripts/validate.sh` para reproduzir os estágios críticos da pipeline; o log consolidado fica em `logs/`.

## Automação com LLMs e Proteção de Segredos
- O contrato para qualquer agente continua sendo `PRD.md` + `AGENTS.md`. A nova `docs/AGENTS.md` resume fluxo seguro (planeje → bootstrap → valide → gere PR) e cita limitações como ausência de rede e bloqueio de credenciais.
- Use `.env.example` como única fonte versionada de variáveis locais (`cp .env.example .env`). Ajuste valores reais apenas fora do Git e utilize cofres (Vault, GitHub Environments, Doppler). Comentários no arquivo listam os segredos que **devem** viver em Secrets do GitHub (`SLACK_WEBHOOK_URL`, `CI_SMTP_*`, tokens de deploy).
- Antes de compartilhar resultados de um agente, rode `bash scripts/secret-scan.sh` (incluso em `scripts/security-scan.sh`). O pipeline e o script falham se detectarem padrões de chave/segredo.
- Nunca cole credenciais nos prompts; troque por placeholders (`<token>`). Para liberar novos agentes ou fluxos, documente a heurística em `docs/AGENTS.md` e referencie no PR.

## GitHub Projects + Tracking Automatizado
1. Crie um quadro GitHub Projects com colunas `Backlog`, `Em andamento`, `Revisão`, `Pronto para deploy`.
2. Configure automações nativas: mover para `Revisão` quando houver PR vinculado e para `Pronto para deploy` quando o GitHub Check `CI / policy` e o `CD / deploy production` estiverem verdes.
3. Agentes e humanos adicionam o campo `Project` diretamente no PR ou Issue. Os comentários enviados pelo `deploy-preview` ajudam o time a validar staging antes da promoção.
4. Para integrações com ferramentas externas (Linear, ClickUp), consuma a API de Projects após a conclusão do workflow (`workflow_run`) e sincronize status baseado nos artifacts/ambientes registrados.

## Próximos Passos (Fase 1)
1. Definir modelos de domínio e migrations iniciais.
2. Implementar autenticação/JWT e módulos de obras, equipes e materiais.
3. Conectar frontend aos endpoints reais e montar dashboards.

> ⚠️ Só adicionar variáveis sensíveis reais após configurar Vault/segredos da infra. Use `.env.example` como referência.
# zappro-mvp
