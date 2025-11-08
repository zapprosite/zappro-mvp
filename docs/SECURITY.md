# SECURITY.md - ZapPro MVP Security Policy

**Última atualização:** 7 Nov 2025  
**Status:** Active & Enforced  
**Compliance:** OWASP Top 10, LGPD-Ready

---

[!IMPORTANT]
Vulnerabilidade? Não abra issue pública. Envie para security@zappro.site. SLA de triagem: 48 horas.

[!WARNING]
Nunca inclua segredos em código, logs ou PRs. Use somente GitHub Actions secrets e `.env.example`.

## Vulnerability Reporting

### Responsible Disclosure
- **Email:** security@zappro.site
- **Response SLA:** Initial triage within 48 horas
- **Confidentiality:** Reports held private until patch released

### Report Template
```text
Subject: [SECURITY] Vulnerability in ZapPro MVP

Description of vulnerability:
[Clear, concise description]

Steps to reproduce:
1. ...
2. ...

Potential impact:
[Business/technical impact]

Suggested fix (optional):
[If you have a patch]
```

---

## Security Scanning Pipeline

### Pre-Push Hooks
```bash
scripts/secret-scan.sh
# Detecta: API keys, tokens, database URIs, credentials
# Action: Blocks commit if found
```

### CI Pipeline Security Checks
```yaml
jobs:
  security:
    - ruff --select=S (bandit rules)
    - bandit -r src -f json
    - npm audit --audit-level=moderate
    - pip-audit --skip-deprecated
    - OWASP Dependency Check (optional)
```

### Scanning Frequency
- **On every commit:** Secret scan
- **On every PR:** Ruff + Bandit + npm audit
- **Daily (02:00 BRT):** Dependency watch + CVE lookup

---

## Dependency Management

### Approval Thresholds
- **LOW:** Auto-merge if >80 coverage maintained
- **MODERATE:** Manual review required, deprecate if no fix
- **HIGH:** Immediate remediation, hotfix PR
- **CRITICAL:** Hotfix + production patch within 24h

### Dependency Update Policy
- **Patch updates:** Auto-merge weekly
- **Minor updates:** Manual PR review monthly
- **Major updates:** Breaking changes → separate epic

---

## API Security

### Authentication & Authorization
- **Token:** JWT (RS256 asymmetric)
- **Expiration:** 15 minutos (refresh token valid 30 dias)
- **Scope:** User role-based (admin, manager, operator)
- **Rotation:** Refresh token invalidated on password change

### Rate Limiting
```text
Public endpoints: 100 req/min per IP
Authenticated: 1000 req/min per user
Admin: No limit (trusted)
```

### CORS Policy
```yaml
allowed_origins:
  - https://app.zappro.site      # Production
  - https://preview-*.zappro.site # PR previews
  - http://localhost:3000         # Development
allow_credentials: true
```

### CSRF Protection
- Form token validation on state-changing operations (POST/PUT/DELETE)
- Token rotated per session
- SameSite=Strict on cookies

---

## Data Protection

### Database Security
- **Encryption at rest:** PostgreSQL pgcrypto
- **Encryption in transit:** TLS 1.3
- **Query parameterization:** SQLAlchemy ORM (no raw SQL)
- **Backup:** Daily encrypted snapshots to S3

### PII Handling (LGPD Compliance)
- **Collection consent:** Explicit opt-in documented
- **Retention:** Delete on account termination (30-day grace)
- **Data export:** Available via API (GDPR Article 20)
- **Audit log:** All PII access logged to immutable audit table

### Secrets Management
- **Never in code:** \`.env\` excluded via \`.gitignore\`
- **GitHub Actions:** Use \`${{ secrets.* }}\` only
- **Local dev:** \`.env.example\` documents structure
- **Rotation:** Quarterly secret rotation policy

---

## Infrastructure Security

### Docker Security
- **Base images:** Alpine Linux 3.20 (minimal attack surface)
- **Non-root user:** Runs as \`app:app\` (UID 1000)
- **Read-only filesystem:** \`/\` mounted read-only except \`/tmp\`, \`/var\`
- **No privileged mode:** \`--privileged\` never used in compose

### Network Security
- **Ingress:** HTTPS only (TLS 1.3)
- **Internal:** Service-to-service via private network
- **Egress:** Whitelist external APIs (no open outbound)
- **Firewall:** Cloud provider security group rules

### Container Orchestration (Future K8s)
```yaml
securityContext:
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  runAsNonRoot: true
  runAsUser: 1000
  capabilities:
    drop: ['ALL']
