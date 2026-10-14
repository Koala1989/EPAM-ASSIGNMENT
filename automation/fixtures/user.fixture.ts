import { test as base } from '@playwright/test';
import type { UserName } from '../config/env';

/**
 * The `user` option every suite shares: `test.use({ user: 'engineer' })`, the user from the case's Prerequisites.
 * UI tests: `page` logs in as this user (auth.fixture). API tests: `api` is authenticated as this user (api.fixture).
 */
export const test = base.extend<{ user: UserName | undefined }>({
  user: [undefined, { option: true }],
});
