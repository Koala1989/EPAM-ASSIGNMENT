import { test, expect } from '../../../fixtures';

test.use({ user: 'allaccess' });

test('seed: logged in as allaccess', async ({ app }) => {
  await app.openHome();
  await expect(app.navigationMenu).toBeVisible();
});
