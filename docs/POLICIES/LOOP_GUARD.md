# Loop Guard Policy

> [!WARNING]
> Se um agente repetir a mesma ação/comando 3+ vezes sem progresso, interrompa e escale.

## Indicadores de Loop
- Mesmos comandos executados repetidamente sem mudança de saída
- Releitura incessante dos mesmos arquivos
- Criação/remoção de arquivos em vai‑e‑vem

## Detecção
```bash
python3 scripts/loop_guard.py
```

## Ação Imediata
1. Interrompa (Ctrl+C) a sessão
2. Registre no `tutor/progress.state.md`
3. Abra issue com label `codex-blocked` (se necessário)
4. Refine prompt com caminhos/linhas exatos

## Escalação
- Notifique @willrefrimix
- Adicione logs relevantes (sem segredos)
