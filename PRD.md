# PRD — Template Full‑Stack (LLM‑Safe)

Este PRD é a fonte única de verdade do projeto e guia tanto humanos quanto LLMs. Preencha os campos entre `< >` de acordo com seu produto.

## 0. Guia de Início: Stack e Dependências (Padrão e Exemplos)
- Escolha a stack (linguagem + framework + runtime) aqui e mantenha consistente ao longo do projeto. A LLM deve seguir esta escolha ao criar arquivos de bootstrap.
- Preencha:
  - Linguagem: `<ex.: Python | Node.js | Go | .NET | Java>`
  - Framework: `<ex.: FastAPI | Django | Next.js | NestJS | Spring>`
  - Banco de dados: `<ex.: PostgreSQL | MySQL | SQLite | MongoDB>`
  - ORM/Migrations: `<ex.: SQLAlchemy + Alembic | Prisma | TypeORM | Django ORM>`
  - Testes: `<ex.: pytest | vitest | jest | go test>`
  - Lint/Format: `<ex.: ruff+black+isort | eslint+prettier | golangci-lint>`
  - Empacotamento/Execução: `<ex.: Docker Compose | PM2 | gunicorn+uvicorn | systemd>`

Exemplos comuns (escolha um ou edite):
- Python (API) — FastAPI + PostgreSQL
  - Deps: `fastapi`, `uvicorn[standard]`, `pydantic`, `sqlalchemy`, `alembic`, `psycopg[binary]`
  - Testes/Qualidade: `pytest`, `httpx`, `ruff`, `black`, `isort`
- Node (Full‑stack) — Next.js + Prisma + PostgreSQL
  - Deps: `next`, `react`, `@prisma/client`, `prisma`, `zod`, `axios`
  - Testes/Qualidade: `vitest`/`jest`, `eslint`, `prettier`, `lint-staged`, `husky`
- Node (API) — NestJS + PostgreSQL
  - Deps: `@nestjs/*`, `class-validator`, `class-transformer`, `prisma`/`typeorm`
  - Testes/Qualidade: `jest`, `eslint`, `prettier`
- Python (API) — Django REST Framework
  - Deps: `django`, `djangorestframework`, `psycopg`, `django-environ`
  - Testes/Qualidade: `pytest-django`, `ruff`, `black`, `isort`
- Go (API) — Gin + Gorm + PostgreSQL
  - Deps: `github.com/gin-gonic/gin`, `gorm.io/gorm`, `github.com/lib/pq`
  - Testes/Qualidade: `go test`, `golangci-lint`

Checklist de Bootstrap (independente da stack):
- [ ] `README.md` atualizado com stack, como rodar e scripts
- [ ] `docs/how-to-run.md` com comandos concretos
- [ ] `Makefile`/`justfile` com `fmt`, `lint`, `test`, `dev`, `run`
- [ ] `src/` scaffold mínimo + endpoint/rota de saúde
- [ ] Testes básicos (health/version)
- [ ] `.gitignore`, `.editorconfig`, `AGENTS.md`, `.codex/policy.json`

## 1. Visão Geral
- Nome do produto: `<nome>`
- Contexto: `<contexto do negócio e problema macro>`
- Objetivo: `<resultado desejado>`
- Métricas de sucesso (KPIs/OKRs): `<métricas e metas>`

## 2. Problema e Objetivos
- Problema principal: `<o que precisa ser resolvido>`
- Objetivos mensuráveis: `<lista de objetivos com metas>`
- Não‑objetivos (fora de escopo): `<o que não será feito>`

## 3. Público‑Alvo e Personas
- Personas: `<persona 1, persona 2>`
- Principais cenários de uso: `<cenário → objetivo → valor>`

