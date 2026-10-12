import { test as base } from '@playwright/test';
import users from '../data/users.json';
import { BasePage } from '../pages/base.page';
import { LoginPage } from '../pages/login.page';

export type UserName = keyof typeof users;
export const userNames = Object.keys(users) as UserName[];
export const displayName = (user: UserName) => users[user].displayName;

type AuthOptions = {
  /** Demo user the test's `page` logs in as, through the login form, before the test body; `test.use({ user: 'engineer' })`. */
  user: UserName | undefined;
};

type AuthFixtures = {
  /** Logs the current user out through the user menu and logs in as another user, in the same page. */
  switchUser: (user: UserName) => Promise<void>;
};

export const test = base.extend<AuthOptions & AuthFixtures>({
  user: [undefined, { option: true }],

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
