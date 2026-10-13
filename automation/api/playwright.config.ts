import { defineConfig } from '@playwright/test';
import { env } from './config/env';

export default defineConfig({
  testDir: './tests',
  timeout: env.testTimeout,
  expect: { timeout: env.expectTimeout },
  // Serial: InvenTree rebuilds the whole part/category tree on every delete, and concurrent rebuilds deadlock (HTTP 500).
  fullyParallel: false,
  workers: 1,
  forbidOnly: !!process.env.CI,
  retries: 0,
  reporter: [['list'], ['html', { open: 'never' }]],
  projects: [
    { name: 'api-smoke', testMatch: /setup\/.*\.setup\.ts/ },
    { name: 'api', testMatch: /.*\.spec\.ts/, dependencies: ['api-smoke'] },
  ],
});
