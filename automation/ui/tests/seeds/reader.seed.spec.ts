import { test, expect } from '../../fixtures';

test.use({ user: 'reader' });

test('seed: logged in as reader', async ({ app }) => {
  await app.openHome();
  await expect(app.navigationMenu).toBeVisible();
});
