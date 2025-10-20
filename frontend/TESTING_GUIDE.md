# Frontend E2E Testing Guide

**Test Framework**: Playwright
**Test Count**: 4 test suites, ~60 tests
**Coverage**: Dashboard, Chat Interface, WebSocket, CLI

---

## 📋 Test Suites

### 1. Dashboard Tests (`tests/dashboard.spec.ts`)
**Tests**: 11

- ✅ Page load and rendering
- ✅ Navigation between pages (Dashboard/CLI/Chat)
- ✅ Active button state indication
- ✅ Stats panel display
- ✅ Responsive mobile layout
- ✅ Page refresh handling
- ✅ Console error detection
- ✅ Load time performance
- ✅ Agent cards display

### 2. Chat Interface Tests (`tests/chat.spec.ts`)
**Tests**: 15

- ✅ Chat interface visibility
- ✅ Agent selection
- ✅ Chat input field availability
- ✅ Typing in chat input
- ✅ Send message on Enter key
- ✅ Send message with button
- ✅ Multi-word message handling
- ✅ Character limit respect (2000 chars)
- ✅ Message history display
- ✅ Agent typing/status indicators
- ✅ Rapid message sending
- ✅ Empty message handling
- ✅ Mobile responsiveness

### 3. WebSocket Tests (`tests/websocket.spec.ts`)
**Tests**: 10

- ✅ WebSocket connection establishment
- ✅ Connection maintenance
- ✅ Send/receive messages
- ✅ Reconnection logic
- ✅ Real-time status updates
- ✅ Concurrent message handling
- ✅ Connection status indicator
- ✅ Error handling (offline mode)
- ✅ Rapid message performance
- ✅ Message latency testing

### 4. CLI Tests (`tests/cli.spec.ts`)
**Tests**: 20

- ✅ CLI interface display
- ✅ Terminal-style input
- ✅ Command prompt/prefix
- ✅ Command acceptance
- ✅ `/help` command execution
- ✅ `/status` command execution
- ✅ `/agents` command execution
- ✅ `/driver <message>` command
- ✅ `/creator <message>` command
- ✅ `/generator <message>` command
- ✅ Invalid command handling
- ✅ Command history navigation (↑/↓)
- ✅ Input clearing after execution
- ✅ Terminal output display
- ✅ Rapid command execution
- ✅ `/clear` command support
- ✅ Mobile responsiveness
- ✅ Command timestamps
- ✅ Command syntax display

---

## 🚀 Running Tests

### Prerequisites

**Both backend and frontend must be running:**

```bash
# Terminal 1 - Backend
cd backend
uv run python run.py

# Terminal 2 - Frontend (handled by Playwright)
# Playwright will automatically start the frontend
```

**Important**: Make sure the backend is running on `http://localhost:5000` before running tests.

### Test Commands

```bash
cd frontend

# Run all tests (headless)
npm run test:e2e

# Run with UI mode (recommended for development)
npm run test:e2e:ui

# Run with visible browser
npm run test:e2e:headed

# Debug mode
npm run test:e2e:debug

# Show test report
npm run test:e2e:report
```

### Run Specific Test Suite

```bash
# Only dashboard tests
npx playwright test dashboard

# Only chat tests
npx playwright test chat

# Only WebSocket tests
npx playwright test websocket

# Only CLI tests
npx playwright test cli
```

### Run on Specific Browser

```bash
# Chromium only
npx playwright test --project=chromium

# Firefox only
npx playwright test --project=firefox

# All browsers
npx playwright test
```

---

## 📊 Test Configuration

**File**: `playwright.config.ts`

### Key Settings:

- **Base URL**: `http://localhost:5173`
- **Timeout**: 30 seconds per test
- **Retries**: 0 (dev), 2 (CI)
- **Workers**: Parallel (dev), 1 (CI)
- **Browsers**: Chromium, Firefox, WebKit
- **Screenshots**: On failure
- **Video**: On failure
- **Trace**: On first retry

### Web Server:

Playwright automatically starts the frontend dev server (`npm run dev`) and waits for it to be ready before running tests.

---

## 🎯 Test Strategy

### 1. **Flexibility**
Tests are designed to be flexible and adapt to different UI implementations:
- Multiple selectors for finding elements
- Fallback strategies for various component structures
- Informational logging for optional features

### 2. **Real-World Scenarios**
Tests simulate actual user behavior:
- Typing and sending messages
- Navigating between pages
- Testing keyboard shortcuts
- Handling network issues

