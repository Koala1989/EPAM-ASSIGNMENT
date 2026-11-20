// case: test-cases/Attributes/part-attributes.md (UI-ATT-066)
import { test, expect } from '../../../fixtures';

test.use({ user: 'engineer' });




test.describe('Part attributes', () => {
  test('UI-ATT-066: A newly created part is Active by default', { tag: ['@smoke', '@regression'] },
    async ({ partsPage, partForm, partDetail, data }) => {
      const partName = data.trackPart(data.name('Active Default'));

      await test.step('1. Open the Add Parts dropdown and select Create Part', async () => {
        await partsPage.open();
        await partsPage.addParts('Create Part');
        await expect(partForm.root).toBeVisible();
      });

      await test.step('2. Fill in the required field only and submit', async () => {
        await partForm.fill({ name: partName });
        await expect(partForm.textField('name')).toHaveValue(partName);
        await partForm.submit();
        await partDetail.currentPartId();
      });

      await test.step('3. Check the part\'s status', async () => {
        await expect(partDetail.detail('Active')).toHaveText(/yes/i);
      });
    });
});
