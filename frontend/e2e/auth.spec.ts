import { test, expect } from "@playwright/test";
import { login } from "./utils/auth";

test.describe("Signup", () => {
  test("a new user can create an account", async ({ page }) => {
    const unique = Date.now();
    const email = `e2e-user-${unique}@example.com`;
    const password = "Password123!";

    await page.goto("/auth");

    // Switch from the default "Sign in" tab to "Sign up".
    await page.getByRole("button", { name: "Sign up" }).click();

    await page.getByLabel("First name").fill("Test");
    await page.getByLabel("Last name").fill("User");
    await page.getByLabel("Username").fill(`e2euser${unique}`);
    await page.getByLabel("Email").fill(email);
    await page.getByLabel("Password", { exact: true }).fill(password);
    await page.getByLabel("Confirm password").fill(password);

    await page.getByRole("button", { name: "Create account" }).click();

    await expect(page).toHaveURL(/\/dashboard/);
  });
});

test.describe("Login", () => {
  test("an existing user can sign in", async ({ page }) => {
    // Requires a seeded/test account. Override via env vars in CI.
    const email = process.env.E2E_USER_EMAIL ?? "e2e-existing-user@example.com";
    const password = process.env.E2E_USER_PASSWORD ?? "Password123!";

    await login(page, email, password);
  });
});
