// case: test-cases/API_Create_Read_Update_Delete/part-and-category-crud.md (API-CRUD-021)
import { test, expect } from '../../../fixtures';

test.use({ user: 'admin' });

test.describe('Part and category CRUD', () => {
  test('API-CRUD-021: Delete an empty category', { tag: ['@smoke', '@regression'] }, async ({ api, data }) => {
    const category = await data.category(data.name('Delete Category'));

    await test.step('1. DELETE /api/part/category/<pk>/ as admin', async () => {
      const res = await api.categories.destroy(category.pk, { delete_parts: false, delete_child_categories: false });
      await expect(res).toHaveStatus(204);
      expect(await res.text()).toBe('');
    });

    await test.step('2. GET /api/part/category/<pk>/ as admin', async () => {
      const res = await api.categories.retrieve(category.pk);
      await expect(res).toHaveStatus(404);
      expect(await res.json()).toEqual({ detail: 'No PartCategory matches the given query.' });
    });
  });
});
