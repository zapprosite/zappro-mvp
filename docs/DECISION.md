# DECISION.md - Matriz de Decisão Refactor vs Rewrite

**Última atualização:** 7 Nov 2025  
**Status:** Active Decision Framework  
**Owner:** @willrefrimix, @jpmarcenaria

---

## Matriz de Decisão

### Critérios de Avaliação
Scoring: 1-5 (1=Low, 5=High)

Cada módulo recebe score em:

Technical Debt (1=clean, 5=high debt)

Reutilização (1=replace all, 5=reuse 100%)

Risco (1=low risk change, 5=high risk)

Tempo (1=<1 week, 5=>4 weeks)

ROI (1=low value, 5=high value)

Decision:

REFACTOR: Score ≤12

REWRITE: Score ≥13

```text
Decision Tree (simplificado)

            +---------------------+
            |  Total Score (1-25) |
            +----------+----------+
                       |
                <= 12  |  >= 13
                       |
                 REFACTOR       REWRITE
          (ajustes incrementais) (reconstrução)
```

[!TIP]
Mantenha evidências por critério (debt, risco, tempo). Registre notas das medições para auditoria.

---

## Módulos Avaliados

### Backend Modules

#### Module: src/utils/auth.py
| Criterion | Score | Notes |
|-----------|-------|-------|
| Technical Debt | 2 | JWT well-structured, but async migration pending |
| Reusability | 4 | Can be extracted to package |
| Risk | 2 | Low risk refactoring |
| Time | 2 | ~1 week async conversion |
| ROI | 5 | High value (performance) |
| **Total** | **15** | **→ REWRITE (async-first)** |

**Decision:** REWRITE to async first
- Migrate `get_current_user` to async
- Convert all DB queries to async session
- Add typed dependency injection
- PR target: v1.1

---

#### Module: src/models/__init__.py
| Criterion | Score | Notes |
|-----------|-------|-------|
| Technical Debt | 3 | Some unused imports, Pydantic V2 migration pending |
| Reusability | 3 | Mixed internal/external models |
| Risk | 3 | Medium risk (affects schemas) |
| Time | 2 | 3-5 days refactor |
| ROI | 4 | Good value (cleaner types) |
| **Total** | **15** | **→ REWRITE (Pydantic V2)** |

