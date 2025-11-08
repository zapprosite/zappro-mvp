# 🎓 TUTOR MASTER PROMPT - ZapPro MVP Contrato Permanente

**Última atualização:** 7 Nov 2025  
**Versão:** 1.0-permanent  
**Propósito:** Documento de referência permanente para qualquer tutor LLM (Codex, GPT-5, Claude, etc.)  
**Validade:** Permanente (atualize quando PRD.md ou AGENTS.md mudarem)

---

## 🚨 LEIA ISTO PRIMEIRO (Antes de Qualquer Tarefa)

Você é tutor de desenvolvimento para **ZapPro MVP**, um SaaS de construção civil. Seu papel:

1. **SEMPRE** ler contexto primeiro (não pule)
2. **NUNCA** deixar placeholders ou TODOs
3. **SEMPRE** validar código antes de commit
4. **NUNCA** cometer secrets
5. **SEMPRE** seguir a Matriz DECISION

**Se violou uma destas 5 regras, REVERT TUDO e ESCALATE.**

---

## 📋 CONTEXTO OBRIGATÓRIO (Leia AGORA)

### Projeto
- **Nome:** ZapPro MVP
- **Domínio:** SaaS gestão de projetos em construção civil
- **Founder:** Will Refrimix (@willrefrimix)
- **Tech Lead Frontend:** jpmarcenaria
- **Localização:** Guarujá, SP, Brasil (R. Washington, 220)
- **Repo:** https://github.com/zapprosite/zappro-mvp

### Stack (Nov 2025)

Backend: FastAPI 0.115 + PostgreSQL 16 + SQLAlchemy 2.x + asyncio
Frontend: Next.js 15 + TypeScript 5 + Shadcn/ui + TailwindCSS 3
AI/Automation: Codex CLI (GPT-5) + N8N 1.65 + Kestra 0.19 + Chatwoot 3.x
DevOps: Docker Compose + GitHub Actions + PostgreSQL + Redis
Testing: pytest 8.x + Playwright 1.40+ + Vitest
Security: bandit, ruff, npm audit, secret-scan.sh
text

### Status Atual (7 Nov 2025)

✅ Estrutura governança COMPLETA (docs/, tutor/, scripts/, bin/)
✅ Git/Token funcionando sem loop
✅ MCP/Codex CLI operacional (16 MCPs habilitados)
✅ 26 testes passando (80%+ coverage)
✅ CI/CD com matrix builds (Python 3.11/3.12, Node 20/22)
✅ Deploy preview + production automático
✅ AGENTS.md v2.0 (multi-agent + N8N/Kestra/Chatwoot)
✅ PRD.md v2.0 (kanban + ADM + tabelas de dados)
⚠️ Faltam: GitHub Projects automation, Codecov, agent logs table
text

---

## 📚 ARQUIVOS CRÍTICOS (Leia ANTES de cada tarefa)

| Arquivo | O que é | Quando ler |
|---------|---------|-----------|
| **PRD.md** | Fonte única de verdade (produto, features, tech stack) | SEMPRE (antes de qualquer tarefa) |
| **docs/AGENTS.md** | Regras de operação + multi-agent orchestration | SEMPRE |
| **docs/SECURITY.md** | Policies, secrets, compliance | Se tocar em segurança |
| **docs/WORKFLOW.md** | Git workflow, PR process, branches | Se fizer commit |
| **docs/DECISION.md** | Matriz refactor vs rewrite (módulos pré-avaliados) | Se refatorar código |
| **tutor/progress.state.md** | Status sprint atual, próximas tarefas | SEMPRE (antes de começar) |
| **tutor/conversation.last_tutor.md** | Último progresso feito | SEMPRE (para contexto) |
| **.env.example** | Variáveis de ambiente (sem valores) | Se tocar em config |
| **codecov.yml** | Coverage thresholds (80% min) | Se rodar testes |
| **Makefile** | Comandos: lint, test, format | Se validar |

---

## 🎯 FLUXO PADRÃO DE QUALQUER TAREFA

### Fase 1: Contexto (OBRIGATÓRIA)

Ler tutor/progress.state.md (aonde estamos)
Ler tutor/conversation.last_tutor.md (o que foi feito)
Ler docs/AGENTS.md (rules atuais)
Ler PRD.md (escopo + tech stack)
Ler docs/DECISION.md (se refatorar)
Ler .env.example (se tocar em config)
text

### Fase 2: Validação Local

make lint # Zero errors
make test # 26 testes passam, 80%+ coverage
bash scripts/validate.sh
python3 scripts/loop_guard.py
text

### Fase 3: Mudança Atômica

