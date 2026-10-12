// case: test-cases/Part/part-creation-flow.md (UI-Part-004)
import { test, expect } from '../../fixtures';

test.use({ user: 'engineer' });

test.describe('Part creation flow', () => {
  test('UI-Part-004: Create a part with optional IPN, Keywords and Link filled', { tag: ['@regression'] },
    async ({ partsPage, partForm, partDetail, data }) => {
      const category = await data.category(data.name('Category'));
      const partName = data.trackPart(data.name('Capacitor 100n'));
      // data.name gives "QA-<8 hex> <label>"; the case's <suffix> is the part after "QA-".
      const suffix = partName.split(' ')[0].replace('QA-', '');
      const ipn = `QA-${suffix}-IPN1`;
      const keywords = `qa${suffix}cap ceramic`;
      const link = 'https://example.com/datasheet';

      // Pre-steps: open the Parts view, then Add Parts > Create Part.
      await partsPage.open();
      await partsPage.addParts('Create Part');
      await expect(partForm.root).toBeVisible();

      await test.step('1. Fill in Name, Category and the optional fields', async () => {
        await partForm.fill({ name: partName, category: String(category.name), ipn, keywords, link });
        await expect(partForm.textField('name')).toHaveValue(partName);
        await expect(partForm.textField('ipn')).toHaveValue(ipn);
        await expect(partForm.textField('keywords')).toHaveValue(keywords);
        await expect(partForm.textField('link')).toHaveValue(link);
        await expect(partForm.form.invalidFields).toHaveCount(0);
        await expect(partForm.form.formError).toBeHidden();
      });

      await test.step('2. Press Submit', async () => {
        await partForm.submit();
        await expect(partForm.root).toBeHidden();
        await partDetail.currentPartId();
      });

      await test.step('3. Check the part details', async () => {
        await expect(partDetail.detail('IPN')).toHaveText(ipn);
        await expect(partDetail.detail('Keywords')).toHaveText(keywords);
        await expect(partDetail.detail('Link')).toHaveText(link);
      });
    });
});
