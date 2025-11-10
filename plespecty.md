# ZapPro — Relatório de Auditoria Técnica (plespecty.md)

> Documento de auditoria detalhado do repositório, cobrindo análise inicial (AGENTS.md → PRD.md → README.md), estado atual, investigação de problemas de conexão em `localhost` (portas `3001` e `3002`), recomendações técnicas e resumo executivo. Inclui timestamps ISO e links para arquivos relevantes.

---

## Metodologia e Timestamps
- Método: leitura dirigida (AGENTS → PRD → README), varredura de configuração (Docker Compose, backend e frontend), verificação de logs e diagnóstico de rede.
- Timestamp da execução: `2025-11-06T12:14:53-03:00` (ISO).
- Timestamps por seção:
  - Análise inicial: `2025-11-06T12:14:53-03:00`
  - Estado atual: `2025-11-06T12:14:53-03:00`
  - Conexões (3001/3002): `2025-11-06T12:14:53-03:00`
  - Recomendações: `2025-11-06T12:14:53-03:00`
  - Resumo executivo: `2025-11-06T12:14:53-03:00`

---

## 1) Análise Inicial

### 1.1 AGENTS.md
- Fonte única do produto: [`PRD.md`](PRD.md) (contrato do produto).
- Regras de contribuição e operação segura: mudanças atômicas, testes + docs junto do código, proibição de segredos em commits.
- Escopo permitido de alterações: `src/**`, `tests/**`, `docs/**`, `README.md`, `CONTRIBUTING.md`, `Makefile`, `scripts/**`, `.github/workflows/**`, `.gitignore`, `.editorconfig`, `AGENTS.md`, `PRD.md`.
- Áreas restritas: `secrets/**`, `infra/prod/**` (dependem de CODEOWNERS).
- Operação: usar buscas rápidas, patches, evitar renomes massivos, manter segurança e validações (`scripts/security-scan.sh`, `scripts/validate.sh`).
- Fluxo de validação: seguir Guia operacional (PRD → plano → bootstrap → validação → PR), CI deve passar, PRs com plano/risco/validação.

Link: [`AGENTS.md`](AGENTS.md)

### 1.2 PRD.md
- Stack alvo completa backend FastAPI + frontend Next.js + Postgres; observabilidade, segurança (JWT/RBAC), workflows/IA.
- Roadmap por fases (F0 → F6) com entregáveis e checklists detalhados.
- Requisitos funcionais (CRUDs de projeto/tarefa/material/usuário/doc, autenticação JWT) e não-funcionais (SLA, LGPD, CORS, rate-limit, headers, A11y, performance).
- Arquitetura alvo e modelo de dados resumido; design de API com versionamento `/api/v1/`.
- Desenvolvimento e ambientes (make targets, variáveis por ambiente) e CI/CD.

Link: [`PRD.md`](PRD.md)

### 1.3 README.md
- Baseline Fase 0 (Bootstrap) com endpoints de saúde, lint/test, docs mínimas e Docker Compose.
- Comandos principais:
```bash
make dev               # inicia API FastAPI (uvicorn --reload)
cd frontend && npm run dev
make lint              # ruff + black --check + isort --check
make fmt               # formatação
make test              # pytest
bash scripts/pre-commit.sh
bash scripts/validate.sh
make security          # ruff/bandit/pip-audit/secret scan/npm audit
cd frontend && npm run test:e2e  # Playwright security smoke
```
- Docker Compose expõe: API `http://localhost:8000/health`, Frontend `http://localhost:3000`, Postgres `5432`.
- Segurança: middleware adiciona CSP, headers, rate-limit e request-id; Playwright valida cabeçalhos; CVE conhecido em `starlette 0.38.6` aguardando bump do FastAPI.

Link: [`README.md`](README.md)

---

## 2) Documentação do Estado Atual

### 2.1 Estrutura do Repositório (macro)
- `src/` — API FastAPI com middleware de segurança e endpoint `/health`.
- `tests/` — Pytest com saúde/headers.
- `frontend/` — Next.js 15 com middleware CSP.
- `docker/` — Dockerfiles (`api.Dockerfile`, `frontend.Dockerfile`).
- `docker-compose.yml` — serviços `api`, `frontend`, `postgres`.
- `scripts/` — automações (backup, restore, validate, security-scan, dependency-watch, daily-health).
- `docs/` — documentação (como rodar, arquitetura, segurança).
- Logs: `security.log`, `audit.log`.

### 2.2 Funcionalidades Implementadas
- Backend:
  - Endpoint `GET /health` retornando `status`, `version`, e parâmetros de rate-limit.
  - Middleware de segurança com: CORS, Trusted Hosts, headers (CSP, X-Frame-Options, etc.), rate limit (janela fixa), rastreador de `request-id` com detecção de colisões.
  - Configuração via env (`ZAPPRO_*`) com parsing seguro de listas; CORS default permitindo `http://localhost:3000`.
