[FastAPI lifespan refactor]

## Critical Fixes
1. src/main.py: migrate @app.on_event startup/shutdown to lifespan context.
2. Add GET /healthz → {"status":"ok"} with 200.

## Enhancements
- Structured logging on startup/shutdown.

## Validation Steps
- shell: make lint && make test
- shell: curl http://localhost:8000/healthz | jq .status=="ok"

## MCP Usage Priority
filesystem → github → git → shell

Commit: refactor(api): migrate to FastAPI lifespan and add /healthz
