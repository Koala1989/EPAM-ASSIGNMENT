import { test as base, APIRequestContext, APIResponse } from '@playwright/test';
import { env, passwordFor } from '../config/env';
import { createApiContext } from '../utils/api-client';
import { qaName, qaSuffix } from '../utils/names';

type Json = Record<string, unknown>;
export type ApiRecord = { pk: number; name?: string } & Json;

async function body(res: APIResponse, what: string) {
  if (!res.ok()) throw new Error(`${what}: HTTP ${res.status()} ${await res.text()}`);
  return res.status() === 204 ? null : res.json();
}

/**
 * Prerequisite data created through the API as admin with unique QA-<8 hex> names,
 * removed after the test in reverse order. Settings changed here are restored.
 */
export class TestData {
  readonly suffix = qaSuffix();
  private readonly cleanups: (() => Promise<void>)[] = [];

  constructor(private readonly api: APIRequestContext) {}

  name(label: string) {
    return qaName(this.suffix, label);
  }

  async post(endpoint: string, fields: Json): Promise<ApiRecord> {
    return body(await this.api.post(endpoint, { data: fields }), `POST ${endpoint}`);
  }

  async category(name: string, fields: Json = {}) {
    const category = await this.post('part/category/', { name, ...fields });
    this.cleanups.push(() =>
      this.remove(`part/category/${category.pk}/`, { delete_parts: false, delete_child_categories: false }),
    );
    return category;
  }

  async part(name: string, fields: Json = {}) {
    const part = await this.post('part/', { name, ...fields });
    this.cleanups.push(() => this.deletePart(part.pk));
    return part;
  }

  async company(name: string, fields: Json = {}) {
    const company = await this.post('company/', { name, ...fields });
    this.cleanups.push(() => this.remove(`company/${company.pk}/`));
    return company;
  }

  async stockItem(part: number, quantity: number, fields: Json = {}) {
    const created = await this.post('stock/', { part, quantity, ...fields });
    const items = (Array.isArray(created) ? created : [created]) as ApiRecord[];
    for (const item of items) this.cleanups.push(() => this.remove(`stock/${item.pk}/`));
    return items[0];
  }

  /** Registers a part the test creates through the UI so it is deleted afterwards. Returns the name. */
  trackPart(name: string) {
    this.cleanups.push(async () => {
      for (const part of await this.findParts(name)) await this.deletePart(part.pk);
    });
    return name;
  }

  /** Looks up parts by exact name, e.g. to get the ID of a part the test created through the UI. */
  async findParts(name: string): Promise<ApiRecord[]> {
    const res = (await body(await this.api.get('part/', { params: { search: name, limit: 100 } }), 'GET part/')) as {
      results: ApiRecord[];
    };
    return res.results.filter((part) => part.name === name);
  }

  async setSetting(key: string, value: unknown) {
    const path = `settings/global/${key}/`;
    const before = (await body(await this.api.get(path), `GET ${path}`)) as Json;
    await body(await this.api.patch(path, { data: { value } }), `PATCH ${path}`);
    this.cleanups.push(async () => {
      await body(await this.api.patch(path, { data: { value: before.value } }), `restore ${path}`);
    });
  }

  async dispose() {
    const errors: string[] = [];
    for (const cleanup of this.cleanups.reverse()) {
      try {
        await cleanup();
      } catch (error) {
        errors.push(String(error));
      }
    }
    if (errors.length) throw new Error(`Cleanup failed:\n${errors.join('\n')}`);
  }

  private async remove(path: string, fields?: Json) {
    const res = await this.api.delete(path, fields ? { data: fields } : undefined);
    if (!res.ok() && res.status() !== 404) await body(res, `DELETE ${path}`);
  }

  // A part must be inactive before it can be deleted; its stock, supplier and manufacturer parts go first.
  private async deletePart(pk: number) {
    for (const endpoint of ['stock/', 'company/part/', 'company/part/manufacturer/']) {
      const res = (await body(await this.api.get(endpoint, { params: { part: pk, limit: 500 } }), `GET ${endpoint}`)) as
        | { results: ApiRecord[] }
        | ApiRecord[];
      for (const row of Array.isArray(res) ? res : res.results) await this.remove(`${endpoint}${row.pk}/`);
    }
    await this.api.patch(`part/${pk}/`, { data: { active: false } });
    await this.remove(`part/${pk}/`);
  }
}

export const test = base.extend<{ data: TestData }, { adminApi: APIRequestContext }>({
  adminApi: [
    async ({}, use) => {
      const api = await createApiContext(env.baseURL, 'admin', passwordFor('admin'));
      await use(api);
      await api.dispose();
    },
    { scope: 'worker' },
  ],

  data: async ({ adminApi }, use) => {
    const data = new TestData(adminApi);
    await use(data);
    await data.dispose();
  },
});