- Frontend:
  - Middleware CSP com nonce; `connect-src 'self'` por padrão.
  - `dev` em `http://localhost:3000` (Turbopack).
- Infra/Automação:
  - Docker Compose: API `8000`, Frontend `3000`, Postgres `5432`.
  - Scripts de segurança, backup/restore, validação e monitoramento diário.
  - Playwright testa headers de segurança e `/health`.

### 2.3 Dependências e Requisitos
- Backend (`requirements.txt`): `fastapi`, `uvicorn`, `pydantic`, `pydantic-settings`, `sqlalchemy`, `alembic`, `pytest`, `httpx`, etc.
- Frontend (`package.json`): Next.js 15, TS, Tailwind v4, shadcn/ui, Zustand, TanStack Query, Playwright.
- Pré-requisitos (dev): Python 3.11+, Node 20+, Docker Compose (opcional), `make`, `git`, `curl`.

### 2.4 Estado Atual do Desenvolvimento
- Fase 0 (Bootstrap) ativa: API/Frontend com `/health`, pipelines de lint/test/scan, Docker Compose funcional.
- Logs indicam segurança ok, CVE conhecido em `starlette` pendente de correção upstream.
- Funcionalidades de Fase 1 (autenticação/CRUDs) ainda não implementadas.

Links: [`docker-compose.yml`](docker-compose.yml), [`src/main.py`](src/main.py), [`frontend/middleware.ts`](frontend/middleware.ts), [`docs/CODEX_RUNBOOK.md`](docs/CODEX_RUNBOOK.md), [`docs/api-endpoints.md`](docs/api-endpoints.md), [`security.log`](security.log), [`audit.log`](audit.log)

---

## 3) Análise de Problemas de Conexão (localhost:3001 e 3002)

### 3.1 Achados na Configuração
- Não há referências a `3001` ou `3002` no repositório (busca global sem ocorrências).
- Portas padrão atuais:
  - API: `8000` (`EXPOSE 8000` e `command --port 8000`).
  - Frontend: `3000` (`EXPOSE 3000`, `npm run dev`).
  - Compose permite variáveis: `API_PORT` (default 8000) e `FRONTEND_PORT` (default 3000).
- Possível causa de erro ao tentar `3001/3002`:
  - Nenhum serviço escutando nessas portas.
  - CSP do frontend: `connect-src 'self'` bloqueia requisições cross-origin (por exemplo, de `http://localhost:3000` para `http://localhost:3001/3002`).
  - CORS do backend: `allow_origins` default só inclui `http://localhost:3000`; origens `3001/3002` seriam bloqueadas.

### 3.2 Verificações de Rede (comandos sugeridos)
- Windows PowerShell:
```powershell
# Portas ativas
netstat -ano | findstr ":3001"
netstat -ano | findstr ":3002"
netstat -ano | findstr ":3000"
netstat -ano | findstr ":8000"

# Teste direto
Test-NetConnection -ComputerName localhost -Port 3001
Test-NetConnection -ComputerName localhost -Port 3002

# Regras de firewall por porta
Get-NetFirewallRule | Get-NetFirewallPortFilter | Where-Object { $_.LocalPort -match "3001|3002" } | Format-Table -AutoSize
```
- Linux/WSL:
```bash
ss -ltnp | grep -E ":(3001|3002|3000|8000)"
sudo ufw status
sudo iptables -L -n | grep -E "3001|3002"

# Docker
docker ps --format "table {{.Names}}\t{{.Ports}}"
```

### 3.3 Logs e Serviços
- Verificar `logs/` (se existentes), `security.log` e `audit.log` por eventos de rede.
- Confirmar se Docker está ativo (`docker info`) e se os serviços `api`/`frontend` estão “UP”.

### 3.4 Ajustes de Configuração (para permitir 3001/3002 em desenvolvimento)
- CSP (frontend): permitir chamadas para API/serviços auxiliares adicionando hosts em `connect-src` via env.
  - Exemplo (dev):
