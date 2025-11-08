# WORKFLOW.md - Git Workflow & PR Process

---

## Branching Strategy

## At a Glance

```text
Branch → Commit → Push → PR → CI (lint, tests, security) → Review (2+) → Merge (squash) → Deploy
```

### Branch Naming
```text
feature/nome-feature              # New features
bugfix/nome-bug                   # Bug fixes
refactor/nome-refactor            # Refactoring
ci/nome-improvement               # CI/CD improvements
docs/nome-documentacao            # Documentation
hotfix/nome-urgente               # Production hotfixes (from main)
```

### Example
```bash
git checkout -b feature/auth-login-oauth
git checkout -b bugfix/task-filter-date-range
git checkout -b ci/matrix-builds-python-node
```

---

## Commit Message Format

### Conventional Commits
```text
<type>(<scope>): <subject>

<body>

<footer>
```

### Examples
```text
feat(auth): add OAuth2 login support

- Integrated Google OAuth2 provider
- Added user migration from email to OAuth
- Updated login page UI

Closes #123

---

fix(tasks): fix date range filter boundary

Was comparing dates without timezone offset.
Fixed by normalizing to UTC before comparison.

---

docs(cicd): add matrix builds documentation

---

ci(workflows): implement codecov integration

Added codecov.yml with 80% coverage threshold.
Configured GitHub Actions secret CODECOV_TOKEN.

---

refactor(models): convert sync SQLAlchemy to async

Breaking: Async session management required
- Updated all DB queries to use select() + await
- Migration: Update all controller signatures

---

chore(deps): bump fastapi from 0.104 to 0.110
```

### Type & Scope
| Type | Scope Examples | When |
|------|---|---|
| feat | auth, tasks, projects | New feature |
| fix | security, validation, database | Bug fix |
| docs | readme, security, guides | Documentation |
| ci | workflows, matrix, secrets | CI/CD changes |
| refactor | async, db-layer, imports | Code restructuring |
| chore | deps, version bump | Maintenance |
| perf | cache, query optimization | Performance |

---

## Pull Request Process

### 1. Create Feature Branch
```bash
git checkout main
git pull origin main
git checkout -b feature/my-feature
```

### 2. Make Changes & Commit
```bash
# Make changes
git add .
git commit -m "feat(scope): description"

# Validate locally
make lint
make test
bash scripts/validate.sh
```

### 3. Push & Open PR
```bash
git push origin feature/my-feature
```

Then open PR on GitHub with template (auto-filled):

```markdown
## Description
Closes #123

Brief description of changes.

## Changes Made
- [ ] Feature A
- [ ] Feature B

## Testing
- [ ] Unit tests added
- [ ] Manual testing on localhost
- [ ] Verified preview URL

## Checklist
- [ ] make lint passes
- [ ] make test passes
- [ ] docs updated
- [ ] No secrets in code
```

### 4. CI/CD Validation
Automatic checks run:
- ✅ Lint (Ruff + Black + isort)
- ✅ Tests (pytest, coverage ≥80%)
- ✅ Security (Bandit, npm audit, secret scan)
- ✅ Deploy preview to \`https://preview-{PR-number}.zappro.site\`

### 5. Code Review
- Minimum 2 reviewers for main branch
- Specific paths:
  - Backend (\`src/\`): @willrefrimix
  - Frontend (\`frontend/\`): @jpmarcenaria
  - DevOps (\`.github/\`, \`scripts/\`): @willrefrimix

### 6. Merge
```bash
# Via GitHub UI (Squash + Merge)
# or CLI:
gh pr merge {PR_NUMBER} --squash --delete-branch
```

### 7. Automatic Deployment
After merge to main:
- Production deployment starts
- Slack notification: \`✅ Deployed production release {COMMIT_SHA}\`
- Monitor logs: \`docker compose logs -f\`

---

## Conflict Resolution

### If merge conflict occurs:
```bash
# Pull latest main
git fetch origin main

# Rebase your branch on main
git rebase origin/main

# Resolve conflicts in editor
git add .
git rebase --continue

# Force push (safe because nobody else should use this branch)
git push origin feature/my-feature --force
```

---

## Release Process

### Version Numbering (Semantic Versioning)
```text
MAJOR.MINOR.PATCH
1.2.3
↑ Breaking changes
  ↑ New features
    ↑ Bug fixes
```

### Release Steps
```bash
# From main branch
git checkout main
git pull origin main

# Tag release
git tag -a v1.2.3 -m "Release v1.2.3: description"
git push origin v1.2.3

# GitHub auto-creates Release from tag
# CD workflow deploys to production
```

---

## Development Best Practices

### Keep PR Small
- Max 300 lines per PR (smaller = faster review)
- One feature = one PR
- If too big → break into sub-PRs

### Always Pull Before Push
```bash
git fetch origin
git rebase origin/main  # or merge if you prefer
git push origin feature/my-feature
```

### Sync with Main Frequently
```bash
# While working on feature branch
git fetch origin main
git rebase origin/main  # Keep up-to-date
```

### Don't Commit Secrets
```bash
# Before committing
git diff --cached | grep -i "secret\|token\|password"

# If found, remove:
git reset HEAD filename
# Edit to remove secrets
git add filename
git commit
```

### Review Your Own PR First
- Click "Files changed" on your PR
- Verify no unintended changes
- Check diffs carefully

---

## Common Workflows

### Scenario 1: Update from Main
```bash
git fetch origin main
git rebase origin/main
# Resolve conflicts if any
git push origin feature/my-feature
```

### Scenario 2: Update Local Main
```bash
git checkout main
git pull origin main
```

### Scenario 3: Discard Local Changes
```bash
git checkout -- filename   # Single file
git reset --hard HEAD      # All changes (⚠️ danger)
```

### Scenario 4: Stash Work (Temporary)
```bash
git stash                  # Save changes
git checkout another-branch
# ... do work ...
git checkout feature/my-feature
git stash pop              # Restore changes
```

---

## CI/CD Integration

### What Runs on Each Push
1. **On feature/* push:**
   - Lint, test, security scan
   - Preview deploy (if PR exists)

2. **On main push (after merge):**
   - Full CI suite
   - Production deploy
   - Slack notification

3. **On PR approval:**
   - Staging preview (optional)
   - Approval notification to Slack

---

## Emergency Procedures

### Hotfix for Production Issue
```bash
# From main (production)
git checkout main
git pull origin main
git checkout -b hotfix/critical-bug

# Make fix
git commit -m "fix(critical): description"

# Fast-track to main
git push origin hotfix/critical-bug
# Open PR with label "hotfix" (skip reviewers if emergency)
gh pr create --title "hotfix: ..." --body "EMERGENCY" --draft false

# After merge to main
# Production deploys automatically
```

### Rollback Production
```bash
# If latest deploy breaks
git revert HEAD
# Creates new commit that undoes changes
# CD automatically deploys revert
```

---

## Troubleshooting

- CI falhou em lint: rode `make lint` local e corrija formatação.
- Testes com erro: reproduza local com `make test`.
- Segredos detectados: use `bash scripts/secret-scan.sh` antes de commitar.

---

## FAQ

**Q: Posso commitar direto em main?**
A: Não! main é protegido. Sempre use branch + PR.

**Q: Meu rebase foi longe demais, como volto?**
A: \`git reflog\` + \`git reset --hard <ref>\`

**Q: Quantos reviewers preciso?**
A: Mínimo 2 (auto-requested baseado na path)

**Q: E se o CI falhar?**
A: Fixe localmente, commit, push novamente. CI roda automaticamente.

---

## Contact
- Questions: GitHub discussions
- Slack: #dev-workflow
