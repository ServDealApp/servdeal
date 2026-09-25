import { expect, test } from "@playwright/test";

test("customer can submit an at-salon booking request", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: /Salon services and great deals/i })).toBeVisible();
  await page.getByRole("button", { name: "Book now" }).first().click();
  await expect(page.getByText("BOOKING REQUEST")).toBeVisible();
  await page.getByLabel("Your name").fill("Saurabh Test");
  await page.getByLabel("Phone number").fill("9876543210");
  await page.getByLabel("Date").fill("2026-10-15");
  await page.getByRole("button", { name: "Request booking" }).click();
  await expect(page.getByText(/Booking SD-[A-Z0-9]+ requested/)).toBeVisible();
});

test("at-home booking shows the required address input", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: "Book now" }).first().click();
  await page.getByLabel("Service mode").selectOption("at_home");
  await expect(page.getByLabel("Home address")).toBeVisible();
});
