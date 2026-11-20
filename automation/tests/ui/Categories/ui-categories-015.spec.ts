// case: test-cases/Categories/category-hierarchy-and-filtering.md (UI-Categories-015)
import { test, expect } from '../../../fixtures';

test.use({ user: 'engineer' });

test.describe('Category hierarchy and filtering', () => {
  test('UI-Categories-015: What-if: a new part created in a sub-category appears in the parent category\'s list', { tag: ['@regression', '@cross-functional'] },
    async ({ partsPage, partForm, partDetail, categoryPage, data }) => {
      const topName = data.name('Top');
      const midName = data.name('Mid');
      const leafName = data.name('Leaf');
      const partName = data.trackPart(data.name('Part New'));

      const top = await data.category(topName);
      const mid = await data.category(midName, { parent: top.pk });
      const leaf = await data.category(leafName, { parent: mid.pk });
      await data.category(data.name('Deep'), { parent: leaf.pk });
      await data.category(data.name('Sibling'), { parent: top.pk });
      await data.category(data.name('Empty'), { parent: top.pk });
      await data.part(data.name('Part Top'), { category: top.pk });
      await data.part(data.name('Part Mid'), { category: mid.pk });
      await data.part(data.name('Part Leaf'), { category: leaf.pk });

      await partsPage.open();

      await test.step('1. Open the Add Parts dropdown and select Create Part', async () => {
        await partsPage.addParts('Create Part');
        await expect(partForm.root).toBeVisible();
      });

      await test.step('2. Fill in the form and submit', async () => {
        await partForm.fill({ name: partName, description: 'New part', category: leafName });
        await expect(partForm.textField('name')).toHaveValue(partName);
        await expect(partForm.textField('description')).toHaveValue('New part');
        await expect(partForm.categoryField).toHaveValue(new RegExp(`(^|/)${leafName}$`));
        await partForm.submit();
        await expect(partForm.root).toBeHidden();
        await expect(partDetail.detail('Name')).toHaveText(partName);
      });

      await test.step('3. Open Top and read its part list', async () => {
        await partsPage.openCategories();
        await partsPage.openCategoryByName(topName);
        await categoryPage.openPartsTab();
        await expect(categoryPage.partsTable.row(partName)).toBeVisible();
      });

      await test.step('4. Open Mid and read its part list', async () => {
        await categoryPage.subcategoriesTab.click();
        await categoryPage.openSubcategory(midName);
        await categoryPage.openPartsTab();
        await expect(categoryPage.partsTable.row(partName)).toBeVisible();
      });
    });
});
