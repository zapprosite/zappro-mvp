# Segurança e Hardening — ZapPro

## Controles Implementados
- **Headers**: CSP dinâmica via middleware (nonce em produção), Referrer-Policy, Permissions-Policy, X-Content-Type-Options, X-Frame-Options, Cache-Control `no-store`.
- **CORS**: configurável via `ZAPPRO_CORS__*` (origens, métodos, headers) com defaults seguros.
- **Rate limiting**: janela fixa com TTL configurável (`ZAPPRO_RATE_LIMIT__MAX_REQUESTS`, `WINDOW_SECONDS`, `TTL_SECONDS`, `MAX_ENTRIES`), fallback em memória e suporte futuro a Redis.
- **Trusted hosts**: aceita strings ou JSON (`ZAPPRO_ALLOWED_HOSTS`), proxies de confiança (`ZAPPRO_TRUSTED_PROXIES`) e normalização de IP.
- **Request ID**: `X-Request-ID` reaproveitado apenas para hosts whitelisted; colisões registradas e monitoradas.

## Scripts de Segurança
- `bash scripts/security-scan.sh`: ruff (unsafe), bandit, pip-audit, secret scan, trivy (se instalado) e npm audit.
- `bash scripts/daily-health.sh`: monitora `/health` (API/frontend) gravando em `logs/health.log` sem falhar offline.
- `bash scripts/backup.sh`: gera artefato em `backups/`; use junto ao `scripts/restore.sh`.
- `bash scripts/dependency-watch.sh`: lista libs desatualizadas (pip/npm) e alimenta `logs/dependency-watch.log`.

## Rotina Recomendadas
1. `make security` antes de abrir PR.
2. `make backup` pós-merge para snapshot local.
3. Agendar `scripts/daily-health.sh` via cron/Kestra para monitoramento.
4. Executar `scripts/security-scan.sh` diariamente e `scripts/dependency-watch.sh` semanalmente (cron/Kestra/context7).

## Próximos Passos
- Integrar scanners externos (Snyk, Dependabot) ao pipeline.
- Adicionar autenticação e RBAC (ver PRD — Fase 1).
- Configurar WAF e rate-limit distribuído no gateway.
