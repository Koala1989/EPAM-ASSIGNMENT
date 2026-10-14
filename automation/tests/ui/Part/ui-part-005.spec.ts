// case: test-cases/Part_Creation_and_Import/part-creation-flow.md (UI-Part-005)
import { test, expect } from '../../../fixtures';

test.use({ user: 'engineer' });

test.describe('Part creation flow', () => {
  test('UI-Part-005: Supplier Information section shows only while Purchaseable is checked',
    { tag: ['@regression', '@settings'] },
    async ({ partsPage, partForm, data }) => {
      await data.setSetting('PART_PURCHASEABLE', true);
      await data.setSetting('PART_CREATE_SUPPLIER', true);

      // Pre-steps: open the Parts view, then Add Parts > Create Part.
      await partsPage.open();
      await partsPage.addParts('Create Part');
      await expect(partForm.root).toBeVisible();

      await test.step('1. Check the Purchaseable option and the form sections', async () => {
        await expect(partForm.flag('purchaseable')).toBeChecked();
        await expect(partForm.supplierSection).toBeVisible();
        await expect(partForm.supplierField('supplier')).toBeVisible();
        await expect(partForm.supplierField('sku')).toBeVisible();
        await expect(partForm.supplierField('manufacturer')).toBeVisible();
        await expect(partForm.supplierField('mpn')).toBeVisible();
      });

      await test.step('2. Uncheck Purchaseable', async () => {
        await partForm.setFlag('purchaseable', false);
        await expect(partForm.flag('purchaseable')).not.toBeChecked();
        await expect(partForm.supplierSection).toBeHidden();
      });

      await test.step('3. Check Purchaseable again', async () => {
        await partForm.setFlag('purchaseable', true);
        await expect(partForm.flag('purchaseable')).toBeChecked();
        await expect(partForm.supplierSection).toBeVisible();
      });

      // Postcondition: the form is closed without submitting.
      await partForm.cancel();
      await expect(partForm.root).toBeHidden();
    });
});
