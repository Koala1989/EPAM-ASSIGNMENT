// case: test-cases/Part_Creation_and_Import/part-creation-flow.md (UI-Part-001)
import { test, expect } from '../../../fixtures';

test.use({ user: 'engineer' });

test.describe('Part creation flow', () => {
  test('UI-Part-001: Create a part with only the required fields', { tag: ['@smoke', '@regression'] },
    async ({ partsPage, partForm, partDetail, data }) => {
      const category = await data.category(data.name('Category'));
      const partName = data.trackPart(data.name('Resistor 10k'));

      await test.step('1. Open the Add Parts dropdown above the parts table and select Create Part', async () => {
        await partsPage.open();
        await partsPage.addParts('Create Part');
        await expect(partForm.root).toBeVisible();
      });

      await test.step('2. Fill in the required field and the category only; leave IPN empty', async () => {
        await partForm.fill({ name: partName, category: String(category.name) });
        await expect(partForm.textField('name')).toHaveValue(partName);
        await expect(partForm.categoryField).toHaveValue(String(category.name));
        await expect(partForm.textField('ipn')).toHaveValue('');
        await expect(partForm.form.invalidFields).toHaveCount(0);
      });

      await test.step('3. Press Submit', async () => {
        await partForm.submit();
        await expect(partForm.root).toBeHidden();
        await partDetail.currentPartId();
      });

      await test.step('4. Check the part details', async () => {
        await expect(partDetail.detail('Name')).toHaveText(partName);
        await expect(partDetail.detail('Category')).toContainText(String(category.name));
        // No "IPN" row is shown in the Part Details panel when IPN is empty.
        await expect(partDetail.detail('IPN')).toHaveCount(0);
      });
    });
});
