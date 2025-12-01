import { expect, test } from "@playwright/test";

const baseUrl = process.env.PLAYWRIGHT_BASE_URL ?? "http://127.0.0.1:8000";

test.describe("Smoke", () => {
  test("home shows projects heading", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByTestId("projects-heading")).toBeVisible();
  });

  test("backend healthz responds ok", async ({ request }) => {
    const response = await request.get(`${baseUrl}/healthz`);
    expect(response.status()).toBe(200);
    const payload = await response.json();
    expect(payload).toEqual({ status: "ok" });
  });
});
