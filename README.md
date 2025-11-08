# ZapPro MVP - SaaS Organização para Construção Civil

[![CI/CD Status](https://github.com/zapprosite/zappro-mvp/actions/workflows/ci.yml/badge.svg)](https://github.com/zapprosite/zappro-mvp/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/zapprosite/zappro-mvp/branch/main/graph/badge.svg)](https://codecov.io/gh/zapprosite/zappro-mvp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/downloads/)
[![Node 20+](https://img.shields.io/badge/Node-20%2B-green)](https://nodejs.org/)

**Descrição:** SaaS robusto para gestão de projetos em construção civil, com automatização via LLM Agents, gateway de APIs, e CI/CD DevOps Senior.

**Stack:** FastAPI + Next.js 15 + PostgreSQL + Docker Compose + GitHub Actions + Codex CLI MCP

---

## Sumário

- [Início Rápido](#início-rápido)
- [Validação Rápida](#validação-rápida)
- [CICD Architecture](#cicd-architecture)
- [Secrets & Configuração](#secrets--configuração)
- [Comandos Úteis](#comandos-úteis)
- [Documentação Técnica](#documentação-técnica)
- [DevOps Standards Compliance](#devops-standards-compliance)
- [Próximos Passos](#próximos-passos)
- [Suporte & Contribuindo](#suporte--contribuindo)
- [Getting Help](#getting-help)
- [License](#license)
- [Contato](#contato)

## Início Rápido

### Pré-requisitos
- Python 3.11+
- Node.js 20+
- Docker Compose 2.0+
- WSL2 (Windows) ou Linux/macOS
- GitHub CLI (`gh auth login`)

### Setup Local

```bash
# Clone e setup
git clone https://github.com/zapprosite/zappro-mvp.git
cd zappro-mvp

# Backend
python -m venv venv
source venv/bin/activate  # WSL/Linux
# ou: venv\Scripts\activate (Windows CMD)
pip install -r requirements.txt
make lint
make test

# Frontend
cd frontend
npm install
npm run dev  # localhost:3000

# Docker Compose completo
docker compose up -d
# Acesso: http://localhost:8000 (API), http://localhost:3000 (Frontend)
```

### Validação Rápida

```bash
bash scripts/validate.sh       # Lint + tests
bash scripts/smoke_test.sh     # Containers + E2E
python3 scripts/loop_guard.py  # Detecção de loops
```

---

## CICD Architecture

### CI Pipeline (Lint, Test, Security, Coverage)
- **Trigger:** PRs em qualquer branch, pushes em main
- **Jobs Paralelos:**
  - Backend: Python 3.11, 3.12 (matrix)
  - Frontend: Node 20, 22 (matrix)
  - Security: Ruff, Bandit, npm audit, secret scan
  - Tests: pytest (Backend 26 testes), Playwright (E2E)
  - Coverage: Codecov report (threshold 80%)
- **Artifacts:** Coverage reports, test results
- **Status:** [![CI Workflow](https://github.com/zapprosite/zappro-mvp/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/zapprosite/zappro-mvp/actions/workflows/ci.yml)

### CD Pipeline (Deploy Preview + Production)
- **Trigger:** Merge em main (production), PR aberta (preview)
- **Jobs:**
  - Build & Push Docker images para GHCR
  - Deploy Staging preview: \`https://preview-{pr-number}.zappro.site\`
  - Deploy Production: \`https://app.zappro.site\` (main branch only)
  - Notify Slack/email com status
- **Status:** [![CD Workflow](https://github.com/zapprosite/zappro-mvp/actions/workflows/cd.yml/badge.svg?branch=main)](https://github.com/zapprosite/zappro-mvp/actions/workflows/cd.yml)

---

## Secrets & Configuração

### GitHub Actions Secrets (Requerido para CD)
Configure via `gh secret set`:
```bash
gh secret set SLACK_WEBHOOK_URL --body "https://hooks.slack.com/..." --repo zapprosite/zappro-mvp
gh secret set SMTP_SERVER --body "smtp.gmail.com" --repo zapprosite/zappro-mvp
gh secret set SMTP_PORT --body "587" --repo zapprosite/zappro-mvp
gh secret set SMTP_USERNAME --body "ci@zappro.site" --repo zapprosite/zappro-mvp
gh secret set SMTP_PASSWORD --body "YOUR_APP_PASSWORD" --repo zapprosite/zappro-mvp
gh secret set GHCR_TOKEN --body "$(gh auth token)" --repo zapprosite/zappro-mvp
gh secret set PREVIEW_BASE_URL --body "https://preview.zappro.site" --repo zapprosite/zappro-mvp
gh secret set PRODUCTION_URL --body "https://app.zappro.site" --repo zapprosite/zappro-mvp
gh secret set CODECOV_TOKEN --body "YOUR_CODECOV_TOKEN" --repo zapprosite/zappro-mvp
```

[!WARNING]
Nunca abra issues públicas para reportar vulnerabilidades. Use security@zappro.site.

### Variáveis Locais (.env.example)
```env
# Backend
DATABASE_URL=postgresql://user:pass@localhost:5432/zappro_db
SECRET_KEY=your-secret-key-here-min-32-chars
DEBUG=false

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000

# Secrets (NUNCA versionados — só em GitHub Actions)
SLACK_WEBHOOK_URL=https://hooks.slack.com/...
SMTP_PASSWORD=app-specific-password
GHCR_TOKEN=ghcr_your_token_here
```

---

## Comandos Úteis

### Backend
```bash
make lint        # Ruff + Black + isort
make test        # Pytest (26 testes)
make security    # Bandit + pip-audit
make format      # Black + isort auto-format
```

### Frontend
```bash
cd frontend
npm run lint     # ESLint + TypeScript
npm run test     # Vitest
npm run build    # Next.js production build
npm run dev      # Development server (localhost:3000)
```

### Docker
```bash
docker compose up -d              # Inicia containers
docker compose logs -f            # Logs em tempo real
docker compose exec zappro-api make test  # Roda teste dentro do container
docker compose down               # Destrói containers
```

### Scripts de Automação
```bash
bash scripts/validate.sh          # Validação completa (lint + test)
bash scripts/smoke_test.sh        # Testes de containers + E2E
bash scripts/deploy.sh staging    # Deploy para staging (preview)
bash scripts/deploy.sh production # Deploy para produção
bash scripts/secret-scan.sh       # Escaneia secrets versionados
bash scripts/policy-check.sh      # Verifica compliance de policies
```

---

## Documentação Técnica

### Documentação Completa
- **[docs/AGENTS.md](./docs/AGENTS.md)** — Agent Configuration para Codex CLI, CICD Rules, Security
- **[docs/SECURITY.md](./docs/SECURITY.md)** — Security policy, vulnerability reporting, compliance
- **[docs/WORKFLOW.md](./docs/WORKFLOW.md)** — Git workflow, branching, PR process
- **[docs/DECISION.md](./docs/DECISION.md)** — Matriz de decisão (Refactor vs Rewrite)
- **[docs/LOG.md](./docs/LOG.md)** — Changelog e histórico de commits
- **[tutor/prompt.md](./tutor/prompt.md)** — Prompt de contexto para LLM tutors
- **[tutor/progress.state.md](./tutor/progress.state.md)** — Status de progresso das features

### Guias de Operação
- **[docs/how-to-run.md](./docs/how-to-run.md)** — Como rodar localmente
- **[docs/metodo-contrato-codex-cli-com-mcp.md](./docs/metodo-contrato-codex-cli-com-mcp.md)** — Contrato para usar Codex CLI com MCP

---

## DevOps Standards Compliance

### Governança Anti-Alucinação
✅ **Loop Guard ativo:** Detecta repetições via \`scripts/loop_guard.py\`
✅ **Context sempre lido:** \`docs/AGENTS.md\`, \`tutor/\` loaded antes de qualquer tarefa
✅ **Commits rastreáveis:** Conventional messages (feat:, fix:, docs:, ci:)
✅ **Zero secrets versionado:** \`.env.example\` only, secrets em GitHub Actions

### Security Scanning
✅ **Pre-push:** Secret scan bloqueia versionamento de tokens
✅ **CI Pipeline:** Ruff + Bandit + npm audit + OWASP Dependency Check
✅ **Vulnerability Reporting:** \`security@zappro.site\` (48h response SLA)

### Testing & Coverage
✅ **Unit Tests:** 26 testes com 80%+ coverage (threshold enforced)
✅ **E2E Tests:** Playwright smoke tests em CI
✅ **Integration:** Tests rodam contra DB real em containers

### Deployment Gates
✅ **PR Preview:** Automatically deploy preview ambiente para PRs
✅ **Production:** Main branch only, requer aprovação de 2 reviewers
✅ **Rollback:** Git revert automático se CD falha

---

## Próximos Passos

### Curto Prazo (Esta Semana)
- [ ] Habilitar GitHub Projects automation para Kanban
- [ ] Configurar todos secrets GitHub Actions (\`gh secret set ...\`)
- [ ] Testar deploy preview em staging
- [ ] Mergear \`ci-cd-bootstrap\` para main com revisão

### Médio Prazo (2 Semanas)
- [ ] Aplicar Matriz DECISION aos módulos críticos (auth, tasks, bootstrap)
- [ ] Migrar imports unused (Pydantic V2 ConfigDict, FastAPI lifespan)
- [ ] Integrar Codecov dashboard
- [ ] Setup GitHub Projects com rules automáticas

### Longo Prazo (1 Mês)
- [ ] Integrar Kestra + N8N para workflow automation
- [ ] Implementar multi-agent system com Codex Cloud
- [ ] Custom MCPs para domínio específico (construção civil)
- [ ] Setup production environment com failover

---

## Suporte & Contribuindo

### Report de Issues
- Bugs: [issues/new?template=bug_report.md](https://github.com/zapprosite/zappro-mvp/issues/new?template=bug_report.md)
- Features: [issues/new?template=feature_request.md](https://github.com/zapprosite/zappro-mvp/issues/new?template=feature_request.md)
- Security: \`security@zappro.site\` (não abra issue)

### Como Contribuir
1. Clone: \`git clone https://github.com/zapprosite/zappro-mvp.git\`
2. Branch: \`git checkout -b feature/meu-feature\`
3. Commit: \`git commit -m "feat: descrição"\`
4. Validate: \`bash scripts/validate.sh\`
5. Push & PR: \`git push origin feature/meu-feature\`

---

## Getting Help

[!TIP]
Para dúvidas gerais, use Issues do GitHub com label `question`. Para vulnerabilidades, envie email para security@zappro.site (não abra issue pública).

---

## License
MIT License — veja https://opensource.org/licenses/MIT para detalhes.

## Contato
- **Founder:** Will Refrimix (@willrefrimix)
- **Tech Lead:** @jpmarcenaria
- **Email:** dev@zappro.site
