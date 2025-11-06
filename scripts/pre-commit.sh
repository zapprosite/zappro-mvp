#!/usr/bin/env bash
set -euo pipefail

root_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

echo "[pre-commit] preparando ambiente virtual..."
make -C "$root_dir" bootstrap >/dev/null

echo "[pre-commit] lintando..."
make -C "$root_dir" lint

echo "[pre-commit] rodando testes..."
make -C "$root_dir" test

echo "[pre-commit] security scan..."
bash "$root_dir/scripts/security-scan.sh"

echo "[pre-commit] tudo certo!"
