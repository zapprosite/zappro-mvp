# Segurança Operacional

O runbook principal (`docs/CODEX_RUNBOOK.md`) centraliza as políticas de segurança em vigor (headers, rate limiting, secrets, scans). Utilize este documento para lembrar os pontos-chave e o histórico extra está em `docs/_archive/security-hardening.md`.

## Checklist mínimo
- Autenticação com tokens JWT e renovação segura
- Middleware adicionando cabeçalhos: `X-Content-Type-Options`, `X-Frame-Options`, `Strict-Transport-Security` quando relevante
- Scanner de segredos e auditorias (`bash scripts/secret-scan.sh`, `bash scripts/security-scan.sh`)
- Logs e alertas no `docs/_archive/LOG.md` apenas para auditoria; priorize o runbook para decisões atuais.