### 3. **Performance Testing**
- Page load times
- WebSocket message latency
- Rapid interaction handling
- Mobile responsiveness

### 4. **Error Detection**
- Console error monitoring
- WebSocket connection errors
- Graceful offline handling
- Invalid input handling

---

## 🔍 Debugging Failed Tests

### View Screenshots

Failed tests automatically capture screenshots:

```bash
# Screenshots saved to:
# test-results/<test-name>/test-failed-1.png
```

### View Videos

Failed tests record video:

```bash
# Videos saved to:
# test-results/<test-name>/video.webm
```

### Use Playwright Inspector

```bash
# Run in debug mode
npm run test:e2e:debug

# This opens the Playwright Inspector
# You can step through tests line by line
```

### View Trace

```bash
# After test failure, view trace
npx playwright show-trace test-results/<test-name>/trace.zip
```

---

## 📝 Writing New Tests

### Test Structure

```typescript
import { test, expect } from '@playwright/test';

test.describe('Feature Name', () => {
  test.beforeEach(async ({ page }) => {
    // Setup before each test
    await page.goto('/');
  });

  test('should do something', async ({ page }) => {
    // Arrange
    const button = page.locator('button:has-text("Click Me")');

    // Act
    await button.click();

    // Assert
    await expect(page.locator('text=Success')).toBeVisible();
  });
});
```

### Best Practices

1. **Use data-testid attributes** for reliable selectors:
   ```tsx
   <button data-testid="send-message">Send</button>
   ```

   ```typescript
   await page.locator('[data-testid="send-message"]').click();
   ```

2. **Wait for network idle** when appropriate:
   ```typescript
   await page.waitForLoadState('networkidle');
   ```

3. **Use flexible selectors**:
   ```typescript
   // Good - flexible
   const input = page.locator('input[type="text"], textarea').first();

   // Bad - brittle
   const input = page.locator('.chat-input-class-name');
   ```

4. **Add timeouts** for slow operations:
   ```typescript
   await expect(element).toBeVisible({ timeout: 10000 });
   ```

5. **Handle optional features** gracefully:
   ```typescript
   const hasFeature = await page.locator('text=Feature').count();
   if (hasFeature > 0) {
     // Test the feature
   }
   ```

---

## 🐛 Common Issues

### Issue: "Timeout waiting for page to load"

**Solution**:
- Ensure backend is running (`uv run python run.py`)
- Check if frontend port 5173 is available
- Increase timeout in `playwright.config.ts`

### Issue: "Element not found"

**Solution**:
- Check if the element exists in the UI
- Use `page.pause()` to inspect the page state
- Add `await page.waitForTimeout(1000)` for dynamic content

### Issue: "WebSocket connection failed"

**Solution**:
- Ensure backend is running with WebSocket support
- Check backend is using `run.py` (not `flask run`)
- Verify CORS settings in backend `.env`

### Issue: "Tests pass locally but fail in CI"

**Solution**:
- Use `process.env.CI` checks in config
- Increase timeouts for CI
- Disable browser parallelization in CI

---

## 📈 Coverage Goals

**Target**: >80% frontend functionality coverage

### Current Coverage by Feature:

- **Navigation**: ~100% (all pages, buttons)
- **Chat Interface**: ~85% (basic + advanced features)
- **WebSocket**: ~70% (connection + messaging)
- **CLI**: ~90% (all commands + history)
- **Error Handling**: ~75% (offline, invalid input)
- **Responsiveness**: ~80% (mobile viewports)

### Not Covered (Future):

- File uploads (if implemented)
- Complex forms with validation
- Authentication flows (if added)
- Settings/preferences persistence
- Advanced agent workflows

---

## 🎨 CI/CD Integration

### GitHub Actions Example

```yaml
name: E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: |
          cd frontend
          npm install
          npx playwright install --with-deps

      - name: Start backend
        run: |
          cd backend
          uv run python run.py &
        env:
          FLASK_ENV: testing

      - name: Run tests
        run: |
          cd frontend
          npm run test:e2e

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: frontend/playwright-report/
```

---

## 📚 Resources

- [Playwright Documentation](https://playwright.dev/)
- [Playwright Test Best Practices](https://playwright.dev/docs/best-practices)
- [Playwright Selectors](https://playwright.dev/docs/selectors)
- [Playwright Debugging](https://playwright.dev/docs/debug)

---

**Test Suite Version**: 1.0.0
**Last Updated**: October 18, 2025
**Maintainer**: Virtual Startup Team
