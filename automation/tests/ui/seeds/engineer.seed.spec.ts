import { test, expect } from '../../../fixtures';

test.use({ user: 'engineer' });

test('seed: logged in as engineer', async ({ app }) => {
  await app.openHome();
  await expect(app.navigationMenu).toBeVisible();
});
