#!/usr/bin/env bash
set -euo pipefail

SESSION="overnight"
tmux has-session -t "$SESSION" 2>/dev/null || tmux new -s "$SESSION" -d
run() { tmux send-keys -t "$SESSION" "$1" C-m; }

# Guard
run "make lint && make test || true"

# T1
run "codex -m gpt-5 -c model.reasoning_effort=high --full-auto \"[FastAPI lifespan refactor] Critical Fixes: migrate to lifespan; add /healthz. Validation: make lint && make test; curl :8000/healthz. MCP: filesystem,github,git,shell.\""

# T2
run "codex -m gpt-5 -c model.reasoning_effort=high --full-auto \"[Auth async rewrite] Critical Fixes: async JWT; precise errors; tests. Validation: make lint && pytest -q tests/test_auth.py. MCP: filesystem,github,git,shell,task_manager.\""

# T3
run "codex -m gpt-5 -c model.reasoning_effort=high --full-auto \"[Pydantic v2 migration] Critical Fixes: migrate models/schemas; remove deprecated validators. Validation: make lint && make test. MCP: filesystem,github,git,shell.\""

# T4
run "codex -m gpt-5 -c model.reasoning_effort=high --full-auto \"[Docker healthchecks] Add healthchecks and deps. Validation: docker compose up -d && docker inspect api ... . MCP: filesystem,shell,git,github.\""

# T5
run "codex -m gpt-5 -c model.reasoning_effort=high --full-auto \"[CI hardening] Codecov 80% + secret scan. Validation: PR checks green. MCP: github,shell,git.\""

# T6
run "codex -m gpt-5 -c model.reasoning_effort=high --full-auto \"[Frontend bootstrap] Next.js 15 home page lists projects via /api/projects. Validation: make lint; playwright smoke. MCP: filesystem,github,git,playwright.\""

# T7
run "codex -m gpt-5 -c model.reasoning_effort=high --full-auto \"[E2E smoke tests] playwright covers / and /healthz. Validation: make test-e2e. MCP: playwright,shell,github,git.\""

# T8
run "codex -m gpt-5 -c model.reasoning_effort=high --full-auto \"[API endpoints doc] generate docs/api-endpoints.md. Validation: headings present. MCP: filesystem,github,git.\""

echo "Queued. Attach: tmux attach -t $SESSION"
