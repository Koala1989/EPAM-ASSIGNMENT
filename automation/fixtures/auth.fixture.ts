import { test as base } from './user.fixture';
import { users, userNames, type UserName } from '../config/env';
import { BasePage } from '../pages/base.page';
import { LoginPage } from '../pages/login.page';

export { userNames, type UserName };
export const displayName = (user: UserName) => users[user].displayName;

type AuthFixtures = {
  /** Logs the current user out through the user menu and logs in as another user, in the same page. */
  switchUser: (user: UserName) => Promise<void>;
};

// `page` logs in as the `user` option (user.fixture), through the login form, before the test body.
export const test = base.extend<AuthFixtures>({
  page: async ({ page, user }, use) => {
    if (user) await new LoginPage(page).loginAs(user);
    await use(page);
  },

  switchUser: async ({ page, user }, use) => {
    let current = user;
    await use(async (next) => {
      if (current) await new BasePage(page).logout(displayName(current));
      await new LoginPage(page).loginAs(next);
      current = next;
    });
  },
});
