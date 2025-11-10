#!/usr/bin/env bash
set -euo pipefail

PROMPT_FILE="${1:-}"
NAME="${2:-task}"
TIMEOUT_MIN="${3:-40}"

if [[ -z "${PROMPT_FILE}" || ! -f "${PROMPT_FILE}" ]]; then
  echo "prompt file inválido: ${PROMPT_FILE}" >&2; exit 2
fi

mkdir -p logs .codex
LOG="logs/${NAME}.log"
RETRY=1

record_task_failure() {
  local source="$1"
  local prompt="$2"
  local reason="$3"
  local rc="$4"
  local log_file="$5"
  local timestamp
  timestamp="$(date -u +"%Y%m%dT%H%M%SZ")"
  local failure_file="task_failure_${timestamp}.md"
  local excerpt
  excerpt="$(tail -n 40 "${log_file}" 2>/dev/null || true)"
  {
    echo "# Falha automática — ${source}"
    echo ""
    echo "- timestamp: ${timestamp}"
    echo "- prompt: ${prompt}"
    echo "- motivo: ${reason}"
    echo "- exit_code: ${rc}"
    echo ""
    echo "## Trecho de log (${log_file})"
    echo '```'
    echo "${excerpt}"
    echo '```'
  } > "${failure_file}"
  printf "\n| %s | %s | %s | %s (veja %s) |\n" "$(date -Iseconds)" "${source}" "${reason}" "${prompt}" "${failure_file}" \
    >> docs/LOG.md
  echo "Falha registrada em ${failure_file}; atualize o task_manager."
}

run_once () {
  timeout "${TIMEOUT_MIN}m" codex -m gpt-5 --full-auto "$(cat "${PROMPT_FILE}")" | tee -a "${LOG}"
}

set +e
run_once; RC=$?
if [[ $RC -ne 0 && $RETRY -gt 0 ]]; then
  echo "[guard] retry 1/1 após falha (rc=${RC})" | tee -a "${LOG}"
  sleep 3
  run_once; RC=$?
fi
set -e

if [[ $RC -ne 0 ]]; then
  record_task_failure "scripts/codex_guard.sh" "${PROMPT_FILE}" "codex guard RC=${RC}" "${RC}" "${LOG}"
fi

exit $RC
