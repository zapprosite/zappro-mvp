# PRD — ZapPro Plataforma Full‑Stack (LLM‑Safe)

Este PRD é a única fonte de verdade do produto e guia times e LLMs para evolução segura e padronizada.

***

## 0. Guia de Início: Stack e Dependências

- Linguagem: Python 3.11+
- Framework: FastAPI 0.115+
- Banco de dados: PostgreSQL 16
- ORM/Migrations: SQLAlchemy 2.x + Alembic 1.13+
- Testes: pytest 8.x, httpx, Playwright (frontend)
- Lint/Format: ruff, black, isort
- Empacotamento/Execução: Docker Compose para dev/local, Kubernetes/EKS produção

**Frontend:**
- Framework: Next.js 15, TypeScript 5+
- Forms/UI: Shadcn/ui, TailwindCSS, Zustand/TanStack Query
- Testes: Playwright
- Lint: eslint, prettier

**AI e Automações:**
- LangChain 1.0, LangGraph 1.0+
- Kestra (>=0.19), n8n (>=1.65)

**Outros:**
- CI/CD: GitHub Actions, FluxCD
- Containerização: Docker, docker-compose
- IaC: Pulumi/Terraform
- Observabilidade: Sentry, Datadog, Posthog, LangSmith
- Gerenciamento de segredos: Vault

**Checklist Bootstrap:**
- [ ] README.md atualizado stack rodando e comandos
- [ ] docs/how-to-run.md com comandos concretos de exec/test/build
- [ ] Makefile ou justfile (`fmt`, `lint`, `test`, `dev`, `run`)
- [ ] src/ scaffold mínimo + health-check endpoint
- [ ] Teste mínimo health/version
- [ ] .gitignore, .editorconfig, AGENTS.md, .codex/policy.json

***

## 1. Visão Geral

- Nome: ZapPro Plataforma Autônoma Construção Civil e HVAC-R
- Contexto: PME de construção civil enfrentam alto desperdício, baixa digitalização e dificuldades de coordenação/automação operacional.
- Objetivo: Reduzir custos, aumentar produtividade e automatizar decisões e execuções operacionais via workflows e assistentes inteligentes integrados.
- Métricas de sucesso:
   - MVP lançado em até 4 meses
   - Ativação ≥ 100 clientes beta em 6 meses
   - Redução de >30% custos operacionais dos clientes
   - NPS ≥ 8 após onboarding
   - SLA uptime >99,5%

***

## 2. Problema e Objetivos

- Problema principal: Falta de automação, controle e integração digital nas rotinas centrais das obras, gerando retrabalho, atrasos e custos extras.
- Objetivos mensuráveis:
   - Gerenciar obras e equipes c/ fluxo unificado
   - Orquestrar tarefas, materiais, documentos e comunicações end-to-end
   - Prover IA assistiva (RAG+tool-calling) para dúvidas/decisões técnicas
   - Implantar automação de notificações, pagamentos e orçamentos
- Não‑objetivos (fora do escopo MVP):
   - ERP próprio (apenas integrações)
   - App mobile nativo (PWA, sim)
   - Contabilidade/fiscal profunda

***

## 3. Público‑Alvo e Personas

- Personas:
    - Gestor de obra/engenheiro
    - Mestre de obras/encarregado de campo
    - Almoxarife/responsável por materiais
    - Pequenos e médios empreiteiros
    - Operador de equipe móvel
- Cenários principais:
    - Cadastro e acompanhamento de obras, controle de tarefas e equipes, baixa/lote de materiais, geração e acompanhamento de orçamentos, recebimento de alertas, consulta rápida a informações técnicas via IA.

***

## 4. Roadmap por Fases

- F0 — Bootstrap: scaffold, ci, pipeline, health, ambiente dev rodando
- F1 — MVP: login, projetos, equipe, materiais, tarefas/documentos, API básica, rotinas principais
- F2 — Observabilidade e Qualidade: logs, métricas, testes, cov. inicial, alertas
- F3 — Infra e Deploy: docker/k8s, migrations, ambientes, rollout seguro
- F4 — Performance e Segurança: cache, CORS, rate-limit, headers, perf-budget, WCAG A11y
- F5 — Escala e DX: filas/jobs, document. API, pipelines, DX de dev, automações user/LLM
- F6 — Release/Manutenção: release notes, versionamento, backup, restore, SLOs

***

## 5. Requisitos Funcionais (User Stories)

