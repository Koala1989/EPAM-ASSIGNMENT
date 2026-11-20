// case: test-cases/API_Relationships/part-and-category-crud.md (API-REL-001)
import { test, expect } from '../../../fixtures';

test.use({ user: 'admin' });

test.describe('Part and category CRUD', () => {
  test('API-REL-001: Delete a category that contains a part', { tag: ['@regression'] }, async ({ api, data }) => {
    const category = await data.category(data.name('Category'));
    const part = await data.part(data.name('Child Part'), { category: category.pk });

    await test.step('1. DELETE /api/part/category/<category pk>/ as admin', async () => {
      const res = await api.categories.destroy(category.pk, { delete_parts: false, delete_child_categories: false });
      await expect(res).toHaveStatus(204);
      expect(await res.text()).toBe('');
    });

    await test.step('2. GET /api/part/category/<category pk>/ as admin', async () => {
      const res = await api.categories.retrieve(category.pk);
      await expect(res).toHaveStatus(404);
      expect(await res.json()).toEqual({ detail: 'No PartCategory matches the given query.' });
    });

    await test.step('3. GET /api/part/<part pk>/ as admin', async () => {
      const res = await api.parts.retrieve(part.pk);
      await expect(res).toHaveStatus(200);
      const body = await res.json();
      expect(body.pk).toBe(part.pk);
      expect(body.category).toBeNull();
    });
  });
});
