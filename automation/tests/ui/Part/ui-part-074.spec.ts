// case: test-cases/Part_Creation_and_Import/part-creation-required-fields.md (UI-Part-074)
import { test, expect } from '../../../fixtures';

test.use({ user: 'engineer' });

test.describe('Part creation: required fields', () => {
  test('UI-Part-074: Create a part with Name only', { tag: ['@smoke', '@regression'] },
    async ({ partsPage, partForm, partDetail, data }) => {
      const partName = data.trackPart(data.name('MinPart'));

      await partsPage.open();
      await partsPage.addParts('Create Part');
      await expect(partForm.root).toBeVisible();

      await test.step('1. Fill in Name only. Leave Category, IPN, Description, Revision, Keywords and Link empty.', async () => {
        await partForm.fill({ name: partName });
        await expect(partForm.textField('name')).toHaveValue(partName);
        await expect(partForm.categoryField).toHaveValue('');
        await expect(partForm.textField('ipn')).toHaveValue('');
        await expect(partForm.textField('description')).toHaveValue('');
        await expect(partForm.textField('revision')).toHaveValue('');
        await expect(partForm.textField('keywords')).toHaveValue('');
        await expect(partForm.textField('link')).toHaveValue('');
        await expect(partForm.form.invalidFields).toHaveCount(0);
        await expect(partForm.form.formError).toBeHidden();
      });

      await test.step('2. Press Submit.', async () => {
        await partForm.submit();
        await expect(partForm.root).toBeHidden();
        await partDetail.currentPartId();
      });

      await test.step('3. Check the detail page header and details.', async () => {
        await expect(partDetail.title).toContainText(partName);
        await expect(partDetail.detail('Name')).toHaveText(partName);
        // Q-Part-23 is open: how the page shows empty Category, IPN, Revision, Keywords, Link
        // and Description is not asserted. IPN, Revision and Keywords are not required: the part was created without them.
      });
    });
});
