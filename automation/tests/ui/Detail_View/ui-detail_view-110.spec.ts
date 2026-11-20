// case: test-cases/Part_Detail_View/part-detail-header-and-tab-visibility.md (UI-Detail_View-110)
import { test, expect } from '../../../fixtures';

test.use({ user: 'allaccess' });

test.describe('Part detail header and tab visibility', () => {
  test('UI-Detail_View-110: The Suppliers tab is visible for a Purchaseable part', { tag: ['@regression'] },
    async ({ partDetail, data }) => {
      const category = await data.category(data.name('Category'));
      const partName = data.name('Buy');
      const part = await data.part(partName, { description: partName, category: category.pk, purchaseable: true });
      await partDetail.open(part.pk);

      await test.step('1. Check the tabs of the part.', async () => {
        await expect(partDetail.tab('Suppliers')).toBeVisible();
      });
    });
});