## 4. Roadmap por Fases
- Fase 0 — Bootstrap: skeleton, CI, docs, ambiente e qualidade.
- Fase 1 — MVP: funcionalidades essenciais para validar valor.
- Fase 2 — Observabilidade e Qualidade: testes, logs, métricas, segurança básica.
- Fase 3 — Infra e Deploy: containerização, migrations, staging, secrets e deploy.
- Fase 4 — Performance e Segurança: caching, perf, hardening, a11y.
- Fase 5 — Escala e DX: filas/jobs, rate‑limit, DX, documentação de APIs.
- Fase 6 — Release e Manutenção: versionamento, releases, SLOs, backups.

## 5. Requisitos Funcionais (User Stories)
- [ ] Como `<persona>`, quero `<ação>` para `<benefício>`.
- [ ] …

## 6. Requisitos Não Funcionais
- Confiabilidade: `<SLOs de uptime, MTTR>`
- Segurança: `<authn/authz, OWASP, secrets>`
- Observabilidade: `<logs, métricas, traces>`
- Performance: `<SLIs (p95), orçamentos (bundle, latência)>`
- Escalabilidade: `<estratégia horizontal/vertical>`
- Compatibilidade: `<browsers, plataformas>`
- Acessibilidade (a11y): `<critérios WCAG>`

## 7. Arquitetura Alvo
- Frontend: `<React/Next.js ou outro>`
- Backend: `<Node/Nest/Express ou Python/FastAPI/Django>`
- API: `<REST/GraphQL>`, versionamento `<v1>`, autenticação `<JWT/OAuth2>`
- Banco de dados: `<PostgreSQL recomendado>`, migrações `<Prisma/Knex/Alembic>`
- Mensageria/Jobs: `<opcional: Redis/Sidekiq/BullMQ/Celery>`
- Armazenamento de arquivos: `<S3/Cloud provider>`
- Infra: `<Docker Compose dev; deploy: Render/Fly/VM/K8s>`
- Diagrama de alto nível: `<descrever módulos e fluxos principais>`

## 8. Modelo de Dados (rótulos e relações)
- Entidades: `<Usuário, Projeto, Tarefa, …>`
- Campos chave: `<nome, email, …>`
- Relacionamentos: `<1:N, N:N>`
- Regras de integridade e índices: `<únicos, FKs, índices>`

## 9. Design de API
- Convenções: `<snake_case vs camelCase, envelopes>`
- Erros: formato padronizado `{ error: { code, message, details } }`
- Paginação/filtros/sort: `<padrões>`
- Versionamento: `</api/v1>`
- Contratos exemplares:
  - `POST /api/v1/auth/login`
  - `GET /api/v1/items?limit=&cursor=`
  - …

## 10. Frontend
- Páginas/rotas: `<lista>`
- Estado: `<React Query/Redux/etc.>`
- UI Kit/Design System: `<opcional>`
- i18n: `<linguagens>`
- Acessibilidade: `<requisitos>`

## 11. Segurança
- Autenticação: `<fluxo>`
- Autorização (RBAC/ABAC): `<papéis e políticas>`
- Proteções web: `<CSRF, XSS, rate‑limit>`
- Gestão de segredos: `<.env local; provedor em produção>`

## 12. Observabilidade e Operação
- Logs: `<níveis, correlação>`
- Métricas: `<técnicas e de negócio>`
- Traces: `<quando útil>`
- Alertas: `<limiares e destinos>`

## 13. Desenvolvimento e Ambientes
- Dev: `make setup` → `make dev`
- Test: `make test` (unit/integration/e2e)
- Lint/Format: `make lint`/`make fmt`
- Ambientes: dev / staging / prod; flags de recurso
- Configuração por ambiente: `<12‑factor, env vars>`

## 14. CI/CD
- CI: lint → test → build → policy‑check → artefatos
- CD: staging automatizado; prod com aprovação
- Estratégia de migrações DB: `<migrar antes/depois, safe‑migrate>`

## 15. Testes
- Pirâmide: unit > integração > e2e
- Cobertura alvo: `<ex.: 80%>`
- Testes de contrato de API e snapshot de UI (quando aplicável)

