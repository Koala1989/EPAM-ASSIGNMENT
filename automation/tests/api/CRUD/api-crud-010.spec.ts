// case: test-cases/API_Create_Read_Update_Delete/part-and-category-crud.md (API-CRUD-010)
import { test, expect } from '../../../fixtures';

test.use({ user: 'engineer' });

test.describe('Part and category CRUD', () => {
  test('API-CRUD-010: Update a part with PUT', { tag: ['@regression'] }, async ({ api, data }) => {
    const category = await data.category(data.name('Category'));
    const part = await data.part(data.name('Put Me'), { description: 'QA before' });
    const payload = {
      name: data.name('Put Done'),
      description: 'QA after',
      category: category.pk,
      active: true,
    };

    await test.step('1. PUT /api/part/<pk>/ as engineer', async () => {
      const res = await api.parts.update(part.pk, payload);
      await expect(res).toHaveStatus(200);
      await expect.soft(res).toMatchSchema('Part');
      const body = await res.json();
      expect(body.name).toBe(payload.name);
      expect(body.description).toBe(payload.description);
      expect(body.category).toBe(payload.category);
    });

    await test.step('2. GET /api/part/<pk>/ as engineer', async () => {
      const res = await api.parts.retrieve(part.pk);
      await expect(res).toHaveStatus(200);
      const body = await res.json();
      expect(body.name).toBe(payload.name);
      expect(body.description).toBe(payload.description);
      expect(body.category).toBe(payload.category);
    });
  });
});
