// case: test-cases/API_Create_Read_Update_Delete/part-and-category-crud.md (API-CRUD-016)
import { test, expect } from '../../../fixtures';

test.use({ user: 'engineer' });

test.describe('Part and category CRUD', () => {
  test('API-CRUD-016: Create a category', { tag: ['@smoke', '@regression'] }, async ({ api, data }) => {
    const payload = { name: data.name('Category'), description: 'QA API category', structural: false };
    let pk = 0;

    await test.step('1. POST /api/part/category/ as engineer', async () => {
      const res = await api.categories.create(payload);
      await expect(res).toHaveStatus(201);
      const body = await res.json();
      pk = data.trackCategory(body.pk);
      await expect.soft(res).toMatchSchema('Category');
      expect(body.name).toBe(payload.name);
      expect(body.description).toBe(payload.description);
      expect(body.structural).toBe(payload.structural);
      expect(body.parent).toBeNull();
      expect(Number.isInteger(body.pk)).toBe(true);
    });

    await test.step('2. GET /api/part/category/<pk from step 1>/ as engineer', async () => {
      const res = await api.categories.retrieve(pk);
      await expect(res).toHaveStatus(200);
      const body = await res.json();
      expect(body.name).toBe(payload.name);
      expect(body.description).toBe(payload.description);
    });
  });
});
