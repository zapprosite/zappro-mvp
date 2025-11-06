#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
BACKUP_DIR="${ROOT_DIR}/backups"
STAMP=$(date +"%Y%m%dT%H%M%S")
ARCHIVE="${BACKUP_DIR}/zappro-backup-${STAMP}.tar.gz"

mkdir -p "$BACKUP_DIR"

LOG_FILE="$ROOT_DIR/logs/backup.log"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
  printf "%s [backup] %s\n" "$(date --iso-8601=seconds)" "$1" | tee -a "$LOG_FILE"
}

log "creating archive $ARCHIVE"
tar --exclude='.git' --exclude='node_modules' --exclude='venv' -czf "$ARCHIVE" -C "$ROOT_DIR" \
  src frontend docs scripts Makefile requirements.txt docker-compose.yml docker

log "backup created"
echo "$ARCHIVE"
