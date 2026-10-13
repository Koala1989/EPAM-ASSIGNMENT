// case: test-cases/API_CRUD/part-and-category-crud.md (API-CRUD-011)
import { test, expect } from '../../fixtures';

test.use({ user: 'engineer' });

test.describe('Part and category CRUD', () => {
  test('API-CRUD-011: Update one field of a part with PATCH', { tag: ['@smoke', '@regression'] }, async ({ api, data }) => {
    const name = data.name('Patch Me');
    const IPN = `${data.suffix}-P`;
    const part = await data.part(name, { description: 'QA keep', IPN });

    await test.step('1. PATCH /api/part/<pk>/ as engineer', async () => {
      const res = await api.parts.partialUpdate(part.pk, { description: 'QA changed' });
      await expect(res).toHaveStatus(200);
      await expect.soft(res).toMatchSchema('Part');
      const body = await res.json();
      expect(body.description).toBe('QA changed');
      expect(body.name).toBe(name);
      expect(body.IPN).toBe(IPN);
    });

    await test.step('2. GET /api/part/<pk>/ as engineer', async () => {
      const res = await api.parts.retrieve(part.pk);
      await expect(res).toHaveStatus(200);
      const body = await res.json();
      expect(body.description).toBe('QA changed');
      expect(body.name).toBe(name);
      expect(body.IPN).toBe(IPN);
    });
  });
});
