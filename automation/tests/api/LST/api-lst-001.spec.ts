// case: test-cases/API_Lists_and_Filters/lists-and-filters.md (API-LST-001)
import { test, expect } from '../../../fixtures';

test.use({ user: 'reader' });

test.describe('Lists and filters', () => {
  test('API-LST-001: A part list request with `limit` returns the paginated envelope with `count`, `results`, `next` and `previous`.', { tag: ['@smoke', '@regression'] }, async ({ api, data }) => {
    const category = await data.category(data.name('Page Cat'));
    await data.part(data.name('P1'), { category: category.pk });
    await data.part(data.name('P2'), { category: category.pk });
    await data.part(data.name('P3'), { category: category.pk });

    await test.step('1. GET /api/part/ as reader (category=<cat pk>, limit=2)', async () => {
      const res = await api.parts.list({ category: category.pk, limit: 2 });
      await expect(res).toHaveStatus(200);
      await expect.soft(res).toMatchSchema('PaginatedPartList');
      const body = await res.json();
      expect(body.count).toBe(3);
      expect(body.results).toHaveLength(2);
      expect(typeof body.next).toBe('string');
      expect(body.previous).toBeNull();
    });
  });
});
