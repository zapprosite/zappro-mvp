.PHONY: bootstrap fmt lint test dev run build validate install clean security backup restore playwright-audit

VENV ?= venv
PYTHON ?= python3
PIP ?= $(VENV)/bin/pip
UVICORN ?= $(VENV)/bin/uvicorn
PYTEST ?= $(VENV)/bin/pytest
ISORT ?= $(VENV)/bin/isort
BLACK ?= $(VENV)/bin/black
RUFF ?= $(VENV)/bin/ruff

export PYTHONPATH := src

$(VENV)/bin/activate:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@touch $(VENV)/bin/activate

bootstrap: $(VENV)/bin/activate

install: bootstrap
	@echo "Dependencies installed into $(VENV)"

fmt: bootstrap
	$(RUFF) check src tests --fix || true
	$(ISORT) --profile black src tests
	$(BLACK) src tests

lint: bootstrap
	$(RUFF) check src tests
	$(BLACK) --check src tests
	$(ISORT) --profile black --check-only src tests

test: bootstrap
	$(PYTEST) -q

dev: bootstrap
	$(UVICORN) src.main:app --reload --host 0.0.0.0 --port 8000

run: bootstrap
	$(UVICORN) src.main:app --host 0.0.0.0 --port 8000

build:
	@echo "Build target reserved for container/image pipeline."

validate:
	bash scripts/validate.sh

clean:
	rm -rf $(VENV) .pytest_cache .ruff_cache

security: bootstrap
	bash scripts/security-scan.sh

backup:
	bash scripts/backup.sh

restore:
	@if [ -z "$(ARCHIVE)" ]; then echo "usage: make restore ARCHIVE=backups/<file>.tar.gz"; exit 1; fi
	bash scripts/restore.sh "$(ARCHIVE)"

test-e2e:
	npx kill-port 8000 3000 || true
	bash scripts/trae_preview.sh || true
	npm --prefix frontend run test:e2e
	npx kill-port 8000 3000 || true

playwright-audit:
	cd frontend && npx playwright test
