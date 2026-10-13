// case: test-cases/API_CRUD/part-and-category-crud.md (API-CRUD-012)
import { test, expect } from '../../fixtures';

test.use({ user: 'engineer' });

test.describe('Part and category CRUD', () => {
  test('API-CRUD-012: Make a part inactive with PATCH', { tag: ['@regression'] }, async ({ api, data }) => {
    const name = data.name('Deactivate');
    const part = await data.part(name, { description: 'Seed API part' });

    await test.step('1. PATCH /api/part/<pk>/ as engineer', async () => {
      const res = await api.parts.partialUpdate(part.pk, { active: false });
      await expect(res).toHaveStatus(200);
      await expect.soft(res).toMatchSchema('Part');
      const body = await res.json();
      expect(body.active).toBe(false);
    });

    await test.step('2. GET /api/part/<pk>/ as engineer', async () => {
      const res = await api.parts.retrieve(part.pk);
      await expect(res).toHaveStatus(200);
      const body = await res.json();
      expect(body.active).toBe(false);
      expect(body.name).toBe(name);
    });
  });
});
