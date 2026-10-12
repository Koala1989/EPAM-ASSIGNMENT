import { mergeTests } from '@playwright/test';
import { test as authTest } from './auth.fixture';
import { test as dataTest } from './data.fixture';
import { test as pagesTest } from './pages.fixture';

export const test = mergeTests(authTest, dataTest, pagesTest);
export { expect } from '@playwright/test';
export type { UserName } from './auth.fixture';
