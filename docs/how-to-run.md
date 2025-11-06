# Como rodar

## Pré-requisitos
- Python 3.11+
- Node.js 20+
- Make, Git, Curl
- Docker + Docker Compose (opcional para stack completa)

## Backend (FastAPI)
```bash
make install          # cria venv/ instala requirements.txt
make dev              # uvicorn com reload (porta 8000)
make run              # uvicorn sem reload
make lint             # ruff + black --check + isort --check-only
make fmt              # corrige formatação
make test             # pytest
bash scripts/validate.sh  # lint + test + healthcheck automatizado
make security          # ruff unsafe + bandit + pip-audit + secret scan + npm audit
make backup            # gera artefato em backups/
```

Health: `GET http://localhost:8000/health → {"status":"ok","version":"0.1.0"}`

## Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev           # porta 3000
npm run lint
npm run typecheck
npm run build
npm run start
npm run test:e2e      # Playwright (requer porta 3000 livre)
```

Health: `GET http://localhost:3000/health → {"status":"ok","version":"0.1.0"}`

## Docker Compose
```bash
cp .env.example .env
docker compose up --build
```
- API disponível em `http://localhost:${API_PORT:-8000}`
- Frontend em `http://localhost:${FRONTEND_PORT:-3000}`
- Postgres com usuário/senha `zappro / change_me` (altere via `.env`)

## Dicas
- Logs das automações ficam em `logs/`.
- `scripts/daily-health.sh` pode ser agendado para monitorar `/health` API + frontend.
- `scripts/restore.sh <arquivo>` reaplica backup gerado via `make backup`.
- Ajuste variáveis reais apenas em ambientes seguros (Vault / secrets). `.env.example` usa placeholders.
