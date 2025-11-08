[Auth async rewrite]

## Critical Fixes
1. src/utils/auth.py: async-friendly JWT encode/decode.
2. RS256 via env; erros Missing/Expired/Invalid token com mensagens precisas.
3. Ajustar/adição de testes em tests/test_auth.py.

## Enhancements
- Type hints completos.

## Validation Steps
- shell: make lint && pytest -q tests/test_auth.py

## MCP Usage Priority
filesystem → github → git → shell → task_manager

Commit: fix(auth): rewrite JWT utils async + tests
