import { test, expect } from "@playwright/test";
import { login } from "./utils/auth";

test("a logged-in user can send a message in an existing conversation", async ({ page }) => {
  const email = process.env.E2E_USER_EMAIL ?? "e2e-existing-user@example.com";
  const password = process.env.E2E_USER_PASSWORD ?? "Password123!";

  await login(page, email, password);

  await page.goto("/messages");

  // Open the first conversation in the list.
  await page.locator('a[href^="/messages/"]').first().click();

  const messageText = `Hello from Playwright ${Date.now()}`;
  const input = page.getByPlaceholder("Type a message…");
  await input.fill(messageText);
  await page.getByRole("button", { name: "Send" }).click();

  await expect(page.getByText(messageText)).toBeVisible();
});