```

---

## LLM Agent Security (Codex CLI)

### Boundaries
- **Read-Only files:** \`src/utils/security/\`, \`docs/SECURITY.md\`
- **No secrets:** Agent cannot access \`.env\`, GitHub Actions secrets
- **Sandboxed execution:** Terminal commands run in controlled shell
- **MCP validation:** All MCPs logged + audited

### Safe Prompting
- Never include hardcoded secrets in prompts
- Always reference files + line numbers (no copy-paste)
- Use MCP tools (filesystem, git, github, shell)
- Validate output before commit

### Incident Response
1. **Loop detected:** Agent aborts, files issue with \`bug\` label
2. **Secret leaked:** Pre-push hook blocks + alerts \`security@zappro.site\`
3. **Test failed >5x:** Agent escalates to manual review
4. **Unusual commit:** Requires code review before merge

---

## Compliance Checklist

### OWASP Top 10
- [ ] **A01:2021 – Broken Access Control:** RBAC enforced, JWT validated
- [ ] **A02:2021 – Cryptographic Failures:** TLS 1.3, PostgreSQL encryption at rest
- [ ] **A03:2021 – Injection:** SQLAlchemy ORM parameterized queries
- [ ] **A04:2021 – Insecure Design:** Security by design reviews in DECISION.md
- [ ] **A05:2021 – Security Misconfiguration:** Docker hardened, minimal base image
- [ ] **A06:2021 – Vulnerable & Outdated Components:** Weekly dependency audit
- [ ] **A07:2021 – Authentication Failures:** MFA ready (GitHub auth), JWT rotation
- [ ] **A08:2021 – Software & Data Integrity Failures:** Git signed commits, PR reviews
- [ ] **A09:2021 – Logging & Monitoring:** Audit logs, Slack alerts on prod deploy
- [ ] **A10:2021 – SSRF:** API whitelists external endpoints

### LGPD (Brazilian Data Protection)
- [ ] **Art. 5:** Purpose, necessity, transparency documented
- [ ] **Art. 6:** Legal bases (consent, contract, obligation) recorded
- [ ] **Art. 11:** Sensitive data not collected without explicit consent
- [ ] **Art. 18:** Data export available via API
- [ ] **Art. 41:** Account deletion removes all PII (30-day grace)

### SOC 2 Type II (Future)
- [ ] Access control: RBAC, MFA, audit logs
- [ ] Change management: PR review, CI/CD approval gates
- [ ] Availability: 99.9% uptime SLA, auto-failover
- [ ] Confidentiality: Encryption at rest + transit

---

## Security Incident Response

### Severity Levels
| Level | Response | Action |
|-------|----------|--------|
| **Critical** | Immediate | Hotfix, production patch, customer notification |
| **High** | 24 hours | Patch released, CVE mitigated |
| **Medium** | 1 week | Scheduled maintenance, testing |
| **Low** | 30 days | Backlog, next release cycle |

### Escalation Path
1. Report → security@zappro.site
2. Triage → Security team reviews
3. Patch → Dev team creates fix
4. Test → QA validates (all tests pass + security scan)
5. Release → Deploy to production
6. Notify → Public advisory + customer email

---

## Security Best Practices

### For Developers
- **Never hardcode secrets:** Use environment variables
- **Validate input:** Always sanitize user input
- **Use HTTPS:** All external connections must use TLS
- **Rotate credentials:** Change passwords every 90 days
- **Review code:** 2-reviewer approval on all PRs

### For Operators
- **Monitor logs:** Daily review of audit logs for anomalies
- **Update software:** Apply security patches within 48h of release
- **Backup data:** Test restores weekly
- **Rotate keys:** SSL certificates before expiration (auto-renew)

### For Users
- **Enable MFA:** GitHub + email verification
- **Strong passwords:** Minimum 12 characters + complexity
- **Report issues:** Use responsible disclosure process
- **Update app:** Upgrade to latest version (auto-update in production)

---

## Security Roadmap

### Q4 2025
- [ ] Implement WAF (Web Application Firewall) rules
- [ ] Add Security headers scanning (CSP, X-Frame-Options, etc.)
- [ ] Setup SIEM (Security Information & Event Management)

### Q1 2026
- [ ] SOC 2 Type II certification audit
- [ ] Penetration testing by external firm
- [ ] Security awareness training for team

### Q2 2026
- [ ] Zero-trust network architecture
- [ ] Hardware security key support (FIDO2)
- [ ] Quantum-resistant cryptography readiness

---

## Contact & Support
- **Security questions:** security@zappro.site
- **Slack:** #security-zappro
- **Issue tracker:** GitHub with label \`security\`
