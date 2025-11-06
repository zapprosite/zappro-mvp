## ZapPro Frontend

Frontend Next.js 15 (App Router) com Tailwind v4, shadcn/ui, Zustand e TanStack Query.

### Instalação
```bash
npm install
```

### Desenvolvimento
```bash
npm run dev     # http://localhost:3000
```

### Lint e build
```bash
npm run lint    # eslint / next lint
npm run typecheck
npm run build   # next build --turbopack
npm run start   # modo produção
npm run test:e2e  # Playwright security smoke (usa /health)
```

### Health
`GET /health` responde `{"status":"ok","version":"0.1.0"}` para sinalizar disponibilidade ao orquestrador.

### Integração
- `NEXT_PUBLIC_API_BASE_URL` aponta para o backend FastAPI (ver `.env.example`).
- Providers globais ficam em `src/app/providers.tsx` com TanStack Query.
- Cabeçalhos de segurança configurados em `next.config.ts` (CSP, X-Frame-Options, X-Content-Type-Options, Permissions-Policy) e validados via Playwright.
