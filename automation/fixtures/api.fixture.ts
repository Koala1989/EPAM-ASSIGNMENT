import { APIRequestContext } from '@playwright/test';
import { test as base } from './user.fixture';
import type { UserName } from '../config/env';
import { Clients, clientsFor } from '../clients';
import { apiContext, tokenFor } from '../utils/api-context';

export type { UserName };
/** Who a request is sent as: a demo user (token auth), no credentials, or an explicit token. */
export type Caller = UserName | 'anonymous' | { token: string };

type ApiFixtures = { api: Clients; apiAs: (caller: Caller) => Promise<Clients> };

export const test = base.extend<ApiFixtures>({
  apiAs: async ({}, use) => {
    const contexts: APIRequestContext[] = [];
    await use(async (caller) => {
      const token = caller === 'anonymous' ? undefined : typeof caller === 'string' ? await tokenFor(caller) : caller.token;
      const context = await apiContext(token);
      contexts.push(context);
      return clientsFor(context);
    });
    for (const context of contexts) await context.dispose();
  },

  api: async ({ user, apiAs }, use) => {
    if (!user) throw new Error("No user for this spec: add test.use({ user: '<demo user>' }) from the case's Prerequisites.");
    await use(await apiAs(user));
  },
});
