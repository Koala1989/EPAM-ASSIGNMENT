import { test as setup, expect } from '@playwright/test';
import { displayName, userNames } from '../../fixtures/auth.fixture';
import { LoginPage } from '../../pages/login.page';

// Smoke check before the suite: every demo user can log in and out through the UI.
// Tests log in themselves through the same LoginPage; nothing is saved here.
for (const user of userNames) {
  setup(`log in and out as ${user}`, async ({ page }) => {
    setup.setTimeout(90_000);
    const loginPage = new LoginPage(page);

    await loginPage.open();
    await loginPage.loginAs(user);
    await expect(loginPage.userMenu(displayName(user))).toBeVisible();

    await loginPage.logout(displayName(user));
    await expect(loginPage.usernameInput).toBeVisible();
  });
}
