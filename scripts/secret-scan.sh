#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

# Patterns tuned to avoid false positives
# Real secrets only: actual keys/tokens, not variable names or documentation
PATTERNS=(
  'AKIA[0-9A-Z]{16}'                    # AWS Access Key ID (real format)
  'AIza[0-9A-Za-z_-]{35}'               # Google API Key (real format)
  '(^|[^A-Za-z_])password\s*=\s*["\047][^"\047]{8,}["\047]'  # password = "actual_value"
  '(^|[^A-Za-z_])secret\s*=\s*["\047][^"\047]{8,}["\047]'    # secret = "actual_value"
  'BEGIN RSA PRIVATE KEY'                # Private keys
  'BEGIN PRIVATE KEY'                    # Generic private keys
  'ghp_[0-9a-zA-Z]{36}'                  # GitHub Personal Access Token
  'sk-[0-9a-zA-Z]{48}'                   # OpenAI API Key
)

LOG_FILE="$ROOT_DIR/logs/security.log"
mkdir -p "$(dirname "$LOG_FILE")"

EXIT_STATUS=0

# Exclude: logs, node_modules, venv, config files, test files, scanner itself
EXCLUDES=(
  ':!logs/*'
  ':!node_modules/*'
  ':!venv/*'
  ':!.venv/*'
  ':!*.pyc'
  ':!*.log'
  ':!.codex/policy.json'
  ':!scripts/secret-scan.sh'
  ':!tests/test_*.py'
  ':!**/test_*.py'
  ':!AGENTS.md'
  ':!guia-secrets.md'
)

for pattern in "${PATTERNS[@]}"; do
  # Use git grep to respect .gitignore and exclude patterns
  if git -C "$ROOT_DIR" grep -niE "$pattern" -- . "${EXCLUDES[@]}" > /tmp/secret-scan.out 2>/dev/null; then
    echo "$(date --iso-8601=seconds) [secret-scan] ⚠️  Found matches for pattern '$pattern':" | tee -a "$LOG_FILE"
    cat /tmp/secret-scan.out | tee -a "$LOG_FILE"
    EXIT_STATUS=1
  fi
done

rm -f /tmp/secret-scan.out 2>/dev/null || true

if [ $EXIT_STATUS -eq 0 ]; then
  echo "$(date --iso-8601=seconds) [secret-scan] ✅ No secrets detected" | tee -a "$LOG_FILE"
else
  echo "$(date --iso-8601=seconds) [secret-scan] ❌ Potential secrets found - review above" | tee -a "$LOG_FILE"
fi

exit $EXIT_STATUS

# Exclude package-lock.json from scans (contains hashes, not secrets)
EXCLUDE_FILES="${EXCLUDE_FILES} --exclude='package-lock.json'"
