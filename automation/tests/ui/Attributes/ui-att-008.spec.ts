// case: test-cases/Attributes/part-attributes.md (UI-ATT-008)
import { test, expect } from '../../../fixtures';

test.use({ user: 'engineer' });

test.describe('Part attributes', () => {
  test('UI-ATT-008: A Virtual part behaves like a regular part: it can be edited and saved', { tag: ['@regression'] },
    async ({ partDetail, partForm, data }) => {
      const part = await data.part(data.name('Virtual Edit'), { description: 'Before', virtual: true });
      await partDetail.open(Number(part.pk));

      await test.step("1. Open the part's edit form.", async () => {
        await partDetail.chooseAction('Edit');
        await expect(partForm.root).toBeVisible();
      });

      await test.step('2. Change the description and submit.', async () => {
        await partForm.fill({ description: 'After edit' });
        await expect(partForm.textField('description')).toHaveValue('After edit');
        await partForm.submit();
        await expect(partForm.root).toBeHidden();
        await expect(partDetail.detail('Description')).toHaveText('After edit');
      });
    });
});