```ts
// frontend/middleware.ts — ajustar connect-src dinamicamente
const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
const EXTRA_CONNECT = process.env.NEXT_PUBLIC_CONNECT_SRC ?? "http://localhost:3001 http://localhost:3002";
const directives = [
  `default-src 'self'`,
  `script-src 'self'`,
  `style-src ${styleSrc}`,
  `img-src ${IMG_SRC.join(" ")}`,
  `font-src ${FONT_SRC.join(" ")}`,
  "object-src 'none'",
  "base-uri 'self'",
  "frame-ancestors 'none'",
  `connect-src 'self' ${API_URL} ${EXTRA_CONNECT}`,
].join("; ");
```
- CORS (backend): incluir origens adicionais via env:
```bash
# .env (exemplo)
ZAPPRO_CORS__allow_origins=["http://localhost:3000","http://localhost:3001","http://localhost:3002"]
# ou
ZAPPRO_CORS__allow_origins=http://localhost:3000,http://localhost:3001,http://localhost:3002
```

---

## 4) Recomendações de Melhorias (com priorização e complexidade)

- Abrir CSP `connect-src` para API/serviços necessários em dev.
  - Justificativa: evita bloqueio por CSP ao chamar `8000/3001/3002`.
  - Prioridade: Alta — habilita integração local.
  - Complexidade: Baixa.

- Ampliar CORS `allow_origins` no backend para `3001/3002` (somente dev).
  - Justificativa: evita `CORS` bloqueando chamadas a partir de origens não listadas.
  - Prioridade: Alta.
  - Complexidade: Baixa.

- Centralizar URL da API no frontend (`NEXT_PUBLIC_API_URL`) e usar fetch/cliente apontando para ela.
  - Justificativa: reduz acoplamento, simplifica troca de endpoints e evita hardcode de portas.
  - Prioridade: Alta.
  - Complexidade: Média.

- Adicionar proxy interno no Next.js (rota `/api/*`) para backend em dev.
  - Justificativa: mantém same-origin; reduz necessidade de abrir CORS/CSP amplo.
  - Prioridade: Média.
  - Complexidade: Média.

- Documentar `.env` com `API_PORT` e `FRONTEND_PORT` e cenários alternativos (3001/3002).
  - Justificativa: reduz ambiguidade; padroniza execução.
  - Prioridade: Média.
  - Complexidade: Baixa.

- Monitorar e mitigar CVEs (`starlette`/`fastapi`) com bump assim que disponível.
  - Justificativa: segurança.
  - Prioridade: Alta.
  - Complexidade: Baixa.

- Introduzir backend de rate-limit via Redis (produção/staging).
  - Justificativa: escalabilidade/robustez.
  - Prioridade: Média.
  - Complexidade: Média‑Alta.

---

## 5) Relatório Final — Resumo Executivo

- Estado atual completo:
  - Fase 0 concluída: API/Frontend com `/health`, segurança básica (headers, CORS, rate-limit), CI/Playwright e Docker Compose.
  - Infra local usa `8000` (API) e `3000` (frontend); `3001/3002` não são utilizados.
  - Logs mostram scans OK e CVE conhecido pendente.

- Principais desafios técnicos:
  - Bloqueios por CSP (`connect-src 'self'`) e CORS em dev ao chamar diferentes portas.
  - Ambiguidade de portas `3001/3002` sem serviços escutando.
  - Dependência indireta com CVE (aguardar patch).

- Soluções propostas para problemas de conexão:
  - Definir `NEXT_PUBLIC_API_URL` e abrir `connect-src` para `8000/3001/3002` quando necessário.
  - Ampliar CORS `allow_origins` para origens reais do dev.
  - Opcional: usar proxy interno Next.js para manter same-origin.
  - Validar portas e firewall com os comandos listados (Windows/WSL/Linux).

- Roadmap de melhorias sugeridas:
  - Imediatas (Alta): ajustar CSP/CORS; documentar `.env` e portas.
  - Próximas (Média): proxy Next.js; centralizar configuração de API.
  - Contínuas: vigilância de CVEs, avaliar Redis p/ rate-limit em ambientes não‑dev.

---

## Referências Rápidas
- [`docker-compose.yml`](docker-compose.yml)
- [`src/main.py`](src/main.py)
- [`src/config.py`](src/config.py)
- [`frontend/middleware.ts`](frontend/middleware.ts)
- [`docs/CODEX_RUNBOOK.md`](docs/CODEX_RUNBOOK.md)
- [`docs/api-endpoints.md`](docs/api-endpoints.md)
- [`AGENTS.md`](AGENTS.md) • [`PRD.md`](PRD.md) • [`README.md`](README.md)
- Logs: [`security.log`](security.log), [`audit.log`](audit.log)

---

## Anexo — Comandos úteis

```bash
# Docker
cp .env.example .env
docker compose up --build

# Backend
make install && make dev
curl -sf http://localhost:8000/health

# Frontend
cd frontend && npm install && npm run dev
curl -sf http://localhost:3000/health
```

> Observação: em dev, se desejar usar `3001/3002`, ajuste `FRONTEND_PORT`/`API_PORT` no Compose e atualize CSP/CORS conforme indicado.
