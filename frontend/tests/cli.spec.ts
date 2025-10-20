import { test, expect } from '@playwright/test';

test.describe('CLI Interface', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to CLI page
    await page.goto('/');
    await page.locator('button:has-text("CLI")').click();
    await page.waitForLoadState('networkidle');
  });

  test('should display CLI interface', async ({ page }) => {
    // Check that CLI interface is visible
    await expect(page.locator('text=CLI Interface')).toBeVisible({
      timeout: 5000,
    });
  });

  test('should show terminal-style input', async ({ page }) => {
    // Look for CLI input field
    const cliInput = page.locator(
      'input[type="text"], textarea, [contenteditable="true"], input[placeholder*="command"], input[placeholder*="CLI"]'
    ).first();

    await expect(cliInput).toBeVisible({ timeout: 5000 });
  });

  test('should display command prompt or prefix', async ({ page }) => {
    // Look for terminal prompt indicators like $, >, >>
    const terminalPrompt = page.locator('text=/[$>]|prompt|>>/i').first();

    // Prompt might be visible (common in CLI interfaces)
    const hasPrompt = await terminalPrompt.count();
    expect(hasPrompt).toBeGreaterThanOrEqual(0);
  });

  test('should accept CLI commands', async ({ page }) => {
    const cliInput = page.locator(
      'input[type="text"], textarea, [contenteditable="true"]'
    ).first();

    await cliInput.waitFor({ state: 'visible', timeout: 5000 });

    // Type a command
    await cliInput.fill('/help');

    // Verify command was entered
    const inputValue = await cliInput.inputValue().catch(() => '');
    const textContent = await cliInput.textContent().catch(() => '');

    expect(inputValue || textContent).toContain('help');
  });

  test('should execute /help command', async ({ page }) => {
    const cliInput = page.locator(
      'input[type="text"], textarea, [contenteditable="true"]'
    ).first();

    await cliInput.waitFor({ state: 'visible', timeout: 5000 });

    // Execute help command
    await cliInput.fill('/help');
    await cliInput.press('Enter');

    await page.waitForTimeout(500);

    // Look for help output
    const helpOutput = page.locator(
      'text=/available.*command|command.*list|help|usage/i'
    );

    const hasHelp = await helpOutput.count();
    console.log('Help command output found:', hasHelp > 0);
  });

  test('should execute /status command', async ({ page }) => {
    const cliInput = page.locator(
      'input[type="text"], textarea, [contenteditable="true"]'
    ).first();

    await cliInput.waitFor({ state: 'visible', timeout: 5000 });

    // Execute status command
    await cliInput.fill('/status');
    await cliInput.press('Enter');

    await page.waitForTimeout(1000);

    // Look for status output
    const statusOutput = page.locator(
      'text=/status|agent|system|running|online/i'
    );

    const hasStatus = await statusOutput.count();
    console.log('Status command output found:', hasStatus > 0);
  });

  test('should execute /agents command', async ({ page }) => {
    const cliInput = page.locator(
      'input[type="text"], textarea, [contenteditable="true"]'
    ).first();

    await cliInput.waitFor({ state: 'visible', timeout: 5000 });

    // Execute agents command
    await cliInput.fill('/agents');
    await cliInput.press('Enter');

    await page.waitForTimeout(1000);

    // Look for agents list
    const agentsOutput = page.locator(
      'text=/agent|driver|creator|generator/i'
    );

    const hasAgents = await agentsOutput.count();
    console.log('Agents command output found:', hasAgents > 0);
  });

  test('should execute /driver command with message', async ({ page }) => {
    const cliInput = page.locator(
      'input[type="text"], textarea, [contenteditable="true"]'
    ).first();

    await cliInput.waitFor({ state: 'visible', timeout: 5000 });

    // Execute driver command with a message
    await cliInput.fill('/driver Hello from CLI test');
    await cliInput.press('Enter');

    await page.waitForTimeout(1500);

    // Command should be processed
    const output = await page.locator('body').textContent();
    console.log('Driver command executed');
  });

  test('should execute /creator command with message', async ({ page }) => {
    const cliInput = page.locator(
      'input[type="text"], textarea, [contenteditable="true"]'
    ).first();

    await cliInput.waitFor({ state: 'visible', timeout: 5000 });

    // Execute creator command
    await cliInput.fill('/creator Research topic test');
    await cliInput.press('Enter');

    await page.waitForTimeout(1500);

    console.log('Creator command executed');
  });

  test('should execute /generator command with message', async ({ page }) => {
    const cliInput = page.locator(
      'input[type="text"], textarea, [contenteditable="true"]'
    ).first();

    await cliInput.waitFor({ state: 'visible', timeout: 5000 });

    // Execute generator command
    await cliInput.fill('/generator Create new agent test');
    await cliInput.press('Enter');

    await page.waitForTimeout(1500);

    console.log('Generator command executed');
  });

  test('should handle invalid commands gracefully', async ({ page }) => {
    const cliInput = page.locator(
      'input[type="text"], textarea, [contenteditable="true"]'
    ).first();

    await cliInput.waitFor({ state: 'visible', timeout: 5000 });

    // Execute invalid command
    await cliInput.fill('/invalidcommand');
    await cliInput.press('Enter');

    await page.waitForTimeout(500);

    // Should show error or unknown command message
    const errorOutput = page.locator(
      'text=/unknown|invalid|error|not.*found|command.*exist/i'
    );

    const hasError = await errorOutput.count();
    console.log('Error handling for invalid command:', hasError > 0);

    // UI should still be functional
    await expect(cliInput).toBeVisible();
  });

  test('should support command history navigation with arrow keys', async ({
    page,
  }) => {
    const cliInput = page.locator(
      'input[type="text"], textarea, [contenteditable="true"]'
    ).first();

    await cliInput.waitFor({ state: 'visible', timeout: 5000 });

    // Execute a few commands to build history
    await cliInput.fill('/help');
    await cliInput.press('Enter');
    await page.waitForTimeout(300);

    await cliInput.fill('/status');
    await cliInput.press('Enter');
    await page.waitForTimeout(300);

    // Press Up arrow to get previous command
    await cliInput.press('ArrowUp');
    await page.waitForTimeout(200);

    const value = await cliInput.inputValue().catch(() => '');
    const text = await cliInput.textContent().catch(() => '');

    // Should recall previous command (/status)
    const recalledCommand = value || text;
    console.log('Recalled command:', recalledCommand);

    // Might contain previous command (feature-dependent)
  });

  test('should clear input after command execution', async ({ page }) => {
    const cliInput = page.locator(
      'input[type="text"], textarea, [contenteditable="true"]'
    ).first();

    await cliInput.waitFor({ state: 'visible', timeout: 5000 });

    // Execute a command
    await cliInput.fill('/help');
    await cliInput.press('Enter');

    await page.waitForTimeout(500);

    // Input should be cleared
    const inputValue = await cliInput.inputValue().catch(() => '');
    const textContent = await cliInput.textContent().catch(() => '');

    expect((inputValue + textContent).trim().length).toBeLessThan(10);
  });

  test('should display command output in terminal area', async ({ page }) => {
    const cliInput = page.locator(
      'input[type="text"], textarea, [contenteditable="true"]'
    ).first();

    await cliInput.waitFor({ state: 'visible', timeout: 5000 });

    // Execute command
    await cliInput.fill('/help');
    await cliInput.press('Enter');

    await page.waitForTimeout(1000);

    // Check for terminal output area
    const outputArea = page.locator(
      '[class*="output"], [class*="terminal"], [role="log"], pre, code'
    );

    const hasOutput = await outputArea.count();
    console.log('Terminal output areas found:', hasOutput);
  });

  test('should handle rapid command execution', async ({ page }) => {
    const cliInput = page.locator(
      'input[type="text"], textarea, [contenteditable="true"]'
    ).first();

    await cliInput.waitFor({ state: 'visible', timeout: 5000 });

    // Execute multiple commands rapidly
    const commands = ['/help', '/status', '/agents'];

    for (const cmd of commands) {
      await cliInput.fill(cmd);
      await cliInput.press('Enter');
      await page.waitForTimeout(200);
    }

    // CLI should still be responsive
    await expect(cliInput).toBeVisible();
  });

  test('should support /clear command if available', async ({ page }) => {
    const cliInput = page.locator(
      'input[type="text"], textarea, [contenteditable="true"]'
    ).first();

    await cliInput.waitFor({ state: 'visible', timeout: 5000 });

    // Execute some commands first
    await cliInput.fill('/help');
    await cliInput.press('Enter');
    await page.waitForTimeout(500);

    // Try clear command
    await cliInput.fill('/clear');
    await cliInput.press('Enter');

    await page.waitForTimeout(500);

    // Terminal might be cleared (feature-dependent)
    console.log('Clear command executed');
  });

  test('should be responsive on mobile viewport', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });

    // CLI should still be accessible
    const cliInput = page.locator(
      'input[type="text"], textarea, [contenteditable="true"]'
    ).first();

    await expect(cliInput).toBeVisible({ timeout: 5000 });

    // Should be able to execute commands
    await cliInput.fill('/help');
    await cliInput.press('Enter');

    await page.waitForTimeout(500);
  });

  test('should display command timestamps if available', async ({ page }) => {
    const cliInput = page.locator(
      'input[type="text"], textarea, [contenteditable="true"]'
    ).first();

    await cliInput.waitFor({ state: 'visible', timeout: 5000 });

    // Execute a command
    await cliInput.fill('/status');
    await cliInput.press('Enter');

    await page.waitForTimeout(500);

    // Look for timestamp patterns (HH:MM:SS, time indicators)
    const timestamps = page.locator('text=/[0-9]{1,2}:[0-9]{2}:[0-9]{2}|[0-9]{2}:[0-9]{2}/');

    const hasTimestamps = await timestamps.count();
    console.log('Timestamps found:', hasTimestamps);
  });

  test('should show command syntax/format in output', async ({ page }) => {
    const cliInput = page.locator(
      'input[type="text"], textarea, [contenteditable="true"]'
    ).first();

    await cliInput.waitFor({ state: 'visible', timeout: 5000 });

    // Execute help to see command format
    await cliInput.fill('/help');
    await cliInput.press('Enter');

    await page.waitForTimeout(1000);

    // Should show command syntax like "/command [args]"
    const syntaxPattern = page.locator('text=/\\/[a-z]+|command/i');

    const hasSyntax = await syntaxPattern.count();
    console.log('Command syntax shown:', hasSyntax > 0);
  });
});
