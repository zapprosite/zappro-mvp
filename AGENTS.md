# AGENTS — Regras para LLMs e Contribuidores

Escopo: estas regras valem para o repositório inteiro. Subpastas podem ter AGENTS.md mais específicos que prevalecem nelas.

Princípios:
- Fonte única: PRD.md é o contrato do produto.
- Mudanças atômicas: pequenas, focadas, com justificativa.
- Testes e docs: sempre juntos ao código.
- Sem segredos: nunca commitar credenciais.

Pode alterar (Bootstrap + iterações):
- src/**, tests/**, docs/**
- README.md, CONTRIBUTING.md, Makefile, scripts/**
- .github/workflows/**, .gitignore, .editorconfig, AGENTS.md, PRD.md

Não alterar (sem aprovação explícita de CODEOWNERS):
- secrets/**, infra/prod/**

Ferramentas e conduta:
- Sem rede para baixar dependências arbitrárias durante análise.
- Use buscas rápidas (rg) e edições via patch aplicável.
- Não renomeie nem delete arquivos massivamente; evite mudanças cosméticas amplas.
- Se tocar em src/**, também atualize tests/** e docs/** relevantes.
- Se `Guia.md` existir, ignore-o (conteúdo é para humanos) e não o modifique. O humano poderá removê-lo antes da execução do Bootstrap.
- Proteja segredos: nunca insira chaves (AWS, GCP, tokens) ou strings com `secret=`/`password=`; use placeholders e `.env.example`.
- Ao criar novas automações, inclua validações de segurança (lint, testes, scans) e registre saídas em `logs/`.
- Antes de subir mudanças críticas, execute `bash scripts/security-scan.sh` e `bash scripts/validate.sh`.

Validação e fluxo:
- Siga também o `Guia.md` para a ordem operacional (PRD → plano → bootstrap → validação → PR).
- Rode `scripts/validate.sh` localmente; CI deve passar.
- PRs devem incluir plano, risco, validação e próximos passos.

