// case: test-cases/Part_Creation_and_Import/part-creation-required-fields.md (UI-Part-074)
import { test, expect } from '../../../fixtures';

test.use({ user: 'engineer' });

test.describe('Part creation with only the required fields', () => {
  test('UI-Part-074: Create a part with Name only', { tag: ['@smoke', '@regression'] },
    async ({ partsPage, partForm, partDetail, data }) => {
      const partName = data.trackPart(data.name('MinPart'));

      await partsPage.open();
      await partsPage.addParts('Create Part');
      await partForm.waitUntilOpen();

      await test.step('1. Fill in Name only. Leave Category, IPN, Description, Revision, Keywords and Link empty.', async () => {
        await partForm.fill({ name: partName });
        await expect(partForm.textField('name')).toHaveValue(partName);
        await expect(partForm.form.formError).toHaveCount(0);
      });

      await test.step('2. Press Submit.', async () => {
        await partForm.submit();
        await partDetail.currentPartId();
        await expect(partForm.root).toBeHidden();
      });

      await test.step('3. Check the detail page header and details.', async () => {
        await expect(partDetail.title).toContainText(partName);
        await expect(partDetail.detail('Name')).toHaveText(partName);
        // Q-Part-23: how empty Category, IPN, Revision, Keywords, Link and Description are shown is not asserted.
      });
    });
});
