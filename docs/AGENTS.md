# AGENTS.md - ZapPro MVP

Estas instruções complementam `AGENTS.md` (raiz) para qualquer automação/LLM que opere em `docs/`, `scripts/`, `frontend/` ou `src/`. Leia ambos antes de agir.

## Agent Configuration
- Model: **GPT-5-Codex (high reasoning)**
- Scope: **Read code, write workflows, manage PRs** — nunca editar `secrets/**` ou `infra/prod/**` sem CODEOWNERS.
- Triggers: **PR opened, main branch push**; execuções ad-hoc precisam de aprovação humana registrada em issue/PR.
- Permissions: **read:code, write:actions, write:labels**. Nenhuma outra permissão deve ser solicitada pelo agente.

## CI/CD Workflow Rules
- All PRs must pass lint + tests (`make lint`, `make test`) before merge; re-rodar localmente `bash scripts/validate.sh`.
- Matrix builds: **Python 3.11/3.12** e **Node 20/22** (ver `.github/workflows/ci.yml`). Falhas devem ser citadas no PR junto com links dos artifacts.
- Staging preview obrigatório em PR (`cd.yml` → environment `staging`); produção apenas em push na `main`.
- Coverage threshold mínimo: **80%** (`pytest --cov ... --cov-report=xml`). PRs devem anexar o relatório se cobertura cair abaixo do baseline.
- Execute `bash scripts/security-scan.sh` antes de pedir review e anexe o resumo no PR (mesmo se CI já rodar).

## Security
- Never commit secrets (use GitHub Secrets). `.env.example` é a única fonte versionada; valores reais ficam fora do Git ou em Vaults.
- Secret scan via pre-push hook: rode `bash scripts/secret-scan.sh` (já incluso em `scripts/security-scan.sh`); PR sem esse log será bloqueado.
- LLM usage: read-only on sensitive files; qualquer tentativa de leitura fora dos diretórios permitidos precisa de justificativa em comentário público.
- Sem rede externa para instalar dependências não listadas em `requirements.txt` ou `frontend/package.json`. Logs obrigatórios em `logs/`.

## Automation Runbook
- Stale issue labeler: marque `stale` após **30 dias** sem atividade e notifique o autor; fechar somente após +7 dias sem resposta.
- Auto-assign reviewers: `@Will.zappro` (backend) e `@jpmarcenaria` (frontend) em toda alteração nos respectivos diretórios.
- Deploy preview URL deve ser comentado automaticamente no PR (saída do job `deploy-preview`); humanos confirmam validação antes do merge.

### Operação diária em 5 passos
1. **Contrato** — leia `PRD.md`, `AGENTS.md` (raiz) e este arquivo antes de planejar.
2. **Planejamento** — proponha plano curto (≤5 passos) e aguarde validação explícita.
3. **Bootstrap** — execute apenas mudanças atômicas. Se tocar `src/**`, atualize `tests/**` e documentação relacionada.
4. **Validação** — rode `bash scripts/security-scan.sh` + `bash scripts/validate.sh`. Falha interrompe o fluxo até correção.
5. **Evidências** — abra PR com plano cumprido, riscos, cobertura, próximos passos e link do preview.

### Guardrails técnicos rápidos
- Sem rede externa durante análise local.
- Scripts críticos: reutilize `scripts/deploy.sh`, `scripts/security-scan.sh`, `scripts/secret-scan.sh`.
- Logs de automação devem ir para `logs/` com carimbo de data ISO-8601.
- Use placeholders (`<token>`) em prompts/comentários públicos.

### GitHub Projects e sincronização
- Vincule Issues/PRs a um card do Project (colunas: Backlog → Em andamento → Revisão → Pronto para deploy).
- Automatize transição para **Revisão** quando o PR é aberto e para **Pronto para deploy** quando `CI / policy` + `CD / deploy production` estiverem verdes.
- Integrações externas (Linear/ClickUp) só podem ler dados após o workflow `workflow_run` concluir com sucesso.

### Automations aprovadas
| Tarefa | Expectativa |
| --- | --- |
| Atualizar dependências | Use `scripts/dependency-watch.sh`, cite CVEs e rode CI completo. |
| Criar blueprint de feature | Baseie-se em `PRD.md`, atualize `docs/*.md`, descreva riscos/testes. |
| Ajustar pipelines | Edite `.github/workflows/*.yml`, explique decisões no README e valide com `scripts/validate.sh`. |

Falhas em qualquer etapa acima devem parar o agente e acionar revisão humana imediatamente.
