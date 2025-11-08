#!/usr/bin/env bash
set -euo pipefail

# Canon: manter
CANON=( \
  "README.md"
  "PRD.md"
  "docs/WORKFLOW.md"
  "docs/AGENTS.md"
  "docs/SECURITY.md"
  "docs/CODEX_RUNBOOK.md"
  "tutor/TUTOR_MASTER_PROMPT.md"
)

# Exageros/longos: arquivar com stub
TO_ARCHIVE=( \
  "docs/saas-blueprint.md"
  "docs/new-project.md"
  "docs/architecture.md"
  "docs/MARKDOWN_AUDIT_TASK.md"
  "docs/governance-codex-dual-mail.md"
  "docs/metodo-contrato-codex-cli-com-mcp.md"
  "docs/LOG.md"
  "overnight_task.txt"
  "plespecty.md"
  "tutor/prompt.md"
  "tutor/all_templates.md"
  "ROADMAP.md"
  "SECURITY.md"     # stub para apontar docs/SECURITY.md
)

# 1) pasta de arquivo
mkdir -p docs/_archive

# 2) move e cria stubs
for f in "${TO_ARCHIVE[@]}"; do
  if [ -f "$f" ]; then
    dest="docs/_archive/$f"
    mkdir -p "$(dirname "$dest")"
    git mv "$f" "$dest" || mv "$f" "$dest"
    # stub no caminho original com ponte clara para evitar links quebrados
    cat > "$f" <<STUB
> **Movido para arquivo**  
> Caminho: \`docs/_archive/$f\`  
> Este é um stub. Não editar aqui. Consultar o arquivo no caminho acima.

STUB
    git add "$f"
  fi
done

# 3) stub de segurança na raiz apontando para docs/SECURITY.md, se não existir
if [ -f "SECURITY.md" ] && ! grep -q "docs/SECURITY.md" SECURITY.md; then
  cat > SECURITY.md <<'STUB'
> **Origem canônica:** [`docs/SECURITY.md`](docs/SECURITY.md)
STUB
  git add SECURITY.md
fi

# 4) índice enxuto de docs
mkdir -p docs
cat > docs/INDEX.md <<'MD'
# INDEX — Documentação Canônica

Canônicos:
- [PRD.md](../PRD.md)
- [docs/WORKFLOW.md](WORKFLOW.md)
- [docs/AGENTS.md](AGENTS.md)
- [docs/SECURITY.md](SECURITY.md)
- [docs/CODEX_RUNBOOK.md](CODEX_RUNBOOK.md)
- [tutor/TUTOR_MASTER_PROMPT.md](../tutor/TUTOR_MASTER_PROMPT.md)

Arquivados (referência, não editar):
- Veja a pasta [`docs/_archive/`](./_archive/)

MD
git add docs/INDEX.md

# 5) README: linkar índice se não houver referência
if [ -f README.md ] && ! grep -qi "docs/INDEX.md" README.md; then
  printf "\n\n## Documentação\nConsulte o índice: [docs/INDEX.md](docs/INDEX.md)\n" >> README.md
  git add README.md
fi

# 6) workflow de checagem de links internos (lychee). opcional se não usar actions.
mkdir -p .github/workflows
cat > .github/workflows/docs-link-check.yml <<'YAML'
name: docs-link-check
on:
  pull_request:
  push:
    paths:
      - '**/*.md'
jobs:
  lychee:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: lycheeverse/lychee-action@v1
        with:
          args: >
            --verbose
            --no-progress
            --exclude-path docs/_archive
            --accept 200,206,429
            .
        env:
          GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}
YAML
git add .github/workflows/docs-link-check.yml

echo "Poda concluída localmente. Faça commit/push em uma branch."
