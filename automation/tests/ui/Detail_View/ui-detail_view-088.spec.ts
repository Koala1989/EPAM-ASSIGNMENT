// case: test-cases/Part_Detail_View/part-detail-header-and-tab-visibility.md (UI-Detail_View-088)
import { test, expect } from '../../../fixtures';

test.use({ user: 'engineer' });

test.describe('Part detail header and tab visibility', () => {
  test('UI-Detail_View-088: The Variants tab is hidden for a part that is not a template', { tag: ['@regression'] },
    async ({ partDetail, data }) => {
      const category = await data.category(data.name('Category'));
      const partName = data.name('NoTemplate');
      const part = await data.part(partName, { description: partName, category: category.pk, is_template: false });
      await partDetail.open(part.pk);

      await test.step('1. Check the tabs of the part.', async () => {
        await expect(partDetail.tab('Variants')).not.toBeVisible();
      });
    });
});
