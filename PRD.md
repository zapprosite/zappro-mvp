# PRD.md — ZapPro MVP Product Requirements Document

**Última atualização:** 7 Nov 2025  
**Versão:** 2.0-multi-agent-automation  
**Status:** Production Ready + Multi-Agent Orchestration  
**Owner:** @willrefrimix, @jpmarcenaria

---

## Executive Summary

[!NOTE]
Este documento descreve o MVP do ZapPro (SaaS para construção civil) com arquitetura full‑stack moderna, automações multi‑agente e práticas DevOps sênior. Use este PRD como fonte única de verdade para escopo, metas e roadmap.

**ZapPro MVP** é um SaaS de gestão de projetos em construção civil com:
- ✅ Full-stack moderno (FastAPI + Next.js 15 + PostgreSQL)
- ✅ Multi-Agent System (Codex + N8N + Kestra + Chatwoot)
- ✅ Automação de workflows (event-driven + scheduled)
- ✅ Customer support via LLM chatbot
- ✅ Real-time dashboards (Kanban + ADM metrics)
- ✅ DevOps Senior (CI/CD, security scanning, coverage gates)

**Timeline:** MVP completo em 30 dias, production-ready em 60 dias

---

## Sumário

- [1. Product Vision](#1-product-vision)
- [2. Architecture & Tech Stack](#2-architecture--tech-stack)
- [3. Core Features (MVP Phase 1)](#3-core-features-mvp-phase-1)
- [4. Data Models (Tables & Schemas)](#4-data-models-tables--schemas)
- [5. Kanban Workflow & Automation](#5-kanban-workflow--automation)
- [6. Multi-Agent Orchestration Roadmap](#6-multi-agent-orchestration-roadmap)
- [7. Deployment & Operations](#7-deployment--operations)
- [8. Quality Metrics & Success Criteria](#8-quality-metrics--success-criteria)
- [9. Known Constraints & Decisions](#9-known-constraints--decisions)
- [10. Go-Live Checklist](#10-go-live-checklist)
- [11. References & Documentation](#11-references--documentation)

---

## 1. Product Vision

### Problem Statement
- Construtoras brasileiras usam planilhas Excel para gestão de projetos
- Falta rastreabilidade, comunicação integrada, e relatórios em tempo real
- Espalhamento de informação em WhatsApp, email, e discos locais

### Solution
- Plataforma centralizada, cloud-native, com IA para automação
- Integração com Kestra (scheduler) + N8N (workflow) + Chatwoot (support)
- Agentes LLM autônomos para tarefas repetitivas
- Real-time notifications (Slack, email, SMS)

### Success Metrics
- ✅ 80%+ test coverage (enforced)
- ✅ 99.9% uptime (staging + production)
- ✅ <2s page load time
- ✅ 100% API endpoints documented + tested
- ✅ Zero security vulnerabilities (OWASP Top 10)
- ✅ Agentes autônomos completam 80%+ tasks sem intervenção manual

---

## 2. Architecture & Tech Stack

### Backend

Language: Python 3.11+
Framework: FastAPI 0.115
Database: PostgreSQL 16 + SQLAlchemy 2.x
Async: asyncio + httpx
Task Queue: Celery (optional, via Kestra)
Caching: Redis 7.x
Authentication: JWT (RS256) + OAuth2
ORM/Migrations: SQLAlchemy + Alembic 1.13
Testing: pytest 8.x + httpx + faker
Linting: ruff, black, isort, mypy
Security: bandit, pip-audit, trivy

### Frontend

Framework: Next.js 15 (App Router)
Language: TypeScript 5
UI Components: Shadcn/ui + TailwindCSS 3
State: Zustand + TanStack Query 5
Forms: React Hook Form + Zod validation
Testing: Playwright 1.40+ (E2E), Vitest (unit)
Linting: ESLint + Prettier + TypeScript strict
Bundle: Next.js optimized (code splitting, ISR)

### AI & Automation

LLM Agent: Codex CLI (GPT-5 High Reasoning)
Orchestration: Kestra 0.19 (event-driven jobs)
Workflow Engine: N8N 1.65 (visual workflows)
Chatbot: Chatwoot 3.x + LangChain 1.0
Knowledge Base: Vector DB (Pinecone or Weaviate)

### Infrastructure

Containerization: Docker + docker-compose (dev)
Orchestration: Kubernetes (K8s, EKS for prod)
IaC: Pulumi or Terraform
CI/CD: GitHub Actions + FluxCD
Secrets: Vault (prod), GitHub Actions (CI)
Monitoring: Sentry, Datadog, Posthog, LangSmith
Logging: ELK Stack or Datadog

---

## 3. Core Features (MVP Phase 1)

### 3.1 Project Management
- [ ] Create/edit/delete projects
- [ ] Team members + role-based access (RBAC)
- [ ] Kanban board (drag-drop tasks)
- [ ] Sprint planning + burndown charts
- [ ] Comments + file attachments
- [ ] Activity log (audit trail)

### 3.2 Task Management
- [ ] Create tasks with priority, assignee, due date
- [ ] Task filters + search (full-text)
- [ ] Recurring tasks (template-based)
- [ ] Time tracking + estimates
- [ ] Subtasks + dependencies
- [ ] Notifications (Slack, email, in-app)

### 3.3 Dashboard & Reporting
- [ ] Real-time project dashboard (Kanban view)
- [ ] Admin metrics (burndown, cycle time, agent performance)
- [ ] Custom reports (PDF export)
- [ ] Data visualization (charts, graphs)

### 3.4 Integrations
- [ ] Slack notifications (new tasks, updates, mentions)
- [ ] GitHub sync (PRs linked to tasks)
- [ ] Webhook support (custom integrations)
- [ ] N8N workflows (custom automation)
- [ ] Kestra schedules (daily reports, backups)

### 3.5 LLM-Powered Automation
- [ ] AI task generation from descriptions
- [ ] Auto-categorization (priority, sprint)
- [ ] Chatwoot customer support chatbot
- [ ] Smart notifications (NLP-based)
- [ ] Anomaly detection (missed deadlines, overload)

### 3.6 Security & Compliance
- [ ] Data encryption (at rest + in transit)
- [ ] MFA + SAML/SSO (enterprise)
- [ ] GDPR/LGPD compliance (data export, deletion)
- [ ] Audit logs (all user actions)
- [ ] Rate limiting + DDoS protection

---

## 4. Data Models (Tables & Schemas)

### Core Tables

```sql
-- Users & Auth
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR UNIQUE NOT NULL,
  password_hash VARCHAR NOT NULL,
  full_name VARCHAR,
  role ENUM ('admin', 'manager', 'member'),
  mfa_enabled BOOLEAN DEFAULT false,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- Projects
CREATE TABLE projects (
  id UUID PRIMARY KEY,
  name VARCHAR NOT NULL,
  description TEXT,
  owner_id UUID REFERENCES users(id),
  status ENUM ('active', 'archived') DEFAULT 'active',
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- Tasks
CREATE TABLE tasks (
  id UUID PRIMARY KEY,
  project_id UUID REFERENCES projects(id),
  title VARCHAR NOT NULL,
  description TEXT,
  priority ENUM ('low', 'medium', 'high', 'critical'),
  status ENUM ('backlog', 'todo', 'in_progress', 'review', 'done'),
  assignee_id UUID REFERENCES users(id),
  due_date DATE,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- Sprints
CREATE TABLE sprints (
  id UUID PRIMARY KEY,
  project_id UUID REFERENCES projects(id),
  name VARCHAR,
  start_date DATE,
  end_date DATE,
  status ENUM ('planning', 'active', 'closed'),
  created_at TIMESTAMP
);

-- Agent Logs (for monitoring)
CREATE TABLE agent_logs (
  id UUID PRIMARY KEY,
  agent_type VARCHAR ('code', 'qa', 'devops', 'docs'),
  task_description TEXT,
  status VARCHAR ('pending', 'running', 'success', 'failed'),
  result TEXT,
  error_message TEXT,
  started_at TIMESTAMP,
  ended_at TIMESTAMP,
  created_at TIMESTAMP
);

-- Webhooks (for N8N/Kestra)
CREATE TABLE webhooks (
  id UUID PRIMARY KEY,
  event_type VARCHAR,
  url VARCHAR NOT NULL,
  active BOOLEAN DEFAULT true,
  created_at TIMESTAMP,
  last_triggered TIMESTAMP
);

-- Audit Trail
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  action VARCHAR,
  resource_type VARCHAR,
  resource_id UUID,
  changes JSONB,
  created_at TIMESTAMP
);
```

### Kanban State Machine

```text
Task States:
BACKLOG → TODO → IN_PROGRESS → REVIEW → DONE

Legendas auxiliares:
Auto Generated | Assigned | Working | Blocked | Archive
```

### Admin Dashboard Metrics Table

| Metric | Formula | Updated | Target |
|--------|---------|---------|--------|
| **Backlog Size** | COUNT(tasks WHERE status=BACKLOG) | Real-time | <50 |
| **Cycle Time (days)** | AVG(done_date - created_date) | Daily | <7 |
| **Agent Success Rate** | COUNT(SUCCESS) / COUNT(ALL) | Real-time | >95% |
| **Coverage** | Test lines / Total lines | CI | >80% |
| **Uptime** | (24h - downtime) / 24h | Hourly | 99.9% |
| **API Response Time** | AVG(response_time) | Real-time | <200ms |

---

## 5. Kanban Workflow & Automation

### Kanban States (GitHub Projects)

```text
BACKLOG (New issues)
↓ [Agent auto-assigns if > 50 items]
IN PROGRESS (Working)
↓ [Auto-notify Slack when assigned]
IN REVIEW (Waiting for approval)
↓ [Auto-request reviewers, assign to 2 reviewers]
DONE (Merged & deployed)
↓ [Auto-archive after 30 days]
ARCHIVED
```

### Automation Rules

```text
Rules:
New issue → Add to Backlog (auto)
Issue assigned → Move to In Progress (auto)
PR opened → Auto-assign reviewers (by path)
PR approved 2x → Ready for merge (auto)
PR merged → Move to Done (auto)
Merged & deployed → Notify Slack (webhook)
Stale 30 days → Move to Archived (auto)
Agent task success → Add ✅ label (auto)
Agent task failed → Add ❌ label + escalate (auto)
```

---

## 6. Multi-Agent Orchestration Roadmap

### Phase 1 (Week 1-2): Single Agent
- ✅ Codex CLI (GPT-5) reads code + commits atomically
- ✅ Loop guard + context validation
- ✅ Testes + lint gates

### Phase 2 (Week 2-3): Sub-Agents
- [ ] Code Agent (features, fixes)
- [ ] QA Agent (tests, coverage)
- [ ] Docs Agent (documentation)
- [ ] DevOps Agent (infra, secrets, monitoring)

### Phase 3 (Week 3-4): External Integrations
- [ ] N8N workflows (webhook-triggered)
- [ ] Kestra schedules (event-driven jobs)
- [ ] Chatwoot bot (customer support)
- [ ] Slack integration (notifications)

### Phase 4+ (After MVP): Advanced
- [ ] Knowledge base (vector DB + RAG)
- [ ] Multi-language support
- [ ] Custom MCPs (construction domain)
- [ ] Advanced analytics (Posthog, LangSmith)

---

## 7. Deployment & Operations

### Environment Stages

| Stage | URL | Frequency | Approval |
|-------|-----|-----------|----------|
| **Development** | localhost:8000 | Every commit | Auto |
| **Staging** | staging.zappro.site | Every main push | Auto |
| **Preview** | preview-{PR}.zappro.site | Every PR | Auto |
| **Production** | app.zappro.site | Manual (via release tag) | 2 reviewers |

### CI/CD Pipeline

```text
PUSH → GitHub Actions:
Lint (ruff, black, isort, eslint)
Tests (pytest, vitest, playwright)
Security Scan (bandit, npm audit, secret-scan)
Coverage Report (codecov, >80% threshold)
Deploy Preview (if PR)
Deploy Production (if main + tag release)
```

### Monitoring & Alerting

```text
Metrics:
API response time (p95, p99)
Error rate (5xx, 4xx)
Database query time
Agent success rate
Uptime (99.9% SLA)

Alerts:
Slack notification on deploy
Email on critical errors
PagerDuty for on-call (production)
GitHub issue for low-severity bugs
```

### Data Model Relationships (overview)

```text
users 1 ─── * projects
projects 1 ─── * tasks
users 1 ─── * tasks (assignee)
projects 1 ─── * sprints
```

---

## 8. Quality Metrics & Success Criteria

### Code Quality
- [ ] Test coverage ≥80% (enforced by CI)
- [ ] Type hints for all functions (Python)
- [ ] TypeScript strict mode (Frontend)
- [ ] No HIGH/CRITICAL security vulnerabilities
- [ ] Zero secrets versionado
- [ ] Code review: 2 min reviewers, <24h response time

### Performance
- [ ] Page load time <2s (lighthouse score >90)
- [ ] API response time <200ms (p95)
- [ ] Database queries <100ms (no N+1 queries)
- [ ] Bundle size <500KB (gzipped)

### Reliability
- [ ] 99.9% uptime (staging + production)
- [ ] 0 unplanned downtime (target)
- [ ] Automated rollback on deploy failure
- [ ] Backup + restore tested weekly

### Agent Performance
- [ ] ≥95% task success rate (Codex)
- [ ] <5% escalation rate (manual intervention)
- [ ] <5 min resolution time (QA agent)
- [ ] ≤3 loop detections per week

---

## 9. Known Constraints & Decisions

### Technical Debt (from docs/_archive/DECISION.md)

| Module | Decision | Timeline |
|--------|----------|----------|
| src/utils/auth.py | REWRITE (async) | Week 2 |
| src/models/__init__.py | REWRITE (Pydantic V2) | Week 2 |
| src/main.py | REFACTOR (FastAPI lifespan) | Week 1 |
| frontend/api-layer | REWRITE (axios + error handling) | Week 3 |
| docker-compose.yml | REFACTOR (healthchecks) | Week 1 |

### Known Issues
- [ ] WSL2 Docker daemon needs manual start (not auto)
- [ ] N8N API rate limits (need queue backoff)
- [ ] Kestra schedule timezone handling (UTC only for now)
- [ ] Chatwoot escalation UX needs polish

---

## 10. Go-Live Checklist

### Pre-Production (Week 4)
- [ ] All features implemented + tested
- [ ] Security audit completed
- [ ] Performance optimized (<2s load time)
- [ ] Monitoring + alerting configured
- [ ] Support runbook written
- [ ] Data migration tested
- [ ] Disaster recovery plan documented

### Production Deployment
- [ ] Blue-green deployment setup
- [ ] DNS failover configured
- [ ] SSL certificates renewed
- [ ] Database backups automated
- [ ] On-call rotation setup
- [ ] Customer communication ready

### Post-Launch
- [ ] Monitor error rates (target: <0.1%)
- [ ] Track agent performance
- [ ] Gather user feedback (Posthog events)
- [ ] Plan next features (roadmap)

---

## 11. References & Documentation

- **docs/CODEX_RUNBOOK.md** — Runbook canônico (políticas, T1..T8, processos)
- **docs/api-endpoints.md** — Catálogo REST com exemplos e envelopes
- **docs/INDEX.md** — Índice de documentos ativos e mapa de dependências
- **docs/WORKFLOW.md** — Sequência operacional para planejamento, execução e validação
- **docs/SECURITY.md** — Políticas de segurança e checklists de validação
- **README.md** — Quick start guide
- **scripts/validate.sh** — Validation suite
- **bin/codex.sh** — Codex CLI wrapper
- **tutor/TUTOR_MASTER_PROMPT.md** — Prompt mestre com regras, matrizes e checkpoints
- **tutor/prompt.md** — LLM context template
- **tutor/progress.state.md** — Sprint status

---

**PRD v2.0 Complete: Multi-Agent + Full Automation Ready**

**Next Sprint:** Week 1 focus on Phase 1 refactors (auth async, main lifespan, docker healthchecks)