- [ ] Como gestor, quero cadastrar e editar obras/projetos para controlar status, responsáveis e prazos.
- [ ] Como engenheiro, quero criar tarefas/checklists e atribuir à equipe e projetistas.
- [ ] Como almoxarife, quero registrar entrada/saída/estoque de materiais em cada obra.
- [ ] Como responsável, quero consultar documentos de projetos e receber notificações de alterações.
- [ ] Como usuário, quero acessar via web/mobile (PWA) e receber alertas via e-mail/WhatsApp.
- [ ] Como gestor, quero consultar dashboards de progresso físico/financeiro.
- [ ] Como colaborador, quero autenticação segura (login JWT), MFA opcional.
- [ ] Como stakeholder, quero consultar informações via agente IA conversacional.

***

## 6. Requisitos Não Funcionais

- Confiabilidade: SLA 99,5% uptime/ano, MTTR < 1h
- Segurança: JWT Auth, RBAC mínimo, LGPD, segredos via Vault, OWASP top-10 mitigado
- Observabilidade: logs JSON, métricas HTTP/DB/IA, tracing requests críticos
- Performance: p95 resp API < 300ms, dashboard < 2s
- Escalabilidade: horizontal auto-scale K8s, cache Redis, bulk API/sync job
- Compatibilidade: PWA, desktop + mobile browsers (Edge, Chrome, Safari, Firefox)
- Acessibilidade (a11y): mínimo WCAG 2.1 AA, navegação por teclado, contraste adequado

***

## 7. Arquitetura Alvo

- Frontend: Next.js 15 + TypeScript + Shadcn/ui + TailwindCSS
- Backend: FastAPI (Python 3.11+), API REST (OpenAPI 3)
- Banco: PostgreSQL 16, Alembic; Redis p/ cache/queue
- Workflow/AI: Kestra + n8n (event-driven), LangChain/LangGraph p/ agentes
- API: JWT; versionamento via `/api/v1/`
- Armazenamento arquivos: S3 ou Cloud equivalente
- Infra: Dev via Docker Compose, prod via K8s (EKS)
- Messaging/Jobs: Celery + RabbitMQ
- Diagrama alto nível: Projeto, tarefas, materiais, equipe e documentos conectados via API, AI/Workflows integrados por eventos e webhooks, observabilidade em todo stack

***

## 8. Modelo de Dados (resumido)

- Usuário: { id, email, senha, nome, perfil }
- Projeto: { id, nome, status, owner_id, ... }
- Tarefa: { id, projeto_id, responsável_id, título, deadline, status }
- Equipe: { projeto_id, user_id, role }
- Material: { id, nome, projeto_id, estoque, fornecedor }
- Documento: { id, projeto_id, tarefa_id, url, tipo }
- Relacionamentos principais: Usuário 1:N Projeto; Projeto 1:N Tarefa/Material/Documento/Equipe
- Índices: por owner, por status, FKs consistentes

***

## 9. Design de API

- Convenção: snake_case para backend, camelCase para frontend (conversão automática)
- Erros: `{ "error": { "code": ..., "message": ..., "details": ... } }`
- Paginação padrão `?limit=&offset=`
- Versionamento: `/api/v1/`
- Exemplos:
   - POST `/api/v1/auth/login`
   - GET `/api/v1/projects`
   - POST `/api/v1/projects`
   - GET `/api/v1/projects/{id}/tasks`
   - POST `/api/v1/materials`
- Autorização no header `Authorization: Bearer <jwt>`
- Docs automáticas (Swagger/ReDoc)

***

## 10. Frontend

- Páginas: `/login`, `/dashboard`, `/projects`, `/projects/[id]`, `/tasks`, `/materials`, `/reports`
- Estado: TanStack Query, Zustand (quando global), SWR mini cache
- UI Kit: Shadcn/ui, ícones Lucide
- i18n: pt‑BR (v1); campos preparados para easy-translate
- A11y: contraste, alt, teclado e roles WAI-ARIA
- SEO: title dinâmico, meta, manifest.json (PWA)

***

## 11. Segurança

- Autenticação: JWT, refresh token, MFA opcional (TOTP/SMS e-mail)
- Autorização: RBAC mínimo (admin, gestor, operador)
- Proteção web: CSRF (apenas se suportar forms POST puros), XSS, CORS restritivo, rate-limit (per IP)
- Gestão de segredos: .env local, Vault prod, nunca versionado
- Auditoria: logs toda ação sensível e login/logout
- Privacy/terms: Política LGPD/privacidade

***

## 12. Observabilidade e Operação

- Logs: estruturados, correlacionados por request-id
- Métricas: HTTP (reqs/s, latência, erro), banco, jobs, AI, uso API
- Tracing: habilitado para RPC/AI/integrações sensíveis
- Alertas: erros críticos, alta latência, falhas em jobs, uso CPU/disco cloud

***

## 13. Desenvolvimento e Ambientes

