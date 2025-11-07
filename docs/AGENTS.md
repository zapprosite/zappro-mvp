# AGENTS — Manual Operacional para LLMs

Estas instruções especializam o `AGENTS.md` raiz para qualquer agente/automation que atue dentro de `docs/`, `scripts/`, `frontend/` ou `src/`.

## Fluxo recomendado
1. **Contrato**: leia `PRD.md`, `AGENTS.md` (raiz) e este documento antes de planejar algo.
2. **Planejamento**: derive um plano curto (≤5 passos) e valide com humano via PR/issue antes de executar.
3. **Bootstrap**: somente após aprovação execute alterações atômicas focadas no objetivo.
4. **Validação**: rode `bash scripts/security-scan.sh` + `bash scripts/validate.sh` (ou os jobs equivalentes no GitHub Actions) antes de propor PR.
5. **Evidências**: anexe nos comentários de PR quais etapas do plano foram cumpridas, riscos e próximos passos.

## Guardrails técnicos
- **Sem rede externa** durante a análise local e nenhum download de dependência não declarado em `requirements.txt` ou `frontend/package.json`.
- **Sem credenciais**: use placeholders (`<token>`). Secrets reais ficam apenas em `.env` local ou nos Actions Secrets (`SLACK_WEBHOOK_URL`, `CI_SMTP_*`, tokens de deploy). Consulte `.env.example`.
- **Arquivos proibidos**: nada em `secrets/**` ou `infra/prod/**` sem aprovação explícita dos CODEOWNERS.
- **Scripts obrigatórios**: toda automação que mexa em deploy ou segurança deve registrar logs em `logs/` e reutilizar `scripts/deploy.sh`, `scripts/security-scan.sh` e `scripts/secret-scan.sh`.
- **Tests/docs juntos**: alterações em `src/**` exigem atualizar `tests/**` e documentação correlata (`docs/`, `README.md`).

## LLMs + CI/CD
- **CI (`ci.yml`)**: garante lint, cobertura, Playwright, security scan e artifacts. Se um agente propuser mudanças que afetam build, descreva no PR quais matrizes (Python/Node) precisam de atenção.
- **CD (`cd.yml`)**: gera imagens no GHCR e executa `scripts/deploy.sh`. Ajuste o script ao provedor real (SSH, Kubernetes, Fly.io) sem remover logs ou validação de `docker compose config`.
- **Notificações**: Slack e email são disparados em reviews. Nunca grave `SLACK_WEBHOOK_URL` ou credenciais SMTP em arquivos; mantenha-os apenas nos secrets.

## Integração com GitHub Projects
- Sempre vincule PRs/Issues a um card do Project. Quando a etapa `deploy-preview` comentar o link da prévia, mova o card para “Revisão”.
- Use automações de Projects para mover cards para “Pronto para deploy” quando `CI / policy` e `CD / deploy production` ficarem verdes.

## Exemplos de automações aprovadas
| Tarefa | Expectativa |
| --- | --- |
| Atualizar dependências | Use `scripts/dependency-watch.sh` e abra PR citando CVEs. |
| Criar blueprint de feature | Referencie seções do `PRD.md`, atualize `docs/*.md` e descreva riscos no PR. |
| Ajustar pipelines | Atualize `<repo>/.github/workflows/*.yml`, explique decisões no README e valide com `scripts/validate.sh`. |

Falhas em qualquer etapa acima devem parar o agente imediatamente e solicitar revisão humana.
