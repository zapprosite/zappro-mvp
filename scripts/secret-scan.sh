#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
PATTERNS=('AWS_SECRET_ACCESS_KEY' 'AWS_ACCESS_KEY_ID' 'GOOGLE_API_KEY' 'password=' 'secret=' 'BEGIN RSA PRIVATE KEY')

LOG_FILE="$ROOT_DIR/logs/security.log"
mkdir -p "$(dirname "$LOG_FILE")"

EXIT_STATUS=0

EXCLUDES=(':!logs/*' ':!node_modules/*' ':!venv/*' ':!AGENTS.md')

for pattern in "${PATTERNS[@]}"; do
  if git -C "$ROOT_DIR" grep -n --color=never -E "$pattern" -- "${EXCLUDES[@]}" >/tmp/secret-scan.out 2>/dev/null; then
    echo "$(date --iso-8601=seconds) [secret-scan] Found matches for pattern '$pattern':" | tee -a "$LOG_FILE"
    cat /tmp/secret-scan.out | tee -a "$LOG_FILE"
    EXIT_STATUS=1
  fi
done

rm -f /tmp/secret-scan.out || true
exit $EXIT_STATUS
