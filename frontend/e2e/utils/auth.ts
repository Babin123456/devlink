import { type Page, expect } from "@playwright/test";

/**
 * Logs an already-registered user in through the /auth screen and waits
 * for the redirect to the dashboard. Used by specs that need an
 * authenticated session (project creation, applications, messaging).
 */
export async function login(page: Page, email: string, password: string) {
  await page.goto("/auth");

  await page.getByLabel("Email").fill(email);
  await page.getByLabel("Password").fill(password);
  await page.getByRole("button", { name: "Sign In" }).click();

  await expect(page).toHaveURL(/\/dashboard/);
}
