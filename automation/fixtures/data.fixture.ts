import { test as base, APIRequestContext, APIResponse } from '@playwright/test';
import { apiContext, tokenFor } from '../utils/api-context';
import { qaName, qaSuffix } from '../utils/names';
import type { Json } from '../clients';

export type ApiRecord = { pk: number; name?: string } & Json;

async function body(res: APIResponse, what: string) {
  if (!res.ok()) throw new Error(`${what}: HTTP ${res.status()} ${await res.text()}`);
  return res.status() === 204 ? null : res.json();
}

/**
 * Prerequisite data for UI and API tests, created through the API as admin with unique QA-<8 hex> names and
 * removed after the test in reverse order. Records the test itself creates (through the request under test, or
 * through the UI) are registered with track*() so they are removed too. Settings changed here are restored.
 */
export class TestData {
  readonly suffix = qaSuffix();
  private readonly cleanups: (() => Promise<void>)[] = [];

  constructor(private readonly admin: APIRequestContext) {}

  name(label: string) {
    return qaName(this.suffix, label);
  }

  async post(endpoint: string, fields: Json): Promise<ApiRecord> {
    return body(await this.admin.post(endpoint, { data: fields }), `POST ${endpoint}`);
  }

  async category(name: string, fields: Json = {}) {
    const category = await this.post('part/category/', { name, ...fields });
    this.trackCategory(category.pk);
    return category;
  }

  async part(name: string, fields: Json = {}) {
    const part = await this.post('part/', { name, ...fields });
    this.trackPart(part.pk);
    return part;
  }

  /** A parameter template for parts (model_type "part"); deleted after the test. */
  async parameterTemplate(name: string, fields: Json = {}) {
    const template = await this.post('parameter/template/', { name, model_type: 'part', ...fields });
    this.cleanups.push(() => this.remove(`parameter/template/${template.pk}/`));
    return template;
  }

  async company(name: string, fields: Json = {}) {
    const company = await this.post('company/', { name, ...fields });
    this.cleanups.push(() => this.remove(`company/${company.pk}/`));
    return company;
  }

  async location(name: string, fields: Json = {}) {
    const location = await this.post('stock/location/', { name, ...fields });
    // Like categories, the delete needs both flags in the body, else 400 (not in the schema).
    this.cleanups.push(() =>
      this.remove(`stock/location/${location.pk}/`, { delete_stock_items: false, delete_sub_locations: false }),
    );
    return location;
  }

  async supplierPart(part: number, supplier: number, SKU: string, fields: Json = {}) {
    const supplierPart = await this.post('company/part/', { part, supplier, SKU, ...fields });
    this.trackSupplierPart(supplierPart.pk);
    return supplierPart;
  }

  /** Adds stock for a part; the stock item is removed after the test. */
  async stockItem(part: number, quantity: number, fields: Json = {}) {
    const created = await this.post('stock/', { part, quantity, ...fields });
    const items = (Array.isArray(created) ? created : [created]) as ApiRecord[];
    for (const item of items) this.cleanups.push(() => this.remove(`stock/${item.pk}/`));
    return items[0];
  }

  /**
   * Registers a part the test creates, so it is deleted after the test, and returns what it was given.
   * API tests pass the pk from the response; UI tests pass the name they type into the form.
   */
  trackPart(pk: number): number;
  trackPart(name: string): string;
  trackPart(part: number | string) {
    this.cleanups.push(async () => {
      const pks = typeof part === 'number' ? [part] : (await this.findParts(part)).map((found) => found.pk);
      for (const pk of pks) await this.deletePart(pk);
    });
    return part;
  }

  /** Parts with exactly this name, e.g. to get the ID of a part the test created through the UI. */
  async findParts(name: string): Promise<ApiRecord[]> {
    const res = (await body(await this.admin.get('part/', { params: { search: name, limit: 100 } }), 'GET part/')) as {
      results: ApiRecord[];
    };
    return res.results.filter((part) => part.name === name);
  }

  /** Registers a category created by the request under test. Its parts and child categories are kept (moved up). */
  trackCategory(pk: number) {
    this.cleanups.push(() => this.remove(`part/category/${pk}/`, { delete_parts: false, delete_child_categories: false }));
    return pk;
  }

  /** Registers a supplier part created by the request under test. */
  trackSupplierPart(pk: number) {
    this.cleanups.push(() => this.remove(`company/part/${pk}/`));
    return pk;
  }

  async setSetting(key: string, value: unknown) {
    const path = `settings/global/${key}/`;
    const before = (await body(await this.admin.get(path), `GET ${path}`)) as Json;
    await body(await this.admin.patch(path, { data: { value } }), `PATCH ${path}`);
    this.cleanups.push(async () => {
      await body(await this.admin.patch(path, { data: { value: before.value } }), `restore ${path}`);
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
    const res = await this.admin.delete(path, fields ? { data: fields } : undefined);
    if (!res.ok() && res.status() !== 404) await body(res, `DELETE ${path}`);
  }

  // A part must be inactive before it can be deleted; its stock, supplier and manufacturer parts go first.
  private async deletePart(pk: number) {
    // Already deleted by the request under test: the part filter below would be rejected for an unknown part.
    if ((await this.admin.get(`part/${pk}/`)).status() === 404) return;
    for (const endpoint of ['stock/', 'company/part/', 'company/part/manufacturer/']) {
      const listing = await this.admin.get(endpoint, { params: { part: pk, limit: 500 } });
      // The supplier and manufacturer part filters reject parts that are not purchaseable: nothing to remove there.
      if (listing.status() === 400) continue;
      const res = (await body(listing, `GET ${endpoint}`)) as { results: ApiRecord[] } | ApiRecord[];
      for (const row of Array.isArray(res) ? res : res.results) await this.remove(`${endpoint}${row.pk}/`);
    }
    await this.admin.patch(`part/${pk}/`, { data: { active: false } });
    await this.remove(`part/${pk}/`);
  }
}

export const test = base.extend<{ data: TestData }, { adminContext: APIRequestContext }>({
  adminContext: [
    async ({}, use) => {
      const context = await apiContext(await tokenFor('admin'));
      await use(context);
      await context.dispose();
    },
    { scope: 'worker' },
  ],

  data: async ({ adminContext }, use) => {
    const data = new TestData(adminContext);
    await use(data);
    await data.dispose();
  },
});
