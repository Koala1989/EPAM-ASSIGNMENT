import { mergeTests } from '@playwright/test';
import { test as apiTest } from './api.fixture';
import { test as authTest } from './auth.fixture';
import { test as dataTest } from './data.fixture';
import { test as pagesTest } from './pages.fixture';

// The only import for specs, UI and API alike. Fixtures are lazy: a UI spec never builds API clients it does not
// use, and an API spec never opens a browser.
export const test = mergeTests(authTest, pagesTest, apiTest, dataTest);
export { expect } from './expect';
export type { UserName } from './auth.fixture';
export type { Caller } from './api.fixture';
export type { ApiRecord } from './data.fixture';