- Dev: `make setup` → `make dev`, `.env.local`
- Test: `make test` (pytest, playwright)
- Lint/Format: `make lint`, `make fmt`
- Ambientes: dev / staging / prod
- Variáveis por ambiente (12‑factor, dotenv)
- Flags de recurso para rollout seguro

***

## 14. CI/CD

- CI: lint → test → build → policy‑check → criar artefato (docker/k8s)
- CD: staging completo/automatizado, produção com aprovação humana
- Migrações sempre antes do deploy app (safe-migrate Alembic)
- Checks e scripts validados sempre antes do merge

***

## 15. Testes

- Pirâmide: unitários > integração > E2E
- Cobertura alvo: 80% backend, 70% frontend
- Teste mínimo: health/version e contrato API ofertas
- Front: Playwright com snapshot básico UI
- Pre-commit hooks ativos para testes rápidos

***

## 16. Internacionalização e SEO

- Idiomas: pt‑BR primário (v1)
- SEO (web pública): titles, metatags, manifest, sitemap, robots.txt

***

## 17. Riscos e Mitigações

- Risco: Falta de onboarding UX → Mitigação: user-test early + survey
- Risco: LLM gerar resposta errada (tool misuse) → Mitigação: tool calling validada/testada + fallback manual/humano
- Risco: Perda de dados acidental → Backups diários automatizados
- Risco: Deploy com segredo exposto → CI bloqueia merge se segredos versionados

***

## 18. Critérios de Aceitação

- Login, CRUD projeto/tarefa/material/doc funcionando
- Health-check e logs no deploy
- API documentada (/_docs)
- Scripts bootstrap e CI verde ao commit
- Coverage mínimo previsto atingido
- Staging deployável com dados fake/seed
- Validação manual user-flow base completa

***

## 19. Entregáveis por Fase

- F0: `src/`, `tests/`, `docs/`, `README`, CI verde
- F1: MVP funcional disponível
- F2: SLOs, logs, métricas completas, erros capturados e dashboards básicos
- F3–F6: Infra estável, escalável, recovery, DX evoluída, documentação e versionamento

***

## 20. Detalhamento das Fases (Checklists)

### F0 — Bootstrap
- [ ] Stack confirmada e README/docs OK
- [ ] Scaffold src/ mínimo, health endpoint
- [ ] Makefile/justfile/ci prontos
- [ ] Pre-commit ativo
- [ ] .gitignore, .editorconfig, AGENTS.md revisados

### F1 — MVP
- [ ] Modelos/CRUD de projeto, tarefa, material, usuário, doc
- [ ] JWT auth, RBAC e refresh
- [ ] Interface frontend funcional/login
- [ ] Testes integração CRUD principais

### F2 — Observabilidade/Qualidade
- [ ] Logs estruturados, req-id correlacionado
- [ ] Métricas HTTP/DB/AI/API
- [ ] Tracing em integrações AI/workflows
- [ ] Testes unit/cov ≥ 80%
- [ ] Pre-commit lint/format/test ativo

### F3 — Infra e Deploy
- [ ] Docker Compose/k8s pronto e diarizado
- [ ] Migrações seguras
- [ ] Diff e rollback documentados
- [ ] Variáveis ambiente seguras e policies de segredo

### F4 — Segurança/Performance
- [ ] CORS, rate-limit, hardening headers, WCAG AA, consultas com paginação/limite

### F5 — Escala e DX
- [ ] Job/queue prontos, doc API validada, flags experimento

### F6 — Release/Manutenção
- [ ] Versionamento, backup/restore simulados
- [ ] SLOs validados e dívida técnica revisada

## Appendix D: DevOps Standards Compliance

### CI/CD Architecture
- Pipeline: GitHub Actions com matrizes Python 3.11/3.12 e Node 20/22.
- Cobertura: artifacts de cobertura publicados e integração com Codecov (limiar 80%).
- Deploy: prévia automática em PR + promoção para produção após merge na `main`.
- Notificações: Slack (`SLACK_WEBHOOK_URL`) e email via SMTP (`CI_SMTP_*`).

### Agent Integration
- `docs/AGENTS.md` define limites de operação de LLMs/agents.
- Fluxo Codex CLI + MCP descrito em `docs/metodo-contrato-codex-cli-com-mcp.md`.
- GitHub Projects automatiza o quadro Kanban e amarra issues/PRs ao roadmap.

### Security Baselines
- Zero segredos versionados; usar `.env.example` apenas como referência.
- `scripts/secret-scan.sh` em pre-push e nos pipelines.
- Monitoramento diário de dependências (`scripts/dependency-watch.sh`) e bloqueios de policy em PR.
- Checks obrigatórios: lint, testes, segurança e Playwright antes do merge.
