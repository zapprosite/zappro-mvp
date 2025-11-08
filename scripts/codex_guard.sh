#!/usr/bin/env bash
set -euo pipefail

PROMPT_FILE="${1:-}"
NAME="${2:-task}"
TIMEOUT_MIN="${3:-40}"

if [[ -z "${PROMPT_FILE}" || ! -f "${PROMPT_FILE}" ]]; then
  echo "prompt file inválido: ${PROMPT_FILE}" >&2; exit 2
fi

mkdir -p logs .codex
exec 9> .codex/lock ; flock -n 9 || { echo "Já existe execução ativa"; exit 3; }

LOG="logs/${NAME}.log"
RETRY=1

run_once () {
  # sem flags arriscadas; só modelo e full-auto
  timeout "${TIMEOUT_MIN}m" codex -m gpt-5 --full-auto "$(cat "${PROMPT_FILE}")" | tee -a "${LOG}"
}

set +e
run_once
RC=$?
if [[ $RC -ne 0 && $RETRY -gt 0 ]]; then
  echo "[guard] retry 1/1 após falha (rc=${RC})" | tee -a "${LOG}"
  sleep 3
  run_once
  RC=$?
fi
set -e

if [[ $RC -ne 0 ]]; then
  echo "[guard] falhou com rc=${RC}" | tee -a "${LOG}"
  exit $RC
fi

echo "[guard] concluído: ${NAME}" | tee -a "${LOG}"
