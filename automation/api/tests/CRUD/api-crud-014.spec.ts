// case: test-cases/API_CRUD/part-and-category-crud.md (API-CRUD-014)
import { test, expect } from '../../fixtures';

test.use({ user: 'admin' });

test.describe('Part and category CRUD', () => {
  test('API-CRUD-014: Delete an active part', { tag: ['@regression'] }, async ({ api, data }) => {
    const part = await data.part(data.name('Active Delete'), { active: true });

    await test.step('1. DELETE /api/part/<pk>/ as admin', async () => {
      const res = await api.parts.destroy(part.pk);
      await expect(res).toHaveStatus(400);
      expect(await res.json()).toEqual({ non_field_errors: ['Cannot delete this part as it is still active'] });
    });

    await test.step('2. GET /api/part/<pk>/ as admin', async () => {
      const res = await api.parts.retrieve(part.pk);
      await expect(res).toHaveStatus(200);
      const body = await res.json();
      expect(body.active).toBe(true);
    });
  });
});