## 16. Internacionalização e SEO
- Idiomas: `<pt‑BR, en‑US, …>`
- SEO: `<metatags, sitemap, robots>` (se web pública)

## 17. Riscos e Mitigações
- `<risco>` → `<mitigação>`

## 18. Critérios de Aceitação
- Demonstrações: `<o que deve ser possível>`
- Checks automáticos: CI verde; `scripts/validate.sh` OK

## 19. Entregáveis por Fase
- Fase 0: skeleton `src/`, `tests/`, `docs/`, `README`, CI verde
- Fase 1: MVP funcional com deploy em `<plataforma>`
- Fase 2: otimizações, SLOs cumpridos, observabilidade completa

## 20. Detalhamento das Fases (Checklists)

### Fase 0 — Bootstrap
- [ ] Confirmar stack (Seção 0) e atualizar `README.md` e `docs/how-to-run.md`
- [ ] Scaffold mínimo em `src/` e teste de saúde
- [ ] `Makefile`/`justfile` com `fmt`, `lint`, `test`, `dev`, `run`
- [ ] CI ativo (validate + policy‑check; testes quando existirem)
- [ ] `.gitignore`, `.editorconfig`, `AGENTS.md`, `.codex/policy.json` revisados

### Fase 1 — MVP
- [ ] Modelos/Entidades centrais e CRUD básico
- [ ] Autenticação (ex.: sessão/JWT/OAuth2, conforme PRD)
- [ ] UI inicial (se full‑stack) com as rotas essenciais
- [ ] Casos de uso principais com testes de integração

### Fase 2 — Observabilidade e Qualidade
- [ ] Logs estruturados, correlação de requisição
- [ ] Métricas técnicas (latência p95, erro rate) e de negócio
- [ ] Tracing (quando aplicável)
- [ ] Testes unitários + cobertura alvo
- [ ] Lint/format e pre‑commit configurados

### Fase 3 — Infra e Deploy
- [ ] Docker/Compose (ou alternativa) e build reproduzível
- [ ] Banco de dados e migrações versionadas
- [ ] Staging com variáveis de ambiente seguras (sem segredos no repo)
- [ ] Processo de deploy e rollback documentados

### Fase 4 — Performance e Segurança
- [ ] Cache/paginação e limites de consulta
- [ ] Hardening de headers, CORS, rate‑limit
- [ ] Acessibilidade (WCAG aplicável), perf de frontend (se web)

### Fase 5 — Escala e DX
- [ ] Filas e jobs (ex.: Redis, Celery/BullMQ)
- [ ] Observabilidade ampliada (dashboards, alertas)
- [ ] Documentação de API (OpenAPI/GraphQL schema) e DX de dev

### Fase 6 — Release e Manutenção
- [ ] Versionamento semântico e notas de release
- [ ] Backups/retentiva e testes de restauração
- [ ] Revisão periódica de SLOs e dívida técnica

---

## Instruções para LLM
1) Leia PRD.md e gere um resumo + plano com etapas curtas.
2) Obtenha da Seção 0 a stack escolhida e confirme no plano.
3) Obedeça AGENTS.md e `.codex/policy.json` (paths permitidos, limites de diff).
4) Fase 0 — Bootstrap (permitido criar/editar):
   - `src/**`, `tests/**`, `docs/**`, `README.md`, `CONTRIBUTING.md`, `Makefile`,
     `scripts/**`, `.github/workflows/**`, `.gitignore`, `.editorconfig`, `AGENTS.md`, `PRD.md`.
5) Não tocar: `secrets/**`, `infra/prod/**`. Nunca inserir segredos.
6) Mantenha mudanças pequenas e focadas; atualize docs e testes junto do código.
7) Valide localmente com `bash scripts/validate.sh`. CI deve ficar verde.
8) Abra PR descrevendo: resumo do PRD, escopo, riscos, validação e próximos passos.
9) Após aprovação, avance pelas Fases 1→6 conforme este PRD.
