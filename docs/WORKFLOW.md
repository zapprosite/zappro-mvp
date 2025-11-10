# Fluxo de Trabalho Operacional

Este documento resume as etapas oficiais para novos ciclos de entrega. A fonte de verdade para cada etapa é o [Codex Runbook](./CODEX_RUNBOOK.md); aqui registramos apenas o mapa de decisões.

## Sequência recomendada
1. **Preparar contexto:** ler `docs/CODEX_RUNBOOK.md`, `docs/INDEX.md` e `tutor/TUTOR_MASTER_PROMPT.md` antes de propor mudanças.
2. **Planejar atomizações:** fatiar tarefas curtas (≤ 25 arquivos) e documentar riscos.
3. **Executar e validar:** seguir os comandos do runbook (`make lint`, `make test`, `make test-e2e`, `bash scripts/validate.sh`).
4. **Registrar entrega:** atualizar o `README.md`/`PRD.md` quando relevante e fechar PRs com checklist completo.

## Auditoria e histórico
Materiais legados (ex.: arquivos de auditoria, governance antiga, security-hardening) foram arquivados em `docs/_archive/**`. Use-os apenas para auditoria e referencie sempre `docs/CODEX_RUNBOOK.md` como guia principal.
