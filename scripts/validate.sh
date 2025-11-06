#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
export PYTHONPATH="$root:${PYTHONPATH:-}"

log() {
  printf "[validate] %s\n" "$1"
}

need() {
  command -v "$1" >/dev/null 2>&1 || { echo "Falta comando: $1" >&2; exit 1; }
}

need git
need curl

# Checagens básicas
[ -f "$root/PRD.md" ] || { echo "PRD.md ausente"; exit 1; }
[ -f "$root/AGENTS.md" ] || { echo "AGENTS.md ausente"; exit 1; }
[ -f "$root/.codex/policy.json" ] || { echo ".codex/policy.json ausente"; exit 1; }
[ -f "$root/.github/workflows/ci.yml" ] || { echo "CI ausente"; exit 1; }

grep -qi "Visão Geral" "$root/PRD.md" || { echo "PRD sem 'Visão Geral'"; exit 1; }

log "instalando dependências..."
make -C "$root" bootstrap >/dev/null

log "executando lint..."
make -C "$root" lint

log "executando testes..."
make -C "$root" test

api_port=${API_PORT:-8000}
log "verificando healthcheck no http://127.0.0.1:${api_port}/health"

source "$root/venv/bin/activate"
uvicorn src.main:app --host 127.0.0.1 --port "${api_port}" >/dev/null 2>&1 &
server_pid=$!
trap 'kill $server_pid 2>/dev/null || true' EXIT

for attempt in {1..10}; do
  if curl -fsS "http://127.0.0.1:${api_port}/health" >/dev/null 2>&1; then
    log "healthcheck ok"
    break
  fi
  sleep 1
  if [ "$attempt" -eq 10 ]; then
    echo "Falha ao verificar health endpoint" >&2
    exit 1
  fi
done

kill $server_pid 2>/dev/null || true
trap - EXIT

log "rodando policy-check"
if git rev-parse --verify -q HEAD >/dev/null 2>&1; then
  CHANGED_FILES=$(git diff --name-only ${GITHUB_BASE_REF:+origin/${GITHUB_BASE_REF}...}HEAD || true)
  CHANGED_FILES="$CHANGED_FILES" "$root/scripts/policy-check.sh" || true
fi

echo "validate: OK"