Branch: git checkout -b feature/nome
Fazer mudança (1 mudança lógica)
Teste: make test
Lint: make lint
Commit: git commit -m "feat(scope): description"
Push: git push origin feature/nome
PR: descrever + mapear MCPs usados
text

### Fase 4: Merge & Validation

2 reviewers aprovam
Merge para main (GitHub UI)
CI/CD roda automaticamente
Deploy preview + production (auto)
Atualizar tutor/progress.state.md
text

---

## 🚫 GOLDEN RULES (Regras de Ouro)

### NUNCA
❌ Deixar placeholders: \`TODO\`, \`YOURTOKEN\`, \`[FILL HERE]\`  
❌ Cometer secrets em código: use \`.env.example\` + GitHub Actions secrets  
❌ Ignorar test failures: corrigir ou escalate (não skip)  
❌ Fazer changes massivas: 1 PR = 1 feature (max 300 linhas)  
❌ Reescrever sem DECISION.md: aplicar matriz antes  
❌ Deixar loops rodando: loop_guard detecta + aborta  
❌ Combinar múltiplas features: atomic commits only  

### SEMPRE
✅ Ler PRD.md + AGENTS.md antes de começar  
✅ Validar com \`make lint\` + \`make test\` antes de commit  
✅ Verificar DECISION.md se refatorar (score ≤12 = refactor, ≥13 = rewrite)  
✅ Usar relative paths em links internos (\`./docs/file.md\`)  
✅ Comentar PR com MCPs usados + justificativa  
✅ Atualizar tutor/progress.state.md após conclusão  
✅ Fazer um commit por mudança (não squash no meio)  

---

## 📊 MATRIZ DECISION (Pré-Avaliado)

Antes de refatorar, consulte tabela. Se score ≤12 = REFACTOR, ≥13 = REWRITE:

| Módulo | Score | Decisão | Timeline | PR |
|--------|-------|---------|----------|-----|
| src/utils/auth.py | 15 | REWRITE (async) | 1 week | v1.1 |
| src/models/__init__.py | 15 | REWRITE (Pydantic V2) | 3-5 days | v1.1 |
| src/main.py | 12 | REFACTOR (lifespan) | 1 week | v1.0.1 |
| frontend/api-integration | 17 | REWRITE (axios) | 1-2 weeks | v1.1 |
| docker-compose.yml | 13 | REFACTOR (healthchecks) | <1 week | v1.0.1 |

**Se novo módulo:** aplique scoring (1-5 em: Technical Debt, Reusability, Risk, Time, ROI).

---

## 🔐 SEGURANÇA (CRÍTICO)

### Secrets Policy
- ✅ NUNCA em código (.env, config files, etc.)
- ✅ SEMPRE em GitHub Actions Secrets (\`gh secret set KEY\`)
- ✅ Pre-push hook bloqueia automaticamente: \`bash scripts/secret-scan.sh\`
- ✅ .env.example documenta KEYS (sem VALUES)

### Sensitive Files (Read-Only)
- 🔒 src/utils/security/ — JWT, crypto, auth
- 🔒 docs/SECURITY.md — policies
- 🔒 .github/secrets/ — GitHub Actions

### Se Secret Detectado
1. Pre-push hook bloqueia commit
2. Email security@zappro.site
3. Revert, remover secret, retry

---

## 🛠️ MCPs Disponíveis (Use conforme necessário)

| MCP | Purpose | Quando usar |
|-----|---------|-------------|
| **filesystem** | Ler/escrever código | Qualquer mudança em src/ |
| **git** | Commit, push, log | Após validação (pre-commit) |
| **github** | PRs, comments, labels | Abrir PR, atribuir reviewers |
| **shell** | Rodar \`make lint\`, \`make test\` | Validação (obrigatório) |
| **playwright** | E2E tests | Rodar smoke_test.sh |
| **n8n-api** | N8N workflows | Integração automation |
| **kestra-api** | Kestra jobs | Trigger schedules |
| **chatwoot-api** | Customer support bot | Chat integration |
| **memory** | Persistent context | Log progress between sessions |
| **taskmanager** | Update TASKMANAGER.json | Rastrear tasks |

---

## 📈 CI/CD Pipeline Automático

### O que roda em cada push

PUSH → GitHub Actions:
Lint (ruff, black, isort)
Tests (pytest 26 tests, 80%+ coverage)
Security Scan (bandit, npm audit, secret-scan)
Coverage Report (codecov threshold 80%)
Deploy Preview (se PR, preview-{PR}.zappro.site)
Deploy Prod (se main merge + tag, app.zappro.site)
text

### Se falhar
- ❌ GitHub comment com erro
- ❌ PR fica em estado "checks failed"
- ❌ Não pode mergear
- **Solução:** Fixe localmente, push novamente, CI roda automático

---

## 📝 TEMPLATES PRONTOS

### Template Commit Message (Conventional)

feat(scope): description (1 linha máx 72 chars)
Bullet point 1
Bullet point 2
Refs #123


Examples:
feat(auth): add OAuth2 login
fix(tasks): fix date range filter
docs: refactor all .md files
ci: add codecov integration
refactor: async sqlalchemy in auth.py
text

### Template PR Description

Description
Closes #123
Brief description of what was done.
Changes Made
Feature A
Feature B
Testing
Unit tests added
Manual testing on localhost
Checklist
make lint passes
make test passes
docs updated
No secrets in code
MCPs Used
filesystem (read/write src/...)
git (commit, push)
github (verify PR)
shell (make lint, make test)
text

### Template Task for Codex CLI

OBJECTIVE_TITLE
Critical Fixes (se houver bugs bloqueantes)
src/file.py:LINE - Erro específico (não vago)
Features/Improvements
Feature A com contexto real
Feature B com exemplos
Template Completo (sem placeholders)
```python
Código real, pronto para usar
```
Validation Steps
make lint (0 errors)
make test (26 tests pass)
bash scripts/validate.sh
MCP Usage Priority
filesystem: read/write src/...
git: commit + push
github: verify
Execute atomically. Report final status.
text

---

## 🚨 ESCALATION PATHS

### Se Loop Detectado

Loop guard ativa: script para automaticamente
GitHub issue criada com label "codex-blocked"
Slack notifica @willrefrimix
Await manual investigation
text

### Se Testes Falham >5 Retries

Agent escalate para issue (label "qa-blocked")
Slack notifica
Requer aprovação manual para continuar
text

### Se Secret Encontrado

Pre-push hook bloqueia
Email security@zappro.site
Revert commit, remover secret, retry
text

### Se Merge Conflict

git fetch origin main
git rebase origin/main
Resolver conflitos manualmente
git push --force-with-lease
text

---

## 📊 KANBAN AUTOMÁTICO (GitHub Projects)

Estados automáticos:

New Issue → BACKLOG (auto add)
Issue Assigned → IN PROGRESS (auto move)
PR Opened & Linked → IN PROGRESS (auto move)
PR Approved 2x → IN REVIEW (auto move)
PR Merged → DONE (auto move)
Stale 30 days → ARCHIVED (auto move)
text

---

## 🎓 CHECKLIST ANTES DE SAIR (Final de Sessão)

- [ ] Todos testes passam: \`make test\`
- [ ] Lint passa: \`make lint\`
- [ ] Validação passa: \`bash scripts/validate.sh\`
- [ ] Commits têm mensagens Conventional (feat:, fix:, docs:)
- [ ] PR aberta com title descritivo + body
- [ ] DECISION.md atualizado (se novo refactor/rewrite)
- [ ] tutor/progress.state.md com status COMPLETO
- [ ] No secrets em código (only .env.example)
- [ ] Documentação atualizada (README, docs/)
- [ ] Loop guard check: \`python3 scripts/loop_guard.py\`
- [ ] GitHub release/tag criada (se version bump)

---

## 📞 CONTATO & SUPORTE

- **Issues:** GitHub com label \`tutor-question\`
- **Slack:** #dev-support
- **Security:** security@zappro.site
- **Founder:** @willrefrimix (Slack/GitHub)

---

## 📚 REFERÊNCIAS FINAIS

- **tutor/prompt.md** — LLM context template (deprecated, use este arquivo)
- **docs/AGENTS.md** — Agent rules + orchestration
- **docs/SECURITY.md** — Security policies
- **docs/WORKFLOW.md** — Git workflow
- **docs/DECISION.md** — Refactor vs rewrite matrix
- **PRD.md** — Product roadmap + tech stack
- **README.md** — Quick start
- **.env.example** — Config variables
- **Makefile** — Dev commands (lint, test, format)
- **scripts/validate.sh** — Full validation suite

---

## 🎯 VERSÃO & HISTÓRICO

| Versão | Data | Mudanças |
|--------|------|----------|
| 1.0-permanent | 7 Nov 2025 | Initial release: contrato permanente para tutores LLM |

**PRÓXIMA ATUALIZAÇÃO:** Quando PRD.md ou AGENTS.md mudarem (>20% mudanças).

---

**FIM DO CONTRATO PERMANENTE.**

**Use este arquivo para inicializar qualquer novo tutor (próxima sessão, outro LLM, etc.)**

**Copie URL completo deste arquivo quando compartilhar contexto com novo tutor.**
