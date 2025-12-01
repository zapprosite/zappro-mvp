[Pydantic v2 migration]

## Critical Fixes
1. src/models/* e src/schemas/*: migrar para Pydantic v2.
2. Substituir validators deprecados por model_validate/model_dump.

## Validation Steps
- shell: make lint && make test

## MCP Usage Priority
filesystem → github → git → shell

Commit: refactor(models): migrate to Pydantic v2
