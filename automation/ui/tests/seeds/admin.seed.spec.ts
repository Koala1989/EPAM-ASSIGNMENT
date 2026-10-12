import { test, expect } from '../../fixtures';

test.use({ user: 'admin' });

test('seed: logged in as admin', async ({ app }) => {
  await app.openHome();
  await expect(app.navigationMenu).toBeVisible();
});
