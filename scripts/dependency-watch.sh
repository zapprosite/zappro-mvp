#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
LOG_FILE="$ROOT_DIR/logs/dependency-watch.log"
mkdir -p "$ROOT_DIR/logs"

log() {
  printf "%s [deps] %s\n" "$(date --iso-8601=seconds)" "$1" | tee -a "$LOG_FILE"
}

log "pip outdated (virtualenv required)"
if [[ -d "$ROOT_DIR/venv" ]]; then
  source "$ROOT_DIR/venv/bin/activate"
  pip list --outdated --format=columns | tee -a "$LOG_FILE" || log "pip list failed"
else
  log "venv ausente; execute make install antes de rodar o watcher"
fi

log "npm outdated"
if command -v npm >/dev/null 2>&1; then
  (cd "$ROOT_DIR/frontend" && npm outdated || log "npm outdated reported issues") | tee -a "$LOG_FILE"
else
  log "npm indisponível; instale Node.js para monitorar dependências"
fi
