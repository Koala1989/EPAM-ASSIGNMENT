// case: test-cases/Part_Creation_and_Import/part-creation-required-fields.md (UI-Part-074)
import { test, expect } from '../../../fixtures';

test.use({ user: 'engineer' });

test.describe('Part creation: required fields', () => {
  test('UI-Part-074: Create a part with Name only', { tag: ['@smoke', '@regression'] },
    async ({ partsPage, partForm, partDetail, data }) => {
      const partName = data.trackPart(data.name('MinPart'));

      await partsPage.open();
      await partsPage.addParts('Create Part');
      await partForm.waitUntilOpen();

      await test.step('1. Fill in Name only. Leave Category, IPN, Description, Revision, Keywords and Link empty.', async () => {
        await partForm.fill({ name: partName });
        await expect(partForm.textField('name')).toHaveValue(partName);
      });

      await test.step('2. Press Submit', async () => {
        await partForm.submit();
        // The detail page opening shows the form was accepted: no form error.
        await partDetail.currentPartId();
        await expect(partForm.root).toBeHidden();
      });

      await test.step('3. Check the detail page header and details', async () => {
        await expect(partDetail.title).toContainText(partName);
        await expect(partDetail.detail('Name')).toHaveText(partName);
        
      });
    });
});
