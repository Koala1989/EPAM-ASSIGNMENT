// case: test-cases/API_Create_Read_Update_Delete/part-and-category-crud.md (API-CRUD-001)
import { test, expect } from '../../../fixtures';

test.use({ user: 'engineer' });

test.describe('Part and category CRUD', () => {
  test(
    'API-CRUD-001: Create a part with name, description and category',
    { tag: ['@smoke', '@regression'] },
    async ({ api, data }) => {
      const category = await data.category(data.name('Category'));
      const payload = {
        name: data.name('Resistor 10k'),
        description: 'QA API part',
        category: category.pk,
      };
      let pk = 0;

      await test.step('1. POST /api/part/ as engineer', async () => {
        const res = await api.parts.create(payload);
        await expect(res).toHaveStatus(201);
        await expect(res).toMatchSchema('Part');
        const body = await res.json();
        pk = data.trackPart(body.pk);
        expect(body.name).toBe(payload.name);
        expect(body.description).toBe(payload.description);
        expect(body.category).toBe(payload.category);
        expect(Number.isInteger(body.pk)).toBe(true);
      });

      await test.step('2. GET /api/part/<pk from step 1>/ as engineer', async () => {
        const res = await api.parts.retrieve(pk);
        await expect(res).toHaveStatus(200);
        await expect(res).toMatchSchema('Part');
        const body = await res.json();
        expect(body.name).toBe(payload.name);
        expect(body.description).toBe(payload.description);
        expect(body.category).toBe(payload.category);
      });
    },
  );
});
