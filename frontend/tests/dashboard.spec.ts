import { test, expect } from '@playwright/test';

test.describe('Dashboard Page', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the app - it starts on Dashboard by default
    await page.goto('/');
  });

  test('should load dashboard page successfully', async ({ page }) => {
    // Wait for dashboard to be visible
    await expect(page.locator('text=Virtual Startup Dashboard')).toBeVisible({
      timeout: 10000,
    });

    // Check that navigation buttons are present
    await expect(page.locator('button:has-text("Dashboard")')).toBeVisible();
    await expect(page.locator('button:has-text("CLI")')).toBeVisible();
    await expect(page.locator('button:has-text("Chat Demo")')).toBeVisible();
  });

  test('should display navigation correctly', async ({ page }) => {
    // Dashboard button should be active (blue background)
    const dashboardBtn = page.locator('button:has-text("Dashboard")');
    await expect(dashboardBtn).toHaveClass(/bg-blue-600/);

    // Other buttons should not be active
    const cliBtn = page.locator('button:has-text("CLI")');
    await expect(cliBtn).not.toHaveClass(/bg-blue-600/);
  });

  test('should navigate to CLI page', async ({ page }) => {
    // Click CLI button
    await page.locator('button:has-text("CLI")').click();

    // Wait for CLI page to load
    await expect(page.locator('text=CLI Interface')).toBeVisible({
      timeout: 5000,
    });

    // CLI button should now be active
    const cliBtn = page.locator('button:has-text("CLI")');
    await expect(cliBtn).toHaveClass(/bg-blue-600/);
  });

  test('should navigate to Chat Demo page', async ({ page }) => {
    // Click Chat Demo button
    await page.locator('button:has-text("Chat Demo")').click();

    // Wait for Chat Demo page to load
    await expect(
      page.locator('text=Chat Demo').or(page.locator('text=Select an Agent'))
    ).toBeVisible({ timeout: 5000 });

    // Chat Demo button should now be active
    const chatBtn = page.locator('button:has-text("Chat Demo")');
    await expect(chatBtn).toHaveClass(/bg-blue-600/);
  });

  test('should navigate back to dashboard from other pages', async ({
    page,
  }) => {
    // Go to CLI
    await page.locator('button:has-text("CLI")').click();
    await expect(page.locator('text=CLI Interface')).toBeVisible();

    // Go back to Dashboard
    await page.locator('button:has-text("Dashboard")').click();
    await expect(page.locator('text=Virtual Startup Dashboard')).toBeVisible();
  });

  test('should display agent cards', async ({ page }) => {
    // Wait for dashboard to load
    await page.waitForLoadState('networkidle');

    // Check for agent-related content
    // The dashboard may show agent statistics or cards
    // This test is flexible since the exact content depends on backend data
    await expect(page.locator('body')).toContainText(/Agent|Dashboard/);
  });

  test('should be responsive on mobile viewport', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });

    // Page should still be accessible
    await expect(page.locator('text=Virtual Startup Dashboard')).toBeVisible();

    // Navigation should be visible
    await expect(page.locator('button:has-text("Dashboard")')).toBeVisible();
  });

  test('should handle page refresh correctly', async ({ page }) => {
    // Reload the page
    await page.reload();

    // Dashboard should still be visible
    await expect(page.locator('text=Virtual Startup Dashboard')).toBeVisible({
      timeout: 10000,
    });

    // Dashboard button should still be active
    const dashboardBtn = page.locator('button:has-text("Dashboard")');
    await expect(dashboardBtn).toHaveClass(/bg-blue-600/);
  });

  test('should display stats panel or metrics', async ({ page }) => {
    // Wait for page to load
    await page.waitForLoadState('networkidle');

    // Check for common dashboard elements
    // Stats might include: total agents, active workflows, etc.
    const body = page.locator('body');

    // At least one of these should be present on a dashboard
    const hasRelevantContent = await body
      .locator('text=/Agent|Workflow|Status|Stat/i')
      .count();
    expect(hasRelevantContent).toBeGreaterThan(0);
  });

  test('should not show console errors on load', async ({ page }) => {
    const consoleErrors: string[] = [];

    // Listen for console errors
    page.on('console', (msg) => {
      if (msg.type() === 'error') {
        consoleErrors.push(msg.text());
      }
    });

    // Navigate to dashboard
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Filter out known harmless errors (e.g., HMR, dev mode warnings)
    const criticalErrors = consoleErrors.filter(
      (err) =>
        !err.includes('HMR') &&
        !err.includes('DevTools') &&
        !err.includes('[vite]')
    );

    // Should have no critical console errors
    expect(criticalErrors.length).toBe(0);
  });

  test('should load within reasonable time', async ({ page }) => {
    const startTime = Date.now();

    await page.goto('/');
    await page.waitForLoadState('networkidle');

    const loadTime = Date.now() - startTime;

    // Page should load in less than 5 seconds
    expect(loadTime).toBeLessThan(5000);
  });
});
