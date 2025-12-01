import type { PlaywrightTestConfig } from "@playwright/test";

const config: PlaywrightTestConfig = {
  testDir: "./tests",
  timeout: 30_000,
  expect: {
    timeout: 5_000,
  },
  retries: process.env.CI ? 2 : 1,
  maxFailures: 1,
  forbidOnly: true,
  use: {
    baseURL: process.env.PLAYWRIGHT_BASE_URL ?? "http://127.0.0.1:3000",
  },
  reporter: [["list"], ["html", { open: "never" }]],
  webServer: [
    {
      command:
        "bash -lc 'npx kill-port 8000 >/dev/null 2>&1; cd .. && venv/bin/uvicorn src.main:app --host 0.0.0.0 --port 8000 --log-level info'",
      url: "http://127.0.0.1:8000/healthz",
      reuseExistingServer: true,
      timeout: 180_000,
    },
    {
      command:
        "bash -lc 'npx kill-port 3000 >/dev/null 2>&1; (npm run build || true) && npm run start -- -H 0.0.0.0 -p 3000'",
      url: "http://127.0.0.1:3000",
      reuseExistingServer: true,
      timeout: 180_000,
    },
  ],
};

export default config;
