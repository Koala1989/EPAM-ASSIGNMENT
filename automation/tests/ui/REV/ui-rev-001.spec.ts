// case: test-cases/Revisions/part-revisions.md (UI-REV-001)
import { test, expect } from '../../../fixtures';

test.use({ user: 'engineer' });

test.describe('Part revisions', () => {
  test('UI-REV-001: A template part cannot have a revision', { tag: ['@regression', '@settings'] },
    async ({ partsPage, partForm, partDetail, data }) => {
      await data.setSetting('PART_ENABLE_REVISION', true);
      const templateName = data.name('Template');
      const template = await data.part(templateName, { description: templateName, is_template: true, assembly: true });

      await test.step('1. Open the part actions menu and select Duplicate Part', async () => {
        await partDetail.open(template.pk);
        await partDetail.chooseAction('Duplicate');
        await expect(partForm.root).toBeVisible();
        await expect(partForm.duplicateSection).toBeVisible();
      });

      await test.step('2. Open the Revision Of field and search for the template part', async () => {
        const matching = await partForm.revisionOf.optionsMatching(templateName);
        await expect(partForm.revisionOf.input).toHaveValue(templateName);
        await expect(matching).toHaveCount(0);
      });

      await test.step('3. Cancel the form', async () => {
        await partForm.closeDropdown();
        await partForm.cancel();
        await expect(partForm.root).toBeHidden();
        expect(await data.findParts(templateName)).toHaveLength(1);
      });

      await test.step('4. Open the Parts view and search for the template name', async () => {
        await partsPage.open();
        await partsPage.searchParts(templateName);
        await expect(partsPage.partsTable.searchInput).toHaveValue(templateName);
        await expect(partsPage.partsTable.row(templateName)).toHaveCount(1);
      });
    });
});
