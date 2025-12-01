# Ambiente de Testes com Docker (venv)

Este documento descreve como construir e executar um ambiente de testes reproduzível e isolado usando Docker e um ambiente virtual Python (venv) dentro do container.

## Visão Geral
- Base: `python:3.11-slim`
- venv: criado automaticamente em `/opt/venv`
- Dependências: instaladas via `requirements.txt` (inclui `pytest` e `pytest-cov`)
- Banco (integração): `postgres:16-alpine` com credenciais padrão de desenvolvimento
- Relatórios: cobertura XML/HTML e JUnit em `test-results/`

## Comandos de Build e Execução
- Build do serviço de testes:
  - `docker compose build tests`
- Executar toda a suíte:
  - `docker compose run --rm tests`
- Executar somente unit/integration:
  - `docker compose run --rm tests bash -lc "scripts/test.sh unit"`
  - `docker compose run --rm tests bash -lc "scripts/test.sh integration"`
- Executar arquivo ou diretório específico:
  - `docker compose run --rm tests bash -lc "scripts/test.sh tests/test_models.py"`

## Como Acessar os Serviços
- API (desenvolvimento): `http://localhost:${API_PORT:-8000}`
- Frontend (desenvolvimento): `http://localhost:${FRONTEND_PORT:-3000}`
- Postgres (teste/integração): disponível internamente pelo hostname `postgres` e porta `5432`

> Observação: o serviço `tests` não expõe porta; ele monta o código, executa `pytest` e finaliza.

## Variáveis de Ambiente de Teste
- `DATABASE_URL`: por padrão `${DATABASE_URL:-postgresql://zappro:zappro@postgres:5432/zappro}`
- `ZAPPRO_ALLOWED_HOSTS`: `api,localhost,127.0.0.1,testserver`
- Ajuste valores em `.env.example` ou sobreponha via `docker compose run -e ...`

## Relatórios de Cobertura
- XML: `test-results/coverage.xml`
- HTML: `test-results/coverage_html/index.html`
- JUnit: `test-results/junit.xml`

## Executar Testes Específicos
- Por marcador (se definido):
  - `docker compose run --rm tests bash -lc "pytest -m unit -q --cov=src"`
- Por caminho:
  - `docker compose run --rm tests bash -lc "pytest tests/test_models.py -q --cov=src"`

## Solução de Problemas Comuns
- Erro de conexão com Postgres:
  - Verifique saúde do serviço: `docker compose ps` e `docker compose logs postgres`
  - Aguarde `depends_on: condition: service_healthy` cumprir o healthcheck
  - Confirme `DATABASE_URL` apontando para `postgres` no compose
- Pacotes faltando:
  - Rebuild após alterar `requirements.txt`: `docker compose build tests`
- Cobertura não gerada:
  - Verifique saída do `pytest` no terminal; arquivos são gravados em `test-results/`
- Permissões em arquivos `test-results/`:
  - No Windows, ajuste permissões do host ou rode com `--rm` para container limpar estado ao sair

## Reprodutibilidade e Isolamento
- venv interno no container garante isolamento das dependências
- Volumes montam apenas código e saída de testes, evitando acoplamento com sistema host
- Healthchecks e `depends_on` garantem que os testes iniciem após banco estar pronto

## Dicas
- Para ver relatório HTML de cobertura, abra `zappro-mvp/test-results/coverage_html/index.html` no navegador
- Integre com CI/CD usando artefatos `coverage.xml` e `junit.xml`

