import fs from "node:fs";
import path from "node:path";

import { expect, test } from "@playwright/test";

const EXPECTED_HEADERS = [
  "content-security-policy",
  "x-content-type-options",
  "x-frame-options",
  "permissions-policy",
  "referrer-policy",
];

const securityLog = path.join(process.cwd(), "logs", "security.log");

function logHeaderIssue(url: string, headers: Record<string, string | undefined>) {
  fs.mkdirSync(path.dirname(securityLog), { recursive: true });
  fs.appendFileSync(
    securityLog,
    `${new Date().toISOString()} [playwright] Missing headers for ${url}: ${JSON.stringify(
      headers
    )}\n`,
    "utf-8"
  );
}

function assertHeaders(url: string, headers: Record<string, string | undefined>) {
  const missing = EXPECTED_HEADERS.filter(
    (header) => !headers[header] || headers[header] === "undefined"
  );
  if (missing.length > 0) {
    logHeaderIssue(url, headers);
    throw new Error(`Missing security headers ${missing.join(", ")} for ${url}`);
  }
}

test.describe("Security headers", () => {
  test("health endpoint exposes security headers and JSON body", async ({ request }) => {
    const response = await request.get("/health");
    expect(response.status()).toBe(200);

    const json = await response.json();
    expect(json).toMatchObject({
      status: "ok",
      version: "0.1.0",
    });

    const headers = response.headers();
    assertHeaders("/health", headers);
    expect(headers["content-security-policy"]).toContain("default-src 'self'");
  });

  test("error responses emit headers", async ({ request }) => {
    const response = await request.get("/non-existent-route");
    expect(response.status()).toBe(404);
    assertHeaders("/non-existent-route", response.headers());
  });

  test("forced production mode blocks unsafe-inline", async ({ request }) => {
    const response = await request.get("/health", {
      headers: { "x-csp-force-prod": "true" },
    });
    expect(response.status()).toBe(200);
    const csp = response.headers()["content-security-policy"] ?? "";
    if (csp.includes("unsafe-inline")) {
      logHeaderIssue("/health?force-prod", response.headers());
      throw new Error("unsafe-inline detected in production CSP");
    }
  });
});
