# Índice de Documentos Canônicos

Este registro expõe a fonte única de verdade para o time e aponta os arquivos que agora vivem apenas em `docs/_archive/**`.

## Documentos Ativos

| Arquivo | Propósito | Referência principal |
|---|---|---|
| `README.md` | Visão geral do produto, setups e links rápidos. | `PRD.md`, `docs/CODEX_RUNBOOK.md` |
| `PRD.md` | Contrato do produto, métricas e prioridades. | `docs/CODEX_RUNBOOK.md`, `docs/INDEX.md` |
| `docs/CODEX_RUNBOOK.md` | Runbook com validações, guardrails e checklist. | `README.md`, `PRD.md`, `tutor/TUTOR_MASTER_PROMPT.md` |
| `docs/INDEX.md` | Este mapa de documentos, histórico e dependências. | `docs/CODEX_RUNBOOK.md` |
| `docs/api-endpoints.md` | Contratos REST e exemplos operacionais. | `docs/CODEX_RUNBOOK.md` |
| `docs/WORKFLOW.md` | Sequência mínima para planejar, executar e validar. | `docs/CODEX_RUNBOOK.md` |
| `docs/SECURITY.md` | Políticas de segurança atualizadas e checklists. | `docs/CODEX_RUNBOOK.md`, `scripts/security-scan.sh` |
| `tutor/TUTOR_MASTER_PROMPT.md` | Prompt permanente com regras e métricas de agente. | `docs/CODEX_RUNBOOK.md`, `tutor/prompt.md` |

## Arquivos Arquivados (auditoria)
Todos os demais documentos agora residem em `docs/_archive/**`. Use-os apenas para histórico; as decisões operacionais vivem em `docs/CODEX_RUNBOOK.md`.

| Arquivo stub | Registro arquivado | Referência recomendada |
|---|---|---|
| `docs/AGENTS.md` | `docs/_archive/AGENTS.md` | `docs/CODEX_RUNBOOK.md` |
| `docs/architecture.md` | `docs/_archive/architecture.md` | `docs/CODEX_RUNBOOK.md` |
| `docs/DECISION.md` | `docs/_archive/DECISION.md` | `docs/CODEX_RUNBOOK.md` |
| `docs/governance-codex-dual-mail.md` | `docs/_archive/governance-codex-dual-mail.md` | `docs/CODEX_RUNBOOK.md` |
| `docs/MARKDOWN_AUDIT_TASK.md` | `docs/_archive/MARKDOWN_AUDIT_TASK.md` | `docs/CODEX_RUNBOOK.md` |
| `docs/LOG.md` | `docs/_archive/LOG.md` | `docs/CODEX_RUNBOOK.md` |
| `docs/how-to-run.md` | `docs/_archive/how-to-run.md` | `docs/CODEX_RUNBOOK.md` |
| `docs/metodo-contrato-codex-cli-com-mcp.md` | `docs/_archive/metodo-contrato-codex-cli-com-mcp.md` | `docs/CODEX_RUNBOOK.md` |
| `docs/new-project.md` | `docs/_archive/new-project.md` | `docs/CODEX_RUNBOOK.md` |
| `docs/saas-blueprint.md` | `docs/_archive/saas-blueprint.md` | `docs/CODEX_RUNBOOK.md` |
| `docs/security-hardening.md` | `docs/_archive/security-hardening.md` | `docs/SECURITY.md` |
| `docs/POLICIES/LOOP_GUARD.md` | `docs/_archive/POLICIES/LOOP_GUARD.md` | `docs/WORKFLOW.md` |

Acesse `docs/_archive/**` apenas quando precisar auditar decisões passadas; todos os fluxos ativos são descritos nos itens acima.