**Decision:** REWRITE to Pydantic V2 ConfigDict
- Replace \`config\` class with \`ConfigDict\`
- Update model validation
- Migrate \`.dict()\` → \`.model_dump()\`
- PR target: v1.1

---

#### Module: src/main.py
| Criterion | Score | Notes |
|-----------|-------|-------|
| Technical Debt | 2 | Mostly clean, but FastAPI lifespan deprecated |
| Reusability | 4 | Good modular structure |
| Risk | 1 | Low risk (FastAPI standard upgrade) |
| Time | 2 | ~1 week lifespan migration |
| ROI | 3 | Medium value (future-proofing) |
| **Total** | **12** | **→ REFACTOR (lifespan)** |

**Decision:** REFACTOR with FastAPI lifespan
- Replace \`@app.on_event("startup")\` with lifespan context
- Test startup/shutdown hooks
- PR target: v1.0.1 (patch)

---

### Frontend Modules

#### Module: frontend/pages/api-integration.ts
| Criterion | Score | Notes |
|-----------|-------|-------|
| Technical Debt | 4 | Legacy fetch API, no error handling |
| Reusability | 2 | Tightly coupled to components |
| Risk | 3 | Medium risk (API calls) |
| Time | 3 | 1-2 weeks refactor |
| ROI | 5 | High value (reliability) |
| **Total** | **17** | **→ REWRITE (axios/error handling)** |

**Decision:** REWRITE API layer
- Migrate to Axios or SWR/TanStack Query
- Add comprehensive error handling
- Implement retry logic + exponential backoff
- Type-safe API responses (Zod validation)
- PR target: v1.1

---

#### Module: frontend/components/forms
| Criterion | Score | Notes |
|-----------|-------|-------|
| Technical Debt | 1 | Clean React hooks, good patterns |
| Reusability | 5 | Highly reusable components |
| Risk | 1 | Low risk (isolated) |
| Time | 1 | No changes needed |
| ROI | 2 | Low value (works well) |
| **Total** | **10** | **→ KEEP (No changes)** |

**Decision:** No changes, use as template
- Document patterns for future components
- Keep as reference architecture

---

### DevOps / Infrastructure

#### Module: docker-compose.yml
| Criterion | Score | Notes |
|-----------|-------|-------|
| Technical Debt | 2 | Mostly current, missing healthchecks |
| Reusability | 4 | Good for dev, production-ready |
| Risk | 2 | Low risk (isolated container config) |
| Time | 1 | <1 week to add healthchecks |
| ROI | 4 | Good value (reliability) |
| **Total** | **13** | **→ REFACTOR (add healthchecks)** |

**Decision:** REFACTOR with healthchecks
- Add \`healthcheck\` to all services (zappro-api, postgres, redis)
- Configure timeout/retry settings
- PR target: v1.0.1 (patch)

---

#### Module: .github/workflows/ci.yml
| Criterion | Score | Notes |
|-----------|-------|-------|
| Technical Debt | 1 | Modern matrix builds, good structure |
| Reusability | 5 | Can be reused for other projects |
| Risk | 1 | Low risk (CI only) |
| Time | 1 | Maintenance-only |
| ROI | 3 | Medium value (quality gates) |
| **Total** | **11** | **→ KEEP** |

**Decision:** KEEP & enhance incrementally
- Monitoring: Already modern
- Future: Add Nx cloud, visual regression tests

---

## Summary Table

| Module | Score | Decision | Timeline | PR Target |
|--------|-------|----------|----------|-----------|
| src/utils/auth.py | 15 | REWRITE (async) | 1 week | v1.1 |
| src/models/__init__.py | 15 | REWRITE (Pydantic V2) | 3-5 days | v1.1 |
| src/main.py | 12 | REFACTOR (lifespan) | 1 week | v1.0.1 |
| frontend/api-integration | 17 | REWRITE (axios) | 1-2 weeks | v1.1 |
| frontend/forms | 10 | KEEP | - | - |
| docker-compose.yml | 13 | REFACTOR (healthchecks) | <1 week | v1.0.1 |
| .github/workflows/ci.yml | 11 | KEEP | - | - |

---

## Implementation Roadmap

### Phase 1: Quick Wins (v1.0.1 Patch)
- [ ] Add FastAPI lifespan to src/main.py
- [ ] Add docker-compose healthchecks
- [ ] Quick test pass + merge to main

### Phase 2: Major Improvements (v1.1)
- [ ] Async-first rewrite of src/utils/auth.py
- [ ] Pydantic V2 ConfigDict migration
- [ ] Frontend API layer rewrite (Axios + error handling)

### Phase 3: Polish & Optimization (v1.2)
- [ ] Performance profiling
- [ ] Custom MCPs for domain (blueprints, materials)
- [ ] Turborepo integration for builds

---

## Risk Assessment

### Refactor Risks (LOW)
- Limited scope
- Backward-compatible (usually)
- Fast rollback possible

### Rewrite Risks (MEDIUM-HIGH)
- Requires comprehensive testing
- May introduce new bugs
- Longer review cycle

**Mitigation:**
- Feature flags for gradual rollout
- 100% test coverage before merge
- Staged deployment (staging → preview → production)

---

## FAQ

**Q: Posso ignorar a matriz?**
A: Não. A matriz garante decisões objetivas. Questione se discorda.

**Q: E se descobrir novo technical debt?**
A: Atualize o score + decision, abra issue, reassess.

**Q: Timeline pode mudar?**
A: Sim. Atualize DECISION.md se tempo mudar >20%.

---

## Contact
- Questions: GitHub discussions
- Slack: #technical-decisions
