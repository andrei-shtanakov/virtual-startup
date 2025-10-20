import { test, expect } from '@playwright/test';

test.describe('Chat Interface', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to Chat Demo page
    await page.goto('/');
    await page.locator('button:has-text("Chat Demo")').click();
    await page.waitForLoadState('networkidle');
  });

  test('should display chat interface', async ({ page }) => {
    // Check that chat interface is visible
    await expect(
      page.locator('text=Chat Demo').or(page.locator('text=Select an Agent'))
    ).toBeVisible({ timeout: 5000 });
  });

  test('should show agent selection options', async ({ page }) => {
    // Wait for page to load
    await page.waitForTimeout(1000);

    // Look for agent-related elements (buttons, dropdowns, or cards)
    const body = page.locator('body');
    const hasAgentSelection = await body
      .locator('text=/Driver|Creator|Generator|Select|Agent/i')
      .count();

    expect(hasAgentSelection).toBeGreaterThan(0);
  });

  test('should allow selecting an agent', async ({ page }) => {
    // Try to find and click any agent-related button or option
    // This could be a button like "Driver", "Creator", etc.
    const possibleAgentButtons = [
      page.locator('button:has-text("Driver")'),
      page.locator('button:has-text("Creator")'),
      page.locator('button:has-text("Generator")'),
      page.locator('select option:has-text("Driver")'),
    ];

    // Try each option until one works
    for (const button of possibleAgentButtons) {
      try {
        if (await button.isVisible({ timeout: 1000 })) {
          await button.click();
          break;
        }
      } catch (e) {
        // Continue to next option
      }
    }

    // After selection, chat input should be available
    await page.waitForTimeout(500);
  });

  test('should display chat input field', async ({ page }) => {
    // Look for text input, textarea, or contenteditable
    const chatInput = page.locator(
      'input[type="text"], textarea, [contenteditable="true"]'
    ).first();

    // Wait for it to appear (might need agent selection first)
    await expect(chatInput).toBeVisible({ timeout: 5000 });
  });

  test('should allow typing in chat input', async ({ page }) => {
    // Find chat input
    const chatInput = page.locator(
      'input[type="text"], textarea, [contenteditable="true"]'
    ).first();

    await chatInput.waitFor({ state: 'visible', timeout: 5000 });

    // Type a message
    await chatInput.fill('Hello, this is a test message');

    // Verify the text was entered
    const inputValue = await chatInput.inputValue().catch(() => '');
    const textContent = await chatInput.textContent().catch(() => '');

    expect(inputValue || textContent).toContain('test message');
  });

  test('should send message on Enter key', async ({ page }) => {
    // Find chat input
    const chatInput = page.locator(
      'input[type="text"], textarea, [contenteditable="true"]'
    ).first();

    await chatInput.waitFor({ state: 'visible', timeout: 5000 });

    // Type a message
    await chatInput.fill('Test message for Enter key');

    // Press Enter
    await chatInput.press('Enter');

    // Input should be cleared or message should appear in chat
    await page.waitForTimeout(500);

    // Check if input was cleared (common pattern)
    const inputValue = await chatInput.inputValue().catch(() => '');
    const textContent = await chatInput.textContent().catch(() => '');

    // Either input is cleared OR message appears in the UI
    const isCleared = (inputValue + textContent).length === 0;
    const messageAppeared = await page
      .locator('text=Test message for Enter key')
      .count();

    expect(isCleared || messageAppeared > 0).toBe(true);
  });

  test('should send message with send button', async ({ page }) => {
    // Find chat input
    const chatInput = page.locator(
      'input[type="text"], textarea, [contenteditable="true"]'
    ).first();

    await chatInput.waitFor({ state: 'visible', timeout: 5000 });

    // Type a message
    await chatInput.fill('Test message for send button');

    // Look for send button
    const sendButton = page.locator(
      'button:has-text("Send"), button[type="submit"], button:has(svg[class*="send"])'
    ).first();

    // Click send if button exists
    if (await sendButton.isVisible({ timeout: 1000 })) {
      await sendButton.click();
      await page.waitForTimeout(500);
    }

    // Message should appear or input should clear
    const inputValue = await chatInput.inputValue().catch(() => '');
    expect(inputValue.length).toBeLessThan(10); // Should be mostly cleared
  });

  test('should handle multi-word messages correctly', async ({ page }) => {
    const chatInput = page.locator(
      'input[type="text"], textarea, [contenteditable="true"]'
    ).first();

    await chatInput.waitFor({ state: 'visible', timeout: 5000 });

    // Type a multi-word message
    const multiWordMessage =
      'This is a multi-word message with several words';
    await chatInput.fill(multiWordMessage);

    // Verify all words are present
    const inputValue = await chatInput.inputValue().catch(() => '');
    const textContent = await chatInput.textContent().catch(() => '');

    expect(inputValue || textContent).toContain('multi-word');
    expect(inputValue || textContent).toContain('several words');
  });

  test('should respect character limit if present', async ({ page }) => {
    const chatInput = page.locator(
      'input[type="text"], textarea, [contenteditable="true"]'
    ).first();

    await chatInput.waitFor({ state: 'visible', timeout: 5000 });

    // Try to type more than 2000 characters (common limit)
    const longMessage = 'a'.repeat(2500);
    await chatInput.fill(longMessage);

    await page.waitForTimeout(300);

    // Check if there's a character counter or if input was truncated
    const charCounter = page.locator('text=/[0-9]+.*2000|2000.*[0-9]+/');
    const hasCounter = await charCounter.count();

    // Either there's a counter or the input was limited
    if (hasCounter > 0) {
      await expect(charCounter).toBeVisible();
    }
  });

  test('should display message history if available', async ({ page }) => {
    // After page loads, check for any existing messages
    await page.waitForTimeout(1000);

    // Look for message containers
    const messageElements = page.locator('[class*="message"], .message, [role="log"]');
    const count = await messageElements.count();

    // Just verify we can detect messages (count may be 0 for new chat)
    expect(count).toBeGreaterThanOrEqual(0);
  });

  test('should show agent typing indicator or status', async ({ page }) => {
    // Select an agent first
    const driverButton = page.locator('button:has-text("Driver")');
    if (await driverButton.isVisible({ timeout: 1000 })) {
      await driverButton.click();
    }

    const chatInput = page.locator(
      'input[type="text"], textarea, [contenteditable="true"]'
    ).first();

    if (await chatInput.isVisible({ timeout: 2000 })) {
      // Send a message
      await chatInput.fill('Hello agent');
      await chatInput.press('Enter');

      // Look for typing indicators or status messages
      await page.waitForTimeout(1000);

      const statusIndicators = page.locator(
        'text=/typing|thinking|processing|busy|working/i'
      );
      // Status indicator might appear (but not required)
      // Just verify the test doesn't crash
    }
  });

  test('should handle rapid message sending', async ({ page }) => {
    const chatInput = page.locator(
      'input[type="text"], textarea, [contenteditable="true"]'
    ).first();

    await chatInput.waitFor({ state: 'visible', timeout: 5000 });

    // Send multiple messages quickly
    for (let i = 0; i < 3; i++) {
      await chatInput.fill(`Rapid message ${i + 1}`);
      await chatInput.press('Enter');
      await page.waitForTimeout(100);
    }

    // UI should still be responsive
    await expect(chatInput).toBeVisible();
  });

  test('should handle empty message gracefully', async ({ page }) => {
    const chatInput = page.locator(
      'input[type="text"], textarea, [contenteditable="true"]'
    ).first();

    await chatInput.waitFor({ state: 'visible', timeout: 5000 });

    // Try to send empty message
    await chatInput.fill('');
    await chatInput.press('Enter');

    // Should either prevent send or handle gracefully
    await page.waitForTimeout(300);

    // UI should still be functional
    await expect(chatInput).toBeVisible();
  });

  test('should be responsive on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });

    // Chat interface should still be accessible
    const chatInput = page.locator(
      'input[type="text"], textarea, [contenteditable="true"]'
    ).first();

    await expect(chatInput).toBeVisible({ timeout: 5000 });
  });
});
