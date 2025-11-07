# Security Policy

## Supported Versions
| Version | Supported |
| ------- | --------- |
| 0.1.x   | ✅        |

## Reporting Vulnerabilities
Envie e-mail para `security@zappro.site` contendo:
- Descrição detalhada da vulnerabilidade
- Passo a passo para reproduzir
- Impacto potencial (dados afetados, escalonamento possível)

Tempo de resposta: até 48h para triagem inicial.

## Security Measures
- Varredura de segredos em pre-push (`scripts/secret-scan.sh`) e nos pipelines.
- `pip-audit` + `npm audit` obrigatórios em `make security`.
- Cabeçalhos CSP, rate limit e políticas HTTP rígidas ativadas no backend.
- Tokens JWT com rotação a cada 15 minutos e revogação por TTL.
- Monitoramento diário de dependências via `scripts/dependency-watch.sh`.
