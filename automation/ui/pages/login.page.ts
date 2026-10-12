import { Locator, Page, expect } from '@playwright/test';
import { passwordFor } from '../config/env';
import { BasePage } from './base.page';

/** The login screen at /web/login. */
export class LoginPage extends BasePage {
  readonly usernameInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;

  constructor(page: Page) {
    super(page);
    this.usernameInput = page.getByRole('textbox', { name: 'login-username' });
    this.passwordInput = page.getByRole('textbox', { name: 'login-password' });
    this.loginButton = page.getByRole('button', { name: 'Log In' });
  }

  /** Opens the login screen (not through BasePage.goto: there is no app shell before login). */
  async open() {
    await this.page.goto('/web/login');
    await expect(this.usernameInput).toBeVisible();
  }

  /**
   * Logs in through the login form, as a user would, and waits for the logged-in app shell.
   * The password comes from config/env.ts.
   */
  async loginAs(username: string) {
    const password = passwordFor(username);
    if (!(await this.usernameInput.isVisible())) await this.open();
    // The form re-renders once server info loads: it can clear what was typed, and a click on Log In
    // during the re-render sends no login request. Retry the whole login until the app shell appears.
    // Each action has a short timeout: if an earlier attempt's login is still completing, the form is
    // gone and the attempt must fail fast so the next one sees the app shell instead of hanging.
    await expect(async () => {
      if (await this.navigationMenu.isVisible()) return;
      await this.usernameInput.fill(username, { timeout: 2_000 });
      await this.passwordInput.fill(password, { timeout: 2_000 });
      await expect(this.usernameInput).toHaveValue(username, { timeout: 1_000 });
      await expect(this.passwordInput).toHaveValue(password, { timeout: 1_000 });
      await this.loginButton.click({ timeout: 2_000 });
      await expect(this.navigationMenu).toBeVisible({ timeout: 10_000 });
    }).toPass({ intervals: [1_000], timeout: 60_000 });
  }
}
