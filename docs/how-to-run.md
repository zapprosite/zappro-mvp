# Como rodar (esqueleto)

Este projeto é um template “LLM‑safe”. O stack (linguagem/framework) será definido no PRD.md e a LLM (ou o time) deve atualizar este documento conforme a escolha.

Ao definir a stack no PRD, inclua aqui:
- Pré‑requisitos (versão da linguagem, gerenciador de pacotes, Docker, etc.)
- Comandos de setup (ex.: `npm ci`, `pip install -r requirements.txt`, `docker compose up`)
- Como rodar em desenvolvimento (reload/hot‑reload)
- Como rodar testes, lint e formatadores
- Como configurar variáveis de ambiente (e `.env.example`)
- Como executar build e/ou iniciar em produção

Dica: mantenha os comandos reunidos em `Makefile` ou `justfile` para padronizar DX.
