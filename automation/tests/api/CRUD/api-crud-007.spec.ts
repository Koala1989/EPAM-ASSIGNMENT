// case: test-cases/API_Create_Read_Update_Delete/part-and-category-crud.md (API-CRUD-007)
import { test, expect } from '../../../fixtures';

test.use({ user: 'engineer' });

test.describe('Part and category CRUD', () => {
  test(
    'API-CRUD-007: The read-only full_name is returned for a created part',
    { tag: ['@regression', '@settings'] },
    async ({ api, data }) => {
      const name = data.name('Full Name');
      const ipn = `${name.split(' ')[0]}-IPN`;
      const expectedFullName = `${ipn} | ${name}`;
      let pk = 0;

      await test.step('1. POST /api/part/ as engineer', async () => {
        const res = await api.parts.create({ name, IPN: ipn });
        await expect(res).toHaveStatus(201);
        const body = await res.json();
        pk = data.trackPart(body.pk);
        expect(body.full_name).toBe(expectedFullName);
      });

      await test.step('2. GET /api/part/<pk from step 1>/ as engineer', async () => {
        const res = await api.parts.retrieve(pk);
        await expect(res).toHaveStatus(200);
        const body = await res.json();
        expect(body.full_name).toBe(expectedFullName);
      });
    },
  );
});
