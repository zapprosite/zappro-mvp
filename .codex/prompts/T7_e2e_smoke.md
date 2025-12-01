[E2E smoke tests]

## Enhancements
1. tests/e2e/smoke.spec.ts cobre "/" e "/healthz".
2. Rodar no CI em PR.

## Validation Steps
- shell: make test-e2e

## MCP Usage Priority
playwright → shell → github → git

Commit: test(e2e): add smoke test for home and healthz
