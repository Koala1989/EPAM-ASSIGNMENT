import { mergeTests } from '@playwright/test';
import { test as apiTest } from './api.fixture';
import { test as dataTest } from './data.fixture';

export const test = mergeTests(apiTest, dataTest);
export { expect } from './expect';
export type { UserName, Caller } from './api.fixture';
export type { ApiRecord } from './data.fixture';
