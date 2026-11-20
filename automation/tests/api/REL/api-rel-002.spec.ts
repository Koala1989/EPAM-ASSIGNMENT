// case: test-cases/API_Relationships/part-and-category-crud.md (API-REL-002)
import { test, expect } from '../../../fixtures';

test.use({ user: 'admin' });

test.describe('Part and category CRUD', () => {
  test('API-REL-002: Delete a category that has a child category', { tag: ['@regression'] }, async ({ api, data }) => {
    const parent = await data.category(data.name('Parent'));
    const child = await data.category(data.name('Child'), { parent: parent.pk });

    await test.step('1. GET /api/part/category/<parent pk>/ as admin', async () => {
      const res = await api.categories.retrieve(parent.pk);
      await expect(res).toHaveStatus(200);
      const body = await res.json();
      expect(body.subcategories).toBe(1);
    });

    await test.step('2. DELETE /api/part/category/<parent pk>/ as admin', async () => {
      const res = await api.categories.destroy(parent.pk, { delete_parts: false, delete_child_categories: false });
      await expect(res).toHaveStatus(204);
      expect(await res.text()).toBe('');
    });

    await test.step('3. GET /api/part/category/<parent pk>/ as admin', async () => {
      const res = await api.categories.retrieve(parent.pk);
      await expect(res).toHaveStatus(404);
      expect(await res.json()).toEqual({ detail: 'No PartCategory matches the given query.' });
    });

    await test.step('4. GET /api/part/category/<child pk>/ as admin', async () => {
      const res = await api.categories.retrieve(child.pk);
      await expect(res).toHaveStatus(200);
      const body = await res.json();
      expect(body.parent).toBeNull();
      expect(body.level).toBe(0);
    });
  });
});
