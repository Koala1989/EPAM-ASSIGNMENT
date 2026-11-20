// case: test-cases/Categories/category-hierarchy-and-filtering.md (UI-Categories-012)
import { test, expect } from '../../../fixtures';

test.use({ user: 'engineer' });

test.describe('Category hierarchy and filtering', () => {
  test('UI-Categories-012: A part in the deepest category appears in the top category\'s list', { tag: ['@regression'] },
    async ({ partsPage, categoryPage, data }) => {
      const topName = data.name('Top');
      const midName = data.name('Mid');
      const leafName = data.name('Leaf');
      const deepName = data.name('Deep');
      const partName = data.name('Part Deep');

      const top = await data.category(topName);
      const mid = await data.category(midName, { parent: top.pk });
      const leaf = await data.category(leafName, { parent: mid.pk });
      const deep = await data.category(deepName, { parent: leaf.pk });
      await data.category(data.name('Sibling'), { parent: top.pk });
      await data.category(data.name('Empty'), { parent: top.pk });
      await data.part(data.name('Part Top'), { category: top.pk });
      await data.part(data.name('Part Mid'), { category: mid.pk });
      await data.part(data.name('Part Leaf'), { category: leaf.pk });
      await data.part(partName, { category: deep.pk });
      await data.part(data.name('Part Sib'), { category: top.pk });

      await partsPage.openCategories();

      await test.step('1. Open the top category and read the part list', async () => {
        await partsPage.openCategoryByName(topName);
        await categoryPage.openPartsTab();
        await expect(categoryPage.partsTable.row(partName)).toBeVisible();
      });

      await test.step('2. Open the deepest category through the hierarchy and read the part list', async () => {
        await categoryPage.subcategoriesTab.click();
        await categoryPage.openSubcategory(midName);
        await categoryPage.openSubcategory(leafName);
        await categoryPage.openSubcategory(deepName);
        await categoryPage.openPartsTab();
        await expect(categoryPage.partsTable.row(partName)).toBeVisible();
      });
    });
});
