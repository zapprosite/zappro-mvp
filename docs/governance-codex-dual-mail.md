[# Governance — Codex CLI Dual Email Account System

**Versão:** 1.0.0  
**Data:** 2025-11-06  
**Autor:** Will.zappro (williamrodriguesrefrimix@gmail.com)  
**Status:** Active  
**Aplicável:** ZapPro MVP — Desenvolvimento com Codex CLI

---

## 1. Visão Geral

Sistema de gerenciamento de **dois emails independentes** para Codex CLI, permitindo rotação automática entre contas quando um email atinge o limite de tasks (~150/5h por conta).

### Contexto de Negócio
- **Custo:** $60/mês (2×$30 ChatGPT Business)
- **Economia:** 70% vs ChatGPT Pro ($200/mês), 90% vs API tokens
- **Throughput:** ~300 tasks/5h combinados (pools isolados)
- **Estratégia:** Dual account como hedge contra rate limiting durante sprints intensivos

---

## 2. Arquitetura Técnica

### 2.1 Componentes
| Componente | Localização | Responsabilidade |
|-----------|-----------|------------------|
| **Estado JSON** | `~/.zappro/dual-account-state.json` | Rastreamento de quota, bloqueios, timestamps |
| **Script Shell** | `~/.zappro/codex-dual-account.sh` | Lógica de seleção, alternância, incremento |
| **Bashrc Hooks** | `~/.bashrc` | Aliases `cx` e `cxs`, sourcing automático |
| **Sessions Codex** | `~/.codex/sessions/*.json` | Auth tokens salvos para auto-switch |

### 2.2 Fluxo de Autenticação
cx "prompt"
↓
select_best_email()
├─ Verifica bloqueios (is_blocked)
├─ Alterna entre e-mails se um estiver bloqueado
└─ Escolhe email com menor uso diário
↓
switch_to_email()
└─ Copia session .json → ~/.codex/auth.json
↓
codex executa com email ativo
├─ Sucesso → incrementa contador
└─ Limite → bloqueia por 5h, tenta outro email
text

---

## 3. Emails Configurados

| Email | Plano | Pool Local | Pool Cloud | Status |
|-------|-------|-----------|-----------|--------|
| `williamrodriguesrefrimix@gmail.com` | Business $30/mês | ~150/5h | ~20-40/5h | Ativo |
| `contato@calirodrigues.com` | Business $30/mês | ~150/5h | ~20-40/5h | Ativo |
| **TOTAL** | **$60/mês** | **~300/5h** | **~40-80/5h** | **Isolado** |

---

## 4. Uso Diário

### 4.1 Comando Principal

Sintaxe correta (obrigatório usar -- antes do prompt)
cx -- "Sua tarefa aqui"
Exemplos
cx -- "Adicionar campo status ao Task model"
cx -- "Implementar paginação GET /tasks"
cx -- "Refatorar frontend componentes"
text

### 4.2 Ver Status Anytime

cxs
Output:
═══════════════════════════════════════
ZapPro Dual Account Status
═══════════════════════════════════════
Email 1 (williamrodriguesrefrimix@gmail.com):
Status: ✅ Disponível
Tasks hoje: 87
Email 2 (contato@calirodrigues.com):
Status: ✅ Disponível
Tasks hoje: 43
Total tasks hoje: 130
text

### 4.3 Comportamento Automático
- **Email 1 atinge ~150 tasks** → Marcado como �� BLOQUEADO por 5h
- **Próximo `cx ...` comando** → Sistema alterna para Email 2 automaticamente
- **Ambos bloqueados** → Exibe erro com próximo desbloqueio

---

## 5. Limites e Resets

### 5.1 Rate Limiting
- **Local tasks:** ~150/email/5h (pool independente)
- **Cloud tasks:** ~20-40/email/5h (pool independente)
- **Reset:** Automático 5 horas após bloqueio, ou 24h reset completo

### 5.2 Monitoramento

Verificar contadores atuais
cat ~/.zappro/dual-account-state.json | jq '.email1_tasks_today, .email2_tasks_today'
Zerar para novo dia (manual)
jq '.email1_tasks_today=0 | .email2_tasks_today=0' ~/.zappro/dual-account-state.json > ~/.zappro/dual-account-state.json.tmp
mv ~/.zappro/dual-account-state.json.tmp ~/.zappro/dual-account-state.json
text

---

## 6. Operações de Manutenção

### 6.1 Revalidar Sessions
Caso o sistema relate "Session não encontrada", revalidar ambas contas:

mkdir -p ~/.codex/sessions
codex logout
codex login # Login Email 1
cp ~/.codex/auth.json ~/.codex/sessions/williamrodriguesrefrimix@gmail.com.json
codex logout
codex login # Login Email 2
cp ~/.codex/auth.json ~/.codex/sessions/contato@calirodrigues.com.json
ls -lh ~/.codex/sessions/ # Verificar ambas presentes
text

### 6.2 Testar Script Syntax

bash -n ~/.zappro/codex-dual-account.sh
text

### 6.3 Limpar Estado (Restart)

rm ~/.zappro/dual-account-state.json ~/.codex/sessions/*.json
Recriar inicial com Passo 1 dos docs
text

---

## 7. Troubleshooting

| Problema | Sintoma | Solução |
|----------|---------|---------|
| **"jq: command not found"** | Status falha | `sudo apt install -y jq` |
| **"Session não encontrada"** | Não alterna emails | Revalidar sessions (§6.1) |
| **"cxs: command not found"** | Alias não carrega | `source ~/.bashrc` em shell interativo |
| **Ambos emails bloqueados** | "⛔ Ambos bloqueados" | Aguardar 5h ou manualmente desbloquear JSON |
| **Contador não incrementa** | Sempre mostra 0 tasks | Verificar permissões: `chmod 644 ~/.zappro/dual-account-state.json` |

---

## 8. Escalação e Upgrades

### Se ~300 tasks/5h Não for Suficiente
**Opção 1:** Esperar reset 5h (pool regenera)  
**Opção 2:** Upgrade para ChatGPT Enterprise ($120-150/mês, 2+ usuários)  
**Opção 3:** API pay-as-you-go como fallback (~$0.05-0.50/task)

### Integração com Trae IDE
- Codex CLI roda no WSL Ubuntu 24.04
- Trae IDE (Windows) gerencia projetos com `.trae/mcp.json`
- Ambos acessam `~/.zappro` e `~/.codex/` normalmente

---

## 9. Checklist de Conformidade

- [ ] Ambas sessions salvas em `~/.codex/sessions/`
- [ ] Script `~/.zappro/codex-dual-account.sh` com syntax OK
- [ ] Aliases `cx` e `cxs` carregam em shell interativo
- [ ] `cxs` mostra ambos emails com status ✅
- [ ] `cx -- "prompt"` executa sem erro "unrecognized subcommand"
- [ ] JSON `.jq` queries não geram "jq: command not found"
- [ ] Contadores incrementam após cada task
- [ ] Documentação atualizada no repositório

---

## 10. SLA e Suporte

| Métrica | Alvo | Critério |
|---------|------|----------|
| **Disponibilidade** | 99% | Ambos emails sempre disponíveis exceto durante bloqueio 5h |
| **Latência** | < 3s | `cx` comando executado em < 3s com output |
| **Recovery** | < 5h | Auto-desbloqueio, retry com outro email |
| **Escalabilidade** | ~300 tasks/5h | Limite natural dos 2 pools; upgrade se consistente |

---

## 11. Histórico de Revisão

| Data | Versão | Mudanças | Autor |
|------|--------|----------|-------|
| 2025-11-06 | 1.0.0 | Inicial — Dual account governance | Will.zappro |

---

## 12. Contato e Escalação

- **Responsável:** Will.zappro (williamrodriguesrefrimix@gmail.com)
- **Repositório:** `git@github.com:zapprosite/zappro-mvp.git`
- **Docs:** `/docs/governance-codex-dual-mail.md`
- **Issues:** GitHub Issues com label `codex-governance`

---

## Apêndice A: Referência de Comandos


Uso básico
cx -- "tarefa" # Executar task
cxs # Ver status
Manutenção
source ~/.bashrc # Recarregar aliases
bash -n ~/.zappro/codex-dual-account.sh # Validar script
rm ~/.zappro/dual-account-state.json # Reset estado (avançado)
Debug
cat ~/.zappro/dual-account-state.json | jq .
ls -lh ~/.codex/sessions/
codex whoami]
