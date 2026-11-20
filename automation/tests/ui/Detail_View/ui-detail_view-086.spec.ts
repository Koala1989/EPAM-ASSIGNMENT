// case: test-cases/Part_Detail_View/part-detail-header-and-tab-visibility.md (UI-Detail_View-086)
import { test, expect } from '../../../fixtures';

test.use({ user: 'allaccess' });

test.describe('Part detail header and tab visibility', () => {
  test('UI-Detail_View-086: A part with every conditional attribute off shows none of the conditional tabs', { tag: ['@regression'] },
    async ({ partDetail, data }) => {
      const category = await data.category(data.name('Category'));
      const partName = data.name('AllOff');
      const part = await data.part(partName, {
        description: partName,
        category: category.pk,
        is_template: false,
        assembly: false,
        component: false,
        salable: false,
        purchaseable: false,
      });
      await partDetail.open(part.pk);
      await expect(partDetail.title).toContainText(partName);

      await test.step('1. Read the tab list of the part page.', async () => {
        // The page has finished rendering its tabs before the absences are checked.
        await expect(partDetail.tab('Part Details')).toBeVisible();
        for (const name of ['Variants', 'Allocated', 'BOM', 'Used In', 'Suppliers', 'Purchase Orders']) {
          await expect(partDetail.tab(name)).toBeHidden();
        }
      });
    });
});
