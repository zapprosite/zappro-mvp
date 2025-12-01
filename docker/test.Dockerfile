FROM python:3.11-slim

# Diretório de trabalho no container
WORKDIR /app

# Variáveis de ambiente padrão Python e venv
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv

# Criar venv e preparar ferramentas essenciais
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential curl && \
    rm -rf /var/lib/apt/lists/* && \
    python -m venv "$VIRTUAL_ENV" && \
    . "$VIRTUAL_ENV/bin/activate" && \
    pip install --upgrade pip wheel setuptools

# Garantir que o venv esteja no PATH
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copiar requirements (backend) e instalar deps de aplicação + teste
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir pytest pytest-cov coverage

# Copiar apenas o que é necessário para executar testes (código e migrações)
COPY src ./src
COPY alembic ./alembic
COPY tests ./tests

# Diretório de resultados de testes
RUN mkdir -p /app/test-results

# Comando padrão: rodar testes unitários e integração com cobertura
CMD ["bash", "-lc", "pytest -q --disable-warnings --maxfail=1 --cov=src --cov-report=term-missing --cov-report=xml:/app/test-results/coverage.xml --cov-report=html:/app/test-results/coverage_html tests"]

