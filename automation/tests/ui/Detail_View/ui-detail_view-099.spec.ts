// case: test-cases/Part_Detail_View/part-detail-header-and-tab-visibility.md (UI-Detail_View-099)
import { test, expect } from '../../../fixtures';

test.use({ user: 'engineer' });

test.describe('Part detail header and tab visibility', () => {
  test('UI-Detail_View-099: The BOM tab is visible for an Assembly part', { tag: ['@smoke', '@regression'] },
    async ({ partDetail, data }) => {
      const category = await data.category(data.name('Category'));
      const partName = data.name('Asm');
      const part = await data.part(partName, { description: partName, category: category.pk, assembly: true });
      await partDetail.open(part.pk);

      await test.step('1. Check the tabs of the part.', async () => {
        // The app names the BOM tab "Bill of Materials".
        await expect(partDetail.tab('Bill of Materials')).toBeVisible();
      });
    });
});
