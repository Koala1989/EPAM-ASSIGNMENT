import { defineConfig, devices } from '@playwright/test';
import { env } from './config/env';

// One project for both suites. UI: login-smoke -> chromium (tests/ui). API: api-smoke -> api (tests/api).
// SKIP_LOGIN_SMOKE=1 drops the login-smoke dependency for single-spec agent runs (set for the playwright-test
// MCP server in .mcp.json); each test still logs in through the real login form via the user fixture.
const skipLoginSmoke = process.env.SKIP_LOGIN_SMOKE === '1';

export default defineConfig({
  timeout: env.testTimeout,
  expect: { timeout: env.expectTimeout },
  forbidOnly: !!process.env.CI,
  // Serial for both suites: UI tests change global InvenTree settings that a parallel test would see, and
  // concurrent part/category deletes deadlock InvenTree's tree rebuild (HTTP 500).
  fullyParallel: false,
  workers: 1,
  reporter: [['list'], ['html', { open: 'never' }]],
  use: {
    baseURL: env.baseURL,
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'login-smoke', testDir: './tests/ui', testMatch: /setup\/login\.setup\.ts/ },
    {
      name: 'chromium',
      testDir: './tests/ui',
      use: { ...devices['Desktop Chrome'] },
      retries: process.env.CI ? 1 : 0,
      dependencies: skipLoginSmoke ? [] : ['login-smoke'],
    },
    { name: 'api-smoke', testDir: './tests/api', testMatch: /setup\/.*\.setup\.ts/ },
    { name: 'api', testDir: './tests/api', testMatch: /.*\.spec\.ts/, dependencies: ['api-smoke'] },
  ],
});
