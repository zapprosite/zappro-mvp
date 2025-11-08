# ZapPro MVP Roadmap 2025-2026

**Status:** Nov 7, 2025 — Phase 1 (Governança) ✅  
**Next:** Phase 2 (Multi-Agent Automation) — 2-4 semanas  
**Team:** Will Refrimix (Backend/DevOps), jpmarcenaria (Frontend)  
**Timeline:** MVP completo até 31 Jan 2026

---

## Phase 1: Governança & Documentação ✅ (COMPLETO)

| Semana | Objetivo | Status |
|--------|----------|--------|
| Nov 4-7 | Estrutura repos + docs + tutor contracts | ✅ DONE |
| Nov 7 | AGENTS.md v2.0 + PRD.md v2.0 refator | ✅ DONE |

**Deliverables:**
- ✅ README.md (com badges + quick start)
- ✅ docs/AGENTS.md (multi-agent + webhooks)
- ✅ docs/SECURITY.md (OWASP + LGPD)
- ✅ docs/WORKFLOW.md (Git workflow)
- ✅ docs/DECISION.md (Matriz refactor/rewrite)
- ✅ PRD.md v2.0 (Kanban + Admin + N8N/Kestra)
- ✅ tutor/TUTOR_MASTER_PROMPT.md (contrato permanente)

---

## Phase 2: Backend & Core Features (Nov 8 - Nov 22)

### Week 1: Refactorings (Nov 8-14)

| Task | Effort | Owner | Status |
|------|--------|-------|--------|
| Async auth.py (DECISION score 15) | 5 days | Will | 🔲 TODO |
| Pydantic V2 models (score 15) | 3 days | Will | 🔲 TODO |
| FastAPI lifespan (score 12) | 3 days | Will | 🔲 TODO |
| Docker healthchecks (score 13) | 2 days | Will | 🔲 TODO |

**Validation:** All 26 tests ≥80% coverage  
**CI/CD:** Matrix builds (Python 3.11/3.12)

### Week 2-3: Core Features (Nov 15-29)

- [ ] Project CRUD endpoints (CREATE, READ, UPDATE, DELETE)
- [ ] Task management system (kanban states, filters)
- [ ] Sprint planning + burndown API
- [ ] User authentication + RBAC (OAuth2 + JWT)
- [ ] Webhook support (for N8N triggers)
- [ ] Activity audit logs

**Tests Required:** >100 new tests, 80%+ coverage  
**Endpoints:** 20+ REST API endpoints documented

---

## Phase 3: Frontend & UI (Nov 22 - Dec 13)

### Week 1: Setup & Components (Nov 22-29)

- [ ] Next.js 15 app structure (App Router)
- [ ] Shadcn/ui + TailwindCSS integration
- [ ] Authentication UI (login, signup, OAuth)
- [ ] Layout components (navbar, sidebar, footer)

### Week 2: Pages & Workflows (Nov 29 - Dec 6)

- [ ] Dashboard page (Kanban board)
- [ ] Projects list + detail page
- [ ] Task creation + editing
- [ ] Team members page

### Week 3: Polish (Dec 6-13)

- [ ] Responsive design (mobile-first)
- [ ] Error handling + loading states
- [ ] Playwright E2E tests (smoke tests)
- [ ] Performance optimization

**Performance Target:** Lighthouse score >90

---

## Phase 4: AI & Automation (Dec 13 - Dec 27)

### Multi-Agent System Setup

| Agent | Role | Status | Timeline |
|-------|------|--------|----------|
| Codex CLI | Code generation + fixes | ✅ Ready | NOW |
| Code Agent | Features, refactors | 🔲 Setup | Dec 13 |
| QA Agent | Tests, coverage | 🔲 Setup | Dec 13 |
| Docs Agent | Documentation | 🔲 Setup | Dec 13 |
| N8N Orchestrator | Workflow automation | 🔲 Setup | Dec 20 |
| Kestra Scheduler | Event-driven jobs | 🔲 Setup | Dec 20 |
| Chatwoot Bot | Customer support | 🔲 Setup | Dec 27 |

### Integration Tasks

- [ ] N8N workflows (GitHub → Slack → Deploy)
- [ ] Kestra scheduled jobs (daily health checks, backups)
- [ ] Chatwoot LLM bot (customer support + escalation)
- [ ] Webhook receivers (.zappro/webhooks/)
- [ ] Vector DB (Pinecone) for knowledge base
- [ ] GitHub Projects automation (kanban states)

**Output:** 5+ working workflows + bot responding to customer messages

---

## Phase 5: DevOps & Production (Dec 27 - Jan 10)

### Infrastructure

- [ ] Kubernetes deployment config (EKS ready)
- [ ] GitHub Actions CD pipeline (blue-green deploy)
- [ ] Monitoring (Sentry, Datadog, Posthog)
- [ ] Backup + disaster recovery (tested weekly)
- [ ] SSL certificates + DNS failover

### Security Audit

- [ ] OWASP Top 10 verification
- [ ] Penetration testing (external firm)
- [ ] LGPD compliance checklist
- [ ] Secret rotation policy

**Target:** 99.9% uptime SLA

---

## Phase 6: Launch & Post-Launch (Jan 10 - Jan 31)

### Pre-Launch (Jan 10-20)

- [ ] Load testing (1000 concurrent users)
- [ ] Database migration testing
- [ ] Backup restore verification
- [ ] Customer communication ready
- [ ] Support runbook finalized

### Launch (Jan 24)

- [ ] Blue-green deployment
- [ ] Monitor error rates (<0.1% target)
- [ ] Track agent performance (>95% success)
- [ ] Gather user feedback (Posthog events)

### Post-Launch (Jan 24-31)

- [ ] Bug fixes (P0/P1 only)
- [ ] Performance monitoring
- [ ] Plan Phase 2 roadmap

---

## 📊 Success Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Test Coverage | ≥80% | 🔲 TODO |
| API Response Time | <200ms (p95) | 🔲 TODO |
| Page Load Time | <2s | 🔲 TODO |
| Uptime | 99.9% | 🔲 TODO |
| Agent Success Rate | ≥95% | 🔲 TODO |
| Security Vulns | 0 HIGH/CRITICAL | 🔲 TODO |

---

## 🎯 Quick Actions (This Week)

```text
Mon Nov 8
  - Run Codex audit: codex -m gpt-5 --full-auto "Audit all .md files"
  - Start async auth refactor (DECISION score 15)
Tue Nov 9
  - Pydantic V2 migration PR
  - Docker healthchecks PR
Wed Nov 10
  - Merge all refactors to main
  - Open GitHub Projects board
  - Auto-assign reviewers
Thu–Fri Nov 11–12
  - Code review + merge PRs
  - Update tutor/progress.state.md
  - Plan Week 2 (core features)
```

---

## 📞 Contact & Escalation

- **Issues:** github.com/zapprosite/zappro-mvp/issues
- **Slack:** #dev-updates
- **Founder:** @willrefrimix
- **Security:** security@zappro.site

---

**Timeline: 86 days to MVP launch (Jan 31, 2026)**  
**Status: ON TRACK** ✅
