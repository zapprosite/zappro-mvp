#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
LOG_FILE="$ROOT_DIR/logs/security.log"
mkdir -p "$ROOT_DIR/logs"

log() {
  printf "%s [security] %s\n" "$(date --iso-8601=seconds)" "$1" | tee -a "$LOG_FILE"
}

ensure_venv() {
  if [[ ! -d "$ROOT_DIR/venv" ]]; then
    log "venv not found; running make install"
    make -C "$ROOT_DIR" install >/dev/null
  fi
}

ensure_venv
source "$ROOT_DIR/venv/bin/activate"

log "running ruff --unsafe-fixes"
ruff check "$ROOT_DIR/src" "$ROOT_DIR/tests" --unsafe-fixes || true

log "running bandit static analysis"
bandit -q -r "$ROOT_DIR/src" || log "bandit completed with findings (see exit code $?)"

log "running pip-audit vulnerability scan"
pip-audit || log "pip-audit reported vulnerable dependencies"

log "checking repository for potential secrets"
bash "$ROOT_DIR/scripts/secret-scan.sh" || log "secret scan reported potential hits"

if command -v trivy >/dev/null 2>&1; then
  log "running trivy filesystem scan"
  trivy fs --scanners vuln,secret --severity HIGH,CRITICAL "$ROOT_DIR" || log "trivy completed with findings"
else
  log "trivy not available; skipping container scan"
fi

if command -v npm >/dev/null 2>&1; then
  if [[ -d "$ROOT_DIR/frontend/node_modules" ]]; then
    log "running npm audit (production)"
    (cd "$ROOT_DIR/frontend" && npm audit --omit=dev || log "npm audit completed with findings")
  else
    log "node_modules ausente; execute 'npm install' antes de rodar npm audit"
  fi
fi

log "security scan finished"
