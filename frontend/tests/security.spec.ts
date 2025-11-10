import { expect, test } from "@playwright/test";

const expectedHeaders = [
  "x-content-type-options",
  "x-frame-options",
  "x-xss-protection",
  "cache-control",
  "content-security-policy",
  "referrer-policy",
  "permissions-policy",
  "x-api-version",
  "x-request-id",
];

const assertSecurityHeaders = (headers: Record<string, string>) => {
  for (const name of expectedHeaders) {
    expect(headers[name], `esperava cabeçalho ${name}`).toBeTruthy();
  }
};

const normalizeHeaders = (responseHeaders: Record<string, string>) =>
  Object.fromEntries(
    Object.entries(responseHeaders).map(([key, value]) => [key.toLowerCase(), value])
  );

const baseUrl = process.env.PLAYWRIGHT_BASE_URL ?? "http://127.0.0.1:8000";

test.describe("Security headers", () => {
  test("/healthz inclui cabeçalhos de segurança", async ({ request }) => {
    const response = await request.get(`${baseUrl}/healthz`);
    expect(response.status()).toBe(200);
    assertSecurityHeaders(normalizeHeaders(response.headers()));
  });

  test("resposta de erro também retorna cabeçalhos", async ({ request }) => {
    const response = await request.get(`${baseUrl}/api/v1/projects/999999`, {
      accept: "application/json",
    });
    expect(response.status()).toBeGreaterThanOrEqual(400);
    assertSecurityHeaders(normalizeHeaders(response.headers()));
  });
});
