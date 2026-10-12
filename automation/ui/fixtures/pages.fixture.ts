import { test as base } from '@playwright/test';
import { BasePage } from '../pages/base.page';
import { LoginPage } from '../pages/login.page';
import { PartsPage } from '../pages/parts.page';
import { PartFormPage } from '../pages/part-form.page';
import { PartDetailPage } from '../pages/part-detail.page';

export type Pages = {
  app: BasePage;
  loginPage: LoginPage;
  partsPage: PartsPage;
  partForm: PartFormPage;
  partDetail: PartDetailPage;
};

export const test = base.extend<Pages>({
  app: async ({ page }, use) => use(new BasePage(page)),
  loginPage: async ({ page }, use) => use(new LoginPage(page)),
  partsPage: async ({ page }, use) => use(new PartsPage(page)),
  partForm: async ({ page }, use) => use(new PartFormPage(page)),
  partDetail: async ({ page }, use) => use(new PartDetailPage(page)),
});
