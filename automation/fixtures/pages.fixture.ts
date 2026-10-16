import { test as base } from '@playwright/test';
import { BasePage } from '../pages/base.page';
import { LoginPage } from '../pages/login.page';
import { PartsPage } from '../pages/parts.page';
import { PartFormPage } from '../pages/part-form.page';
import { PartDetailPage } from '../pages/part-detail.page';
import { ParameterFormPage } from '../pages/parameter-form.page';
import { StockItemFormPage } from '../pages/stock-item-form.page';

export type Pages = {
  parameterForm: ParameterFormPage;
  stockItemForm: StockItemFormPage;
  app: BasePage;
  loginPage: LoginPage;
  partsPage: PartsPage;
  partForm: PartFormPage;
  partDetail: PartDetailPage;
};

export const test = base.extend<Pages>({
  parameterForm: async ({ page }, use) => use(new ParameterFormPage(page)),
  stockItemForm: async ({ page }, use) => use(new StockItemFormPage(page)),
  app: async ({ page }, use) => use(new BasePage(page)),
  loginPage: async ({ page }, use) => use(new LoginPage(page)),
  partsPage: async ({ page }, use) => use(new PartsPage(page)),
  partForm: async ({ page }, use) => use(new PartFormPage(page)),
  partDetail: async ({ page }, use) => use(new PartDetailPage(page)),
});
