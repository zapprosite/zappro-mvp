#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 4 ]]; then
  echo "usage: $0 <environment> <backend-image[@digest]> <frontend-image[@digest]> <git-ref>" >&2
  exit 1
fi

ENVIRONMENT="$1"
BACKEND_REF="$2"
FRONTEND_REF="$3"
GIT_REF="$4"

split_ref() {
  local ref="$1"
  local image="$ref"
  local digest=""
  if [[ "$ref" == *@* ]]; then
    image="${ref%@*}"
    digest="${ref#*@}"
  fi
  printf '%s %s' "$image" "$digest"
}

IFS=' ' read -r BACKEND_IMAGE BACKEND_DIGEST <<<"$(split_ref "$BACKEND_REF")"
IFS=' ' read -r FRONTEND_IMAGE FRONTEND_DIGEST <<<"$(split_ref "$FRONTEND_REF")"

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
LOG_DIR="$ROOT_DIR/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/deploy-${ENVIRONMENT}.log"

log() {
  printf "%s [deploy:%s] %s\n" "$(date --iso-8601=seconds)" "$ENVIRONMENT" "$1" | tee -a "$LOG_FILE"
}

log "Preparing deployment for ref ${GIT_REF}"
log "Backend image ${BACKEND_IMAGE} (digest: ${BACKEND_DIGEST:-n/a})"
log "Frontend image ${FRONTEND_IMAGE} (digest: ${FRONTEND_DIGEST:-n/a})"

if command -v docker >/dev/null 2>&1; then
  log "Validating docker compose manifest"
  (cd "$ROOT_DIR" && docker compose config >/dev/null)
else
  log "Docker CLI not available; skipping compose validation"
fi

MANIFEST="$LOG_DIR/deploy-${ENVIRONMENT}-$(date +%s).json"
cat <<EOF > "$MANIFEST"
{
  "environment": "${ENVIRONMENT}",
  "git_ref": "${GIT_REF}",
  "backend_image": "${BACKEND_IMAGE}",
  "backend_digest": "${BACKEND_DIGEST}",
  "frontend_image": "${FRONTEND_IMAGE}",
  "frontend_digest": "${FRONTEND_DIGEST}",
  "generated_at": "$(date --iso-8601=seconds)"
}
EOF

log "Deployment manifest written to ${MANIFEST}"
