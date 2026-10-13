// case: test-cases/API_CRUD/part-and-category-crud.md (API-CRUD-009)
import { test, expect } from '../../fixtures';

test.use({ user: 'engineer' });

test.describe('Part and category CRUD', () => {
  test(
    'API-CRUD-009: Read a part with an ID that does not exist',
    { tag: ['@regression'] },
    async ({ api, apiAs, data }) => {
      // Prerequisite: a pk that no longer exists (create as admin, make inactive, delete).
      const admin = await apiAs('admin');
      const part = await data.part(data.name('Deleted Part'));
      await expect(await admin.parts.partialUpdate(part.pk, { active: false })).toHaveStatus(200);
      await expect(await admin.parts.destroy(part.pk)).toHaveStatus(204);

      await test.step('1. GET /api/part/<deleted pk>/ as engineer', async () => {
        const res = await api.parts.retrieve(part.pk);
        await expect(res).toHaveStatus(404);
        expect(await res.json()).toEqual({ detail: 'No Part matches the given query.' });
      });
    },
  );
});
