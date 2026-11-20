// case: test-cases/API_Lists_and_Filters/lists-and-filters.md (API-LST-005)
import { test, expect } from '../../../fixtures';

test.use({ user: 'reader' });

test.describe('Lists and filters', () => {
  test('API-LST-005: `offset` skips that many results and the page starts at the next one.', { tag: ['@regression'] }, async ({ api, data }) => {
    const category = await data.category(data.name('Page Cat'));
    const name1 = data.name('P1');
    const name2 = data.name('P2');
    const name3 = data.name('P3');
    await data.part(name1, { category: category.pk });
    await data.part(name2, { category: category.pk });
    await data.part(name3, { category: category.pk });

    await test.step('1. GET /api/part/ as reader (category=<cat pk>, limit=2, offset=1, ordering=id)', async () => {
      const res = await api.parts.list({ category: category.pk, limit: 2, offset: 1, ordering: 'id' });
      await expect(res).toHaveStatus(200);
      await expect.soft(res).toMatchSchema('PaginatedPartList');
      const body = await res.json();
      expect(body.count).toBe(3);
      expect(body.results.map((p: { name: string }) => p.name)).toEqual([name2, name3]);
      expect(typeof body.previous).toBe('string');
    });
  });
});
