// case: test-cases/API_Create_Read_Update_Delete/part-and-category-crud.md (API-CRUD-008)
import { test, expect } from '../../../fixtures';

test.use({ user: 'engineer' });

test.describe('Part and category CRUD', () => {
  test('API-CRUD-008: Read a part by ID', { tag: ['@smoke', '@regression'] }, async ({ api, data }) => {
    const name = data.name('Read Me');
    const part = await data.part(name, { description: 'QA read' });

    await test.step('1. GET /api/part/<pk>/ as engineer', async () => {
      const res = await api.parts.retrieve(part.pk);
      await expect(res).toHaveStatus(200);
      await expect.soft(res).toMatchSchema('Part');
      const body = await res.json();
      expect(body.pk).toBe(part.pk);
      expect(body.name).toBe(name);
      expect(body.description).toBe('QA read');
    });
  });
});
