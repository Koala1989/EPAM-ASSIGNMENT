// case: test-cases/API_Create_Read_Update_Delete/part-and-category-crud.md (API-CRUD-003)
import { test, expect } from '../../../fixtures';

test.use({ user: 'engineer' });

test.describe('Part and category CRUD', () => {
  test('API-CRUD-003: A part created without `active` is active', { tag: ['@regression'] }, async ({ api, data }) => {
    const payload = { name: data.name('Default Active') };
    let pk = 0;

    await test.step('1. POST /api/part/ as engineer', async () => {
      const res = await api.parts.create(payload);
      await expect(res).toHaveStatus(201);
      const body = await res.json();
      pk = data.trackPart(body.pk);
      expect(body.active).toBe(true);
    });

    await test.step('2. GET /api/part/<pk from step 1>/ as engineer', async () => {
      const res = await api.parts.retrieve(pk);
      await expect(res).toHaveStatus(200);
      const body = await res.json();
      expect(body.active).toBe(true);
    });
  });
});
