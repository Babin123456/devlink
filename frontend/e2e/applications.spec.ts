import { test, expect } from "@playwright/test";
import { login } from "./utils/auth";

/**
 * NOTE: In this snapshot of the codebase, `ApplyButton`
 * (frontend/src/components/applications/ApplyButton.tsx) is not yet
 * rendered from any route — it isn't wired into the project detail page
 * or the flares feed. This test targets it generically by its visible
 * "Apply" label wherever it ends up mounted. Once the component is wired
 * into a real page, update the `page.goto(...)` call below to that page.
 */
test("a logged-in user can submit an application", async ({ page }) => {
  const email = process.env.E2E_USER_EMAIL ?? "e2e-existing-user@example.com";
  const password = process.env.E2E_USER_PASSWORD ?? "Password123!";

  await login(page, email, password);

  await page.goto("/projects");
  await page.getByRole("link").first().click();

  await page.getByRole("button", { name: "Apply", exact: true }).click();

  await page
    .getByLabel("Message")
    .fill("I'd love to help build this — I have relevant experience.");

  await page.getByRole("button", { name: "Submit application" }).click();

  await expect(page.getByText("Applied successfully")).toBeVisible();
});