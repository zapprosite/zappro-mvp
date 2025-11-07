#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="${PROJECT_ROOT}/logs"
LOG_FILE="${LOG_DIR}/bootstrap.log"

mkdir -p "${LOG_DIR}"
touch "${LOG_FILE}"

timestamp() {
    date +"%Y-%m-%dT%H:%M:%S%z"
}

{
    if ! command -v docker >/dev/null 2>&1; then
        echo "[$(timestamp)] ❌ Docker CLI não encontrado. Instale Docker Desktop/Engine antes de rodar este script."
        exit 1
    fi

    if ! docker info >/dev/null 2>&1; then
        echo "[$(timestamp)] ❌ Docker daemon indisponível. Inicie o serviço e tente novamente."
        exit 1
    fi

    echo "[$(timestamp)] ▶ Starting Docker services..."
    docker compose -f "${PROJECT_ROOT}/docker-compose.yml" up -d

    echo "[$(timestamp)] ▶ Waiting for containers to stabilize..."
    sleep 2

    echo "[$(timestamp)] ▶ Running Alembic migrations..."
    (cd "${PROJECT_ROOT}" && ./venv/bin/alembic upgrade head)

    echo "[$(timestamp)] ▶ Executing pytest suite..."
    (cd "${PROJECT_ROOT}" && ./venv/bin/python -m pytest tests/ -v)

    echo "[$(timestamp)] ✅ Bootstrap completed successfully."
} 2>&1 | tee -a "${LOG_FILE}"
