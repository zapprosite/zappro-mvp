#!/usr/bin/env bash
set -euo pipefail

# Script de testes automatizados dentro do venv
# Uso: scripts/test.sh [unit|integration|all|path]

SCOPE="${1:-all}"
RESULTS_DIR="test-results"
mkdir -p "$RESULTS_DIR/coverage_html"

PYTEST_COMMON_ARGS=(
  -q
  --disable-warnings
  --maxfail=1
  --cov=src
  --cov-report=term-missing
  --cov-report=xml:"${RESULTS_DIR}/coverage.xml"
  --cov-report=html:"${RESULTS_DIR}/coverage_html"
  --junitxml "${RESULTS_DIR}/junit.xml"
)

echo "[tests] Escopo: ${SCOPE}"
echo "[tests] Resultados em: ${RESULTS_DIR}"

case "$SCOPE" in
  unit)
    echo "[tests] Rodando testes unitários"
    pytest "tests" "-m" "unit" "${PYTEST_COMMON_ARGS[@]}"
    ;;
  integration)
    echo "[tests] Rodando testes de integração"
    pytest "tests" "-m" "integration" "${PYTEST_COMMON_ARGS[@]}"
    ;;
  all)
    echo "[tests] Rodando toda a suíte"
    pytest tests "${PYTEST_COMMON_ARGS[@]}"
    ;;
  *)
    echo "[tests] Rodando alvo específico: ${SCOPE}"
    pytest "${SCOPE}" "${PYTEST_COMMON_ARGS[@]}"
    ;;
esac

echo "[tests] Concluído. Cobertura XML: ${RESULTS_DIR}/coverage.xml"
echo "[tests] Relatório HTML: ${RESULTS_DIR}/coverage_html/index.html"

