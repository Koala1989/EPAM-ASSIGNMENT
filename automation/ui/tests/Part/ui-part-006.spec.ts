// case: test-cases/Part/part-creation-flow.md (UI-Part-006)
import { test, expect } from '../../fixtures';

test.use({ user: 'engineer' });

test.describe('Part creation flow', () => {
  test('UI-Part-006: Create a part with supplier and manufacturer data from the Supplier Information section',
    { tag: ['@regression', '@cross-functional', '@settings'] },
    async ({ partsPage, partForm, partDetail, data, switchUser }) => {
      await data.setSetting('PART_PURCHASEABLE', true);
      await data.setSetting('PART_CREATE_SUPPLIER', true);
      const category = await data.category(data.name('Category'));
      const supplier = await data.company(data.name('Supplier'), { is_supplier: true });
      const manufacturer = await data.company(data.name('Manufacturer'), { is_manufacturer: true, is_supplier: false });
      const partName = data.trackPart(data.name('Connector'));
      const sku = `QA-${data.suffix}-SKU1`;
      const mpn = `QA-${data.suffix}-MPN1`;

      // Pre-steps: open the Parts view, then Add Parts > Create Part.
      await partsPage.open();
      await partsPage.addParts('Create Part');
      await expect(partForm.root).toBeVisible();

      await test.step('1. Fill in Name and Category; leave Purchaseable checked', async () => {
        await partForm.fill({ name: partName, category: String(category.name) });
        await expect(partForm.flag('purchaseable')).toBeChecked();
        await expect(partForm.supplierSection).toBeVisible();
      });

      await test.step('2. Enter the supplier and manufacturer data in Supplier Information', async () => {
        await partForm.fillSupplier({
          supplier: String(supplier.name),
          sku,
          manufacturer: String(manufacturer.name),
          mpn,
        });
        await expect(partForm.supplierField('sku')).toHaveValue(sku);
        await expect(partForm.supplierField('mpn')).toHaveValue(mpn);
        await expect(partForm.form.invalidFields).toHaveCount(0);
      });

      let partId = 0;

      await test.step('3. Press Submit', async () => {
        await partForm.submit();
        await expect(partForm.root).toBeHidden();
        partId = await partDetail.currentPartId();
        await expect(partDetail.title).toContainText(partName);
      });

      await test.step('4. Log out, log in as allaccess, open the new part and its Suppliers tab', async () => {
        await switchUser('allaccess');
        await partDetail.open(partId);
        await partDetail.openTab('Suppliers');

        const supplierPart = partDetail.supplierPartsTable.row(sku);
        await expect(supplierPart).toHaveCount(1);
        await expect(supplierPart).toContainText(String(supplier.name));

        const manufacturerPart = partDetail.manufacturerPartsTable.row(mpn);
        await expect(manufacturerPart).toHaveCount(1);
        await expect(manufacturerPart).toContainText(String(manufacturer.name));
      });
    });
});
