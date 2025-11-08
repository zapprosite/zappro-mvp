# AGENTS.md - Agent Operations & Multi-Agent System

**Última atualização:** 7 Nov 2025  
**Versão:** 2.0-multi-agent  
**Status:** Production-Ready Multi-Agent + N8N/Kestra/Chatwoot Integration

---

## Sumário

- [1. Scope & Governance](#1-scope--governance)
- [2. Agent Types & Responsibilities](#2-agent-types--responsibilities)
- [3. Multi-Agent Orchestration](#3-multi-agent-orchestration)
- [4. Agent Constraints & Golden Rules](#4-agent-constraints--golden-rules)
- [5. MCP Integration & Routing](#5-mcp-integration--routing)
- [6. Webhook Integration (N8N/Kestra/Chatwoot)](#6-webhook-integration-n8nkestrachatwoot)

---

## 1. Scope & Governance

### Áreas de Operação (em ordem de precedência)
1. **PRD.md** — Fonte única de verdade do produto
2. **AGENTS.md** — Regras de operação (este arquivo)
3. **Subdiretórios** — Podem ter AGENTS.md específicos (que prevalecem localmente)

### O que pode alterar
- ✅ \`src/\`, \`tests/\`, \`docs/\`, \`README.md\`, \`Makefile\`, \`scripts/\`
- ✅ \`.github/workflows/\`, \`.gitignore\`, \`.editorconfig\`
- ✅ \`AGENTS.md\`, \`PRD.md\` (com justificativa clara)

### O que requer aprovação explícita (CODEOWNERS)
- 🔒 \`.env\`, \`secrets/\`, infra produção (K8s, Vault, DB credentials)
- 🔒 Deploy automático (CD pipeline rules)
- 🔒 Alterações críticas de segurança

---

## 2. Agent Types & Responsibilities

### Agent Classes

| Agent Type | Purpose | MCPs | Timeout | Auto-Execute |
|-----------|---------|------|---------|---------------|
| **Code Agent** | Refactor, features, fixes | filesystem, git, github, shell, playwright | 2h | ✅ |
| **QA Agent** | Testing, validation, coverage | shell, filesystem, playwright, github | 1h | ✅ |
| **DevOps Agent** | Infra, deployment, monitoring | shell, git, github, kubernetes, docker | 3h | ⚠️ (needs approval) |
| **Docs Agent** | Documentation, runbooks, changelog | filesystem, git, github, web-search | 30m | ✅ |
| **N8N Orchestrator** | Workflow automation, integrations | n8n-api, webhook, github, slack | 1h | ✅ |
| **Kestra Scheduler** | Event-driven jobs, schedules | kestra-api, shell, github, slack | 2h | ✅ |
| **Chatwoot Bot** | Customer support, FAQ, escalation | chatwoot-api, langchain, knowledge-base | 15m | ✅ |

---

## 3. Multi-Agent Orchestration

### Agent Hierarchy (Sub-Agent Pattern)

```text
┌─────────────────────────────────────────────────────────────┐
│ Main Codex Agent (GPT-5 High Reasoning, 7h timeout)         │
└──────────────┬──────────────────────────────────────────────┘
               │
      ┌────────┼─────────┬──────────────┬───────────────┐
      ▼        ▼         ▼              ▼               ▼
   Code      QA       DevOps           Docs         N8N/Kestra
   Agent     Agent     Agent           Agent        Orchestrator
      │        │         │              │               │
      ▼        ▼         ▼              ▼               ▼
  Features  Tests    Deployment      Runbooks        Automation
  Fixes     Coverage  Monitoring     Changelog       Integrations
  Refactor  E2E       Security       Docs           Schedules
```

### Agent Handoff Protocol

1. **Main Agent** receives task + reads context (PRD.md, AGENTS.md, progress.state.md)
2. **Main Agent** delegates to specialized sub-agents via MCP calls
3. **Sub-agents** execute atomically, report status to Main Agent
4. **Main Agent** aggregates results, opens PR with summary
5. **Validation** (lint, test, security) gates merge

### Communication Pattern (Webhook-Based)

```text
Webhook Flows:
GitHub PR opened → Slack notification → Code review auto-assignment
Tests fail → GitHub comment → Code Agent re-trigger
Deploy success → Chatwoot notification → Customer support
N8N job failure → Slack alert → DevOps Agent escalation
Kestra schedule trigger → Workflow execution → GitHub commit log
```

---

## 4. Agent Constraints & Golden Rules

### Code Safety

[!IMPORTANT]
Valide antes de commitar: `make lint`, `make test` e `bash scripts/validate.sh` devem passar.

✅ **MUST:**
- Read context first: \`docs/AGENTS.md\`, \`PRD.md\`, \`tutor/progress.state.md\`
- Validate before commit: \`make lint\`, \`make test\`, \`bash scripts/validate.sh\`
- Map MCPs explicitly in PR body
- Never commit secrets (pre-push hook blocks)
- One atomic change per commit
- All tests must pass (80%+ coverage threshold)

❌ **NEVER:**
- Recursive prompts (loop guard active)
- Copy-paste code without validation
- Hardcode secrets in code
- Rename/delete files massively
- Skip security scanning
- Ignore test failures (escalate after 5 retries)

[!WARNING]
Nunca exponha secrets em código ou PRs. Use `.env.example` e GitHub Actions secrets.

### Resource Access

| Resource | Access | Notes |
|----------|--------|-------|
| \`src/\` | ✅ Read/Write | Apply DECISION.md matrix before refactor |
| \`tests/\` | ✅ Read/Write | Update tests alongside code changes |
| \`docs/\` | ✅ Read/Write | Keep docs in sync with code |
| \`scripts/\` | ✅ Read/Write | Validate with \`bash scripts/validate.sh\` |
| \`.env\` | 🔒 Read-only | Use \`.env.example\` as reference only |
| \`secrets/\` | 🔒 Blocked | Use GitHub Actions secrets |
| \`infra/\` | 🔒 Blocked | DevOps Agent only + approval |

---

## 5. MCP Integration & Routing

### MCP Priority Table

| Task | Primary | Secondary | Fallback |
|------|---------|-----------|----------|
| Read repo | github | filesystem | git |
| Write code | filesystem | github | - |
| Commit/push | git | github | - |
| Create PR | github | taskmanager | - |
| Run tests | shell | playwright | - |
| Update docs | filesystem | github | - |
| Deploy | shell (k8s) | github | - |
| Notify | webhook (n8n) | slack-api | github-comment |
| Schedule job | kestra-api | n8n-api | - |
| Chat support | chatwoot-api | langchain | web-search |

### MCP Configuration (codex.sh wrapper)

```bash
#!/bin/bash
# bin/codex.sh — Wrapper para Codex CLI com context + MCPs pré-configurados
MODEL=${1:-gpt-5}
REASONING=${2:-high}
TASK=${3:-}

if [ -z "$TASK" ]; then
  echo "Usage: ./bin/codex.sh [gpt-5] [high|medium] 'your task'"
  exit 1
fi

# Load context (fail if missing)
[ -f "docs/AGENTS.md" ] || { echo "❌ docs/AGENTS.md not found"; exit 1; }
[ -f "PRD.md" ] || { echo "❌ PRD.md not found"; exit 1; }
[ -f "tutor/progress.state.md" ] || { echo "❌ tutor/progress.state.md not found"; exit 1; }

# Run Codex with MCPs
codex \
  -m "$MODEL" \
  -c "model.reasoning_effort=$REASONING" \
  --context "docs/AGENTS.md PRD.md tutor/progress.state.md" \
  --full-auto \
  "$TASK"
```

**Usage:**

```bash
./bin/codex.sh gpt-5 high "feat: add OAuth2 login with TypeScript types"
# Runs up to 7 hours, auto-validates, creates PR when done
```

---

## 6. Webhook Integration (N8N/Kestra/Chatwoot)

### Webhook Endpoints

| Event | Endpoint | Payload | Handler |
|-------|----------|---------|---------|
| **PR Opened** | \`POST /webhooks/github-pr\` | owner, pr_id, title | Code Agent assigns reviewers |
| **Tests Failed** | \`POST /webhooks/ci-failed\` | job_name, error, pr_id | Code Agent debug + re-run |
| **Deploy Success** | \`POST /webhooks/deploy-ok\` | version, env, url | Chatwoot notify + Slack |
| **N8N Trigger** | \`POST /webhooks/n8n-event\` | workflow_id, data | Execute automated task |
| **Kestra Trigger** | \`POST /webhooks/kestra-schedule\` | job_id, timestamp | Run scheduled workflow |
| **Chatwoot Message** | \`POST /webhooks/chatwoot-new-msg\` | customer, message | LLM bot responds + escalate |

### N8N Integration Schema

```json
{
"name": "ZapPro Automation Hub",
"workflows": [
{
"id": "github-to-slack",
"trigger": "webhook:github-pr",
"actions": [
{ "type": "parse_github_payload" },
{ "type": "format_slack_message" },
{ "type": "send_slack_notification" }
]
},
{
"id": "deploy-to-customers",
"trigger": "webhook:deploy-ok",
"actions": [
{ "type": "get_deployment_info" },
{ "type": "notify_chatwoot" },
{ "type": "update_github_release" }
]
},
{
"id": "customer-support-escalation",
"trigger": "webhook:chatwoot-message",
"actions": [
{ "type": "extract_intent_langchain" },
{ "type": "search_knowledge_base" },
{ "type": "respond_or_escalate" }
]
}
]
}
```

### Kestra Integration (Event-Driven Jobs)

```yaml
# workflows/zappro-daily-health.yml
namespace: zappro
id: daily-health-check
description: Daily health checks + performance metrics
triggers:
id: daily-schedule
type: io.kestra.core.models.triggers.types.Schedule
cron: "0 2 * * *" # 02:00 BRT daily
tasks:
id: run-tests
type: io.kestra.core.tasks.scripts.Bash
commands:
"cd /app && make test"
id: security-scan
type: io.kestra.core.tasks.scripts.Bash
commands:
"bash scripts/secret-scan.sh && bash scripts/security-scan.sh"
id: notify-slack
type: io.kestra.plugin.notifications.slack.SlackIncomingWebhook
webhook: "{{ env.SLACK_WEBHOOK_URL }}"
payload:
text: "✅ Daily health check passed"
id: backup-database
type: io.kestra.core.tasks.scripts.Bash
commands:
"pg_dump {{ env.DATABASE_URL }} > /backups/$(date +%Y-%m-%d).sql"
```

### Chatwoot Bot Integration (Customer Support)

```python
# src/integrations/chatwoot_bot.py
from fastapi import APIRouter, HTTPException
from langchain import OpenAI, ConversationChain
from langchain.memory import ConversationBufferMemory

router = APIRouter(prefix="/webhooks/chatwoot", tags=["chatbot"])

@router.post("/incoming-message")
def incoming_message(payload: dict):
    # TODO: implement handler (example placeholder)
    return {"ok": True}
```
async def handle_chatwoot_message(payload: dict):
"""
Webhook from Chatwoot: customer sends message
LLM bot responds, escalate if needed
"""
customer_id = payload.get("customer_id")
message = payload.get("message")
conversation_id = payload.get("conversation_id")
text
# Search knowledge base (RAG)
knowledge = await search_knowledge_base(message)

# LLM response
memory = ConversationBufferMemory()
chain = ConversationChain(
    llm=OpenAI(model="gpt-4"),
    memory=memory,
    system_prompt="Você é suporte técnico ZapPro. Use knowledge base para responder."
)
response = chain.run(message + "\n\nKnowledge: " + knowledge)

# Send response back to Chatwoot
await send_chatwoot_reply(conversation_id, response)

# If escalation needed
if "escalation_required" in response:
    await assign_to_human(conversation_id, "support_team")

return {"status": "ok", "message_id": conversation_id}

async def search_knowledge_base(query: str) -> str:
"""Vector search in ZapPro docs + FAQs"""
# Implementation: Pinecone/Weaviate vector DB
pass
async def send_chatwoot_reply(conv_id: str, text: str):
"""Send message back via Chatwoot API"""
# Implementation: POST to Chatwoot API
pass
text

---

## 7. Kanban & ADM (GitHub Projects Automation)

### Kanban Workflow States


BACKLOG → IN PROGRESS → IN REVIEW → DONE → ARCHIVED
↓ ↓ ↓ ↓
New Working Reviewers Merged
Issue (Assigned) (2 min) (Deployed)
text

### GitHub Projects Automation Rules


.github/workflows/kanban-automation.yml
name: Kanban Automation
on:
issues:
types: [opened, closed]
pull_request:
types: [opened, ready_for_review, review_requested, closed]
jobs:
update-board:
runs-on: ubuntu-latest
steps:
- name: New issue → Backlog
if: github.event.action == 'opened' && github.event.issue
uses: actions/github-script@v6
with:
script: |
const issue = context.payload.issue;
const project = await github.rest.projects.listForRepo({
owner: context.repo.owner,
repo: context.repo.repo
});
// Add issue to "Backlog" column
text
  - name: PR opened → In Progress (with assignee)
    if: github.event.action == 'opened' && github.event.pull_request
    run: |
      # Move PR to "In Progress" column
      # Auto-assign reviewers based on path filters

  - name: PR merged → Move to Done
    if: github.event.action == 'closed' && github.event.pull_request.merged
    run: |
      # Move to "Done" column
      # Mark as deployed if deploy succeeds

  - name: Stale (30 days) → Archive
    uses: actions/stale@v8
    with:
      days-before-stale: 30
      operations-per-run: 100
      stale-label: 'stale'

text

### ADM Dashboard (Real-time Metrics)


src/api/v1/admin/dashboard.py
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
from sqlalchemy import func
router = APIRouter(prefix="/v1/admin/dashboard", tags=["admin"])
@router.get("/kanban-metrics")
async def get_kanban_metrics(db: Session = Depends(get_db)):
"""
Real-time dashboard:
- Total issues/PRs by status
- Cycle time (avg days in each stage)
- Burndown chart
- Agent performance metrics
"""
now = datetime.utcnow()
week_ago = now - timedelta(days=7)
text
metrics = {
    "issues": {
        "backlog": db.query(Issue).filter(Issue.state == "BACKLOG").count(),
        "in_progress": db.query(Issue).filter(Issue.state == "IN_PROGRESS").count(),
        "in_review": db.query(Issue).filter(Issue.state == "IN_REVIEW").count(),
        "done": db.query(Issue).filter(Issue.state == "DONE").count()
    },
    "prs": {
        "total": db.query(PullRequest).count(),
        "merged": db.query(PullRequest).filter(PullRequest.merged_at.isnot(None)).count(),
        "avg_review_time_hours": db.query(
            func.avg(
                func.extract("epoch", PullRequest.merged_at - PullRequest.created_at) / 3600
            )
        ).scalar() or 0
    },
    "agents": {
        "code_agent": {
            "tasks_completed": db.query(AgentLog).filter(
                AgentLog.agent_type == "code",
                AgentLog.status == "SUCCESS",
                AgentLog.created_at >= week_ago
            ).count(),
            "success_rate": 0.95,  # 95% PRs merged without issues
            "avg_time_hours": 2.5
        },
        "qa_agent": {
            "tests_run": 156,
            "coverage": 82,  # 82%
            "bugs_found": 3
        }
    },
    "cycle_time": {
        "avg_days_backlog_to_done": 7.2,
        "fastest_issue_hours": 2,
        "slowest_issue_days": 30
    }
}

return metrics

@router.get("/burndown-chart")
async def get_burndown_chart(db: Session = Depends(get_db)):
"""Sprint burndown: issues completed vs planned"""
sprint_start = datetime.utcnow().replace(day=1)
text
daily_data = []
for day in range(30):
    date = sprint_start + timedelta(days=day)
    completed = db.query(Issue).filter(
        Issue.completed_at <= date,
        Issue.sprint == "current"
    ).count()
    daily_data.append({
        "date": date.isoformat(),
        "completed": completed,
        "planned": 50  # hardcoded sprint size
    })

return {"burndown": daily_data}

text

---

## 8. Validation & Quality Gates

### Pre-Commit Hooks (Local)


#!/bin/bash
.git/hooks/pre-commit
echo "🔍 Running pre-commit checks..."
1. Lint
make lint || exit 1
2. Tests
make test || exit 1
3. Secret scan
bash scripts/secret-scan.sh || exit 1
4. Type check (Python)
mypy src/ || echo "⚠️ Type hints incomplete"
echo "✅ Pre-commit checks passed"
text

### CI Pipeline (GitHub Actions)


name: CI/CD Full Pipeline
on: [push, pull_request]
jobs:
validate:
runs-on: ubuntu-latest
strategy:
matrix:
python-version: ['3.11', '3.12']
node-version: ['20', '22']
text
steps:
  - uses: actions/checkout@v4
  
  - name: Lint
    run: make lint
  
  - name: Tests
    run: make test
  
  - name: Security Scan
    run: bash scripts/security-scan.sh
  
  - name: Coverage Report
    uses: codecov/codecov-action@v3
    with:
      token: ${{ secrets.CODECOV_TOKEN }}
      files: ./coverage.xml
      flags: unittests
      fail_ci_if_error: true
      minimum_coverage: 80
  
  - name: Deploy Preview (if PR)
    if: github.event_name == 'pull_request'
    run: |
      bash scripts/deploy.sh preview-${{ github.event.number }}
  
  - name: Deploy Production (if main merge)
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    run: bash scripts/deploy.sh production

text

---

## 9. Escalation & Troubleshooting

### When Agent Loops


Ctrl+C to interrupt
Review loop_guard.py output
Refine prompt (add line numbers + file paths)
Retry with explicit MCP mapping
text

### When Tests Fail >5 Retries


Agent escalates to GitHub issue (label: codex-blocked)
Manual intervention required
Fix uploaded to PR draft
Agent continues after human approval
text

### When Secrets Detected


Pre-push hook blocks commit
Email security@zappro.site
Revert commit, remove secret
Retry
text

---

## 10. Documentation & Resources

- **PRD.md** — Product roadmap, features, acceptance criteria
- **tutor/prompt.md** — LLM context template
- **tutor/progress.state.md** — Current sprint status
- **docs/WORKFLOW.md** — Git + PR process
- **docs/DECISION.md** — Refactor vs rewrite matrix
- **scripts/validate.sh** — Full validation suite
- **bin/codex.sh** — Codex CLI wrapper with safety checks

---

**Version 2.0 Complete: Multi-Agent + N8N/Kestra/Chatwoot Ready**
