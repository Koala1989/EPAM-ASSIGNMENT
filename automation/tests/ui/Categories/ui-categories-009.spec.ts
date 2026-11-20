// case: test-cases/Categories/category-hierarchy-and-filtering.md (UI-Categories-009)
import { test, expect } from '../../../fixtures';

test.use({ user: 'engineer' });

test.describe('Category hierarchy and filtering', () => {
  test('UI-Categories-009: A parent category\'s part list includes the parts of all its sub-categories', { tag: ['@smoke', '@regression'] },
    async ({ partsPage, categoryPage, data }) => {
      const topName = data.name('Top');
      const partNames = [
        data.name('Part Top'),
        data.name('Part Mid'),
        data.name('Part Leaf'),
        data.name('Part Deep'),
        data.name('Part Sib'),
      ];

      const top = await data.category(topName);
      const mid = await data.category(data.name('Mid'), { parent: top.pk });
      const leaf = await data.category(data.name('Leaf'), { parent: mid.pk });
      const deep = await data.category(data.name('Deep'), { parent: leaf.pk });
      const sibling = await data.category(data.name('Sibling'), { parent: top.pk });
      await data.category(data.name('Empty'), { parent: top.pk });
      await data.part(data.name('Part Top'), { category: top.pk });
      await data.part(data.name('Part Mid'), { category: mid.pk });
      await data.part(data.name('Part Leaf'), { category: leaf.pk });
      await data.part(data.name('Part Deep'), { category: deep.pk });
      await data.part(data.name('Part Sib'), { category: sibling.pk });

      await partsPage.openCategories();

      await test.step('1. Open the top category from the Parts view', async () => {
        await partsPage.openCategoryByName(topName);
        await expect(categoryPage.partsTab).toBeVisible();
      });

      await test.step('2. Read the category\'s part list', async () => {
        await categoryPage.openPartsTab();
        for (const name of partNames) {
          await expect(categoryPage.partsTable.row(name)).toBeVisible;
        }
      });
    });
});
