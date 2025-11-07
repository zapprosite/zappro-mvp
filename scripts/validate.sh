#!/usr/bin/env bash
# Comando de validação completa antes do PR
make lint
make test
bash scripts/smoke_test.sh
