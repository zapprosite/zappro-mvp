#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
LOG_FILE="$ROOT_DIR/logs/health.log"
API_URL=${API_URL:-http://127.0.0.1:8000/health}
FRONTEND_URL=${FRONTEND_URL:-http://127.0.0.1:3000/health}

mkdir -p "$(dirname "$LOG_FILE")"

log() {
  printf "%s [health] %s\n" "$(date --iso-8601=seconds)" "$1" | tee -a "$LOG_FILE"
}

check_url() {
  local label=$1
  local url=$2
  if curl -fsS "$url" >/dev/null; then
    log "$label reachable"
  else
    log "$label unreachable at $url"
  fi
}

check_url "API" "$API_URL"
check_url "Frontend" "$FRONTEND_URL"
