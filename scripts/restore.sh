#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 <backup.tar.gz>" >&2
  exit 1
fi

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
ARCHIVE=$1

if [[ ! -f "$ARCHIVE" ]]; then
  echo "backup file not found: $ARCHIVE" >&2
  exit 1
fi

LOG_FILE="$ROOT_DIR/logs/restore.log"
mkdir -p "$(dirname "$LOG_FILE")"

printf "%s [restore] restoring %s\n" "$(date --iso-8601=seconds)" "$ARCHIVE" | tee -a "$LOG_FILE"

tar -xzf "$ARCHIVE" -C "$ROOT_DIR"

printf "%s [restore] restore completed\n" "$(date --iso-8601=seconds)" | tee -a "$LOG_FILE"
