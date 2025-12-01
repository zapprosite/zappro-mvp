#!/usr/bin/env bash
set -euo pipefail

echo "[trae-preview] checking environment"
if command -v trae >/dev/null 2>&1; then
  echo "[trae-preview] Trae detected → exposing 8000/3000"
  (trae preview --port 8000 >/dev/null 2>&1 || true)
  (trae preview --port 3000 >/dev/null 2>&1 || true)
  exit 0
fi

if [[ -n "${TRAE_PREVIEW_BASE:-}" ]]; then
  echo "[trae-preview] Trae preview base detected"
  echo "API Preview: ${TRAE_PREVIEW_BASE}/8000"
  echo "Web Preview: ${TRAE_PREVIEW_BASE}/3000"
  exit 0
fi

echo "[trae-preview] local URLs: http://127.0.0.1:8000/healthz and http://127.0.0.1:3000/"
