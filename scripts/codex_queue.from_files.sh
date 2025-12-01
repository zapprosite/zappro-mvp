#!/usr/bin/env bash
set -euo pipefail
validate(){ set +e; make lint && make test; RC=$?; set -e; return $RC; }
rollback(){ git reset --hard HEAD; }
commit_if(){ git diff --quiet || { git add -A; git commit -m "$1"; } }

mkdir -p logs
LOG="logs/codex_queue.log"

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

FILES=(.codex/prompts/T1_fastapi_lifespan.md .codex/prompts/T2_auth_async.md .codex/prompts/T3_pydantic_v2.md .codex/prompts/T4_healthchecks.md .codex/prompts/T5_ci_hardening.md .codex/prompts/T6_frontend_bootstrap.md .codex/prompts/T7_e2e_smoke.md .codex/prompts/T8_api_docs.md)
MSGS=("refactor(api): migrate to FastAPI lifespan and add /healthz" "fix(auth): rewrite JWT utils async + tests" "refactor(models): migrate to Pydantic v2" "ci(docker): add healthchecks and deps order" "ci(workflows): enable codecov and enforce secret-scan" "feat(web): bootstrap Next.js 15 home with projects list" "test(e2e): add smoke test for home and healthz" "docs(api): add api-endpoints.md")

git checkout -B feature/codex-overnight
for i in "${!FILES[@]}"; do
  f="${FILES[$i]}"; msg="${MSGS[$i]}"
  test -f "$f" || { echo "faltando $f"; exit 2; }

  set +e
  timeout 40m codex -m gpt-5 --full-auto "$(cat "$f")" | tee -a "${LOG}"
  RC=${PIPESTATUS[0]}
  set -e
  if [[ $RC -ne 0 ]]; then
    echo "falha codex em $f (rc=${RC})" | tee -a "${LOG}"
    record_task_failure "scripts/codex_queue.from_files.sh" "$f" "codex RC=${RC}" "$RC" "${LOG}"
    rollback
    continue
  fi

  if validate; then
    commit_if "$msg"
    git push -u origin feature/codex-overnight || true
  else
    echo "validação falhou em $f" | tee -a "${LOG}"
    record_task_failure "scripts/codex_queue.from_files.sh" "$f" "validação falhou" "$RC" "${LOG}"
    rollback
  fi
  sleep 3
done
