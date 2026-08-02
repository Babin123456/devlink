import { test, expect } from "@playwright/test";
import { login } from "./utils/auth";

test("a logged-in user can create a new project", async ({ page }) => {
  const email = process.env.E2E_USER_EMAIL ?? "e2e-existing-user@example.com";
  const password = process.env.E2E_USER_PASSWORD ?? "Password123!";
  const projectTitle = `E2E Project ${Date.now()}`;

  await login(page, email, password);

  await page.goto("/projects");
  await page.getByRole("button", { name: "New project" }).click();

  await page.getByLabel("Title").fill(projectTitle);
  await page.getByLabel("Description").fill("Created by an automated Playwright test.");

  await page.getByRole("button", { name: "Create project" }).click();

  await expect(page.getByText(projectTitle)).toBeVisible();
});