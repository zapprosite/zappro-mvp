# Novo Projeto com o Template (LLM)

Este passo‑a‑passo orienta como iniciar um projeto novo usando este template com VS Code (Remote – WSL) e Codex CLI no terminal.

## Pré‑requisitos (no WSL/Ubuntu)
- Git e Bash (já presentes no template/CI)
- Node.js LTS e Python 3 (para MCPs e utilitários)
- ripgrep (busca rápida), opcional para servers de busca
- (Opcional) Playwright e browsers para E2E

Dica: mantenha tudo instalado dentro do WSL para evitar problemas de caminho e permissões.

## 1) Criar o projeto a partir do template
- Copie esta pasta para o novo repositório (ou use como template).
- Ajuste `CODEOWNERS` se necessário.
- Configure o remoto (ex.):
  - `git remote add origin <URL>`
  - `git push -u origin main`

## 2) Preencher o PRD
- Edite `PRD.md` (Seção 0) e escolha a stack (linguagem, framework, DB, ORM, testes, lint, execução).
- Adicione o mínimo das seções 1.. para contextualizar MVP e fases.

## 3) Remover o guia humano
- Este arquivo `Guia.md` é só para humanos e não deve ser usado pela LLM.
- Remoção (manual):
  - `git rm Guia.md && git commit -m "docs: remove Guia.md (PRD concluído; iniciar LLM)"`

## 4) Kickoff da LLM (Fase 0 — Bootstrap)
- Prompt sugerido (cole para a LLM):
  """
  Leia PRD.md e obedeça estritamente AGENTS.md e .codex/policy.json. Confirme a stack escolhida na Seção 0 do PRD e proponha um plano curto para a Fase 0 (Bootstrap). Em seguida, implemente apenas o mínimo necessário:
  - Scaffold em src/** (ou estrutura equivalente), endpoint/rota de saúde;
  - Arquivos de dependências e scripts (fmt, lint, test, dev, run) via Makefile/justfile;
  - Atualize docs/how-to-run.md com comandos concretos;
  - Mantenha diffs pequenos, sem tocar secrets/ e infra/prod/;
  - Rode scripts/validate.sh localmente e descreva validação.
  Abra um PR pequeno com escopo, riscos, validação e próximos passos para a Fase 1.
  """

## 5) Validação local e PR
- `bash scripts/validate.sh` → deve imprimir `validate: OK`.
- Abra um PR pequeno. CI roda validação e policy‑check.
- No GitHub, habilite proteção da branch `main`, exija CI verde, configure CODEOWNERS, e prepare secrets fora do repo (para fases futuras).

## 6) Próximas fases
- Fase 1 (MVP): funcionalidades essenciais + testes de integração.
- Fase 2 (Observabilidade/Qualidade): logs, métricas, cobertura, SAST.
- Fase 3 (Infra/Deploy): containerização, migrations, staging, deploy.

Referências: `README.md`, `AGENTS.md`, `docs/how-to-run.md`, `docs/saas-blueprint.md`.
