# Guia de Segredos e Variáveis de Ambiente — ZapPro

## Por que segredos não devem ser versionados?
Variáveis de ambiente (.env) podem conter credenciais de bancos, tokens de APIs e chaves privadas. Se forem commitadas no Git, tornam‑se públicas para todo o time (ou internet), gerando riscos de invasão, vazamento de dados e custos financeiros. O repositório mantém apenas `.env.example` com placeholders; arquivos reais nunca devem ser versionados.

## Como criar e gerenciar seu `.env` local
1. Copie o modelo: `cp .env.example .env`.
2. Abra o `.env` apenas no seu editor local (VS Code/Neovim). Evite ferramentas que sincronizam automaticamente com nuvem.
3. Preencha valores reais somente no arquivo `.env` (ou `.env.local`) armazenado fora do Git.
4. Ajuste permissões: `chmod 600 .env` no Linux/macOS, garantindo que só você possa ler/escrever.
5. Nunca envie `.env` por e‑mail, chat ou commit; compartilhe segredos via gerenciadores seguros.
6. Para atualizar, utilize `dotenv set` (ou scripts da equipe) e registre alterações no vault designado.

## Uso do `.env.example`
- Serve como documentação das variáveis esperadas.
- Preencha com valores fictícios ou strings como `CHANGE_ME`.
- Adicione comentários explicando formato esperado.
- Sempre que surgir uma nova variável, atualize o `.env.example`.

## Produção e ambientes gerenciados
- **Vault/HashiCorp**: recomendado para clusters Kubernetes ou workflows multi-equipe.
- **AWS Secrets Manager / Parameter Store**: integra com IAM e rotations automáticas.
- **Google Secret Manager / Azure Key Vault**: opções nativas para clouds específicas.
- Politique revisões periódicas, rotação automática e alerte o time de SRE a cada novo segredo.

## Verificações automáticas
- Execute `bash scripts/secret-scan.sh` antes de cada commit/push; o script procura padrões como `password=` ou chaves AWS.
- Configure pre-commit hook para rodar `scripts/secret-scan.sh` automaticamente (adapte `scripts/pre-commit.sh` se desejar).
- No CI, acrescente etapa que faila o build quando segredos forem detectados.

## Uso com Python/FastAPI e Docker Compose
- **Python/FastAPI**: utilize `python-dotenv` (ou `pydantic-settings`) para carregar `.env` em desenvolvimento:
  ```python
  from dotenv import load_dotenv
  load_dotenv()
  ```
  Em produção, prefira variáveis do ambiente do container/host.
- **Docker Compose**: defina `env_file: .env` ou variáveis no `docker-compose.yml`. Nunca bake segredos na imagem.
- Para jobs/CI, injete segredos via parâmetros (`docker run --env-file` ou `--env VAR=value`).

## Checklist mínimo (exemplos)
- `DATABASE_URL=postgresql+psycopg://user:password@host:5432/db`
- `SECRET_KEY=super-long-random-string`
- `API_TOKEN=change_me`
- `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000`
- `ZAPPRO_ALLOWED_HOSTS=["localhost","127.0.0.1"]`

> **Regra de Ouro:** **Nunca compartilhe ou suba `.env`, `.env.local` ou equivalentes no Git.**

## Recursos recomendados
- python-dotenv: https://pypi.org/project/python-dotenv/
- pydantic-settings: https://docs.pydantic.dev/latest/concepts/pydantic_settings/
- HashiCorp Vault: https://www.vaultproject.io/
- AWS Secrets Manager: https://aws.amazon.com/secrets-manager/
- Security best practices em Docker: https://docs.docker.com/engine/swarm/secrets/
- OWASP Cheat Sheet – Secrets Management: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html

Mantenha este guia sempre por perto e atualize‑o quando novas rotinas de segurança forem estabelecidas.
