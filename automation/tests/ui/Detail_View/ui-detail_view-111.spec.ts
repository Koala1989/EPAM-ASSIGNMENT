// case: test-cases/Part_Detail_View/part-detail-header-and-tab-visibility.md (UI-Detail_View-111)
import { test, expect } from '../../../fixtures';

test.use({ user: 'allaccess' });

test.describe('Part detail header and tab visibility', () => {
  test('UI-Detail_View-111: The Suppliers tab is hidden for a part that is not Purchaseable', { tag: ['@regression'] },
    async ({ partDetail, data }) => {
      const category = await data.category(data.name('Category'));
      const partName = data.name('NoBuy');
      const part = await data.part(partName, { description: partName, category: category.pk, purchaseable: false });
      await partDetail.open(part.pk);

      await test.step('1. Check the tabs of the part.', async () => {
        // The tab list is rendered (Part Details is always shown) before asserting the absence of Suppliers.
        await expect(partDetail.tab('Part Details')).toBeVisible();
        await expect(partDetail.tab('Suppliers')).toBeHidden();
      });
    });
});
