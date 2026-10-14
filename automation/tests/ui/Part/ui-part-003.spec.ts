// case: test-cases/Part_Creation_and_Import/part-creation-flow.md (UI-Part-003)
import { test, expect } from '../../../fixtures';

test.use({ user: 'reader' });

test.describe('Part creation flow', () => {
  test('UI-Part-003: Add Parts menu is not available without create permission', { tag: ['@regression', '@permissions'] },
    async ({ partsPage }) => {
      await test.step('1. Open the Parts view', async () => {
        await partsPage.open();
        await expect(partsPage.partsTable.searchInput).toBeVisible();
      });

      await test.step('2. Look above the parts table for the Add Parts dropdown', async () => {
        await expect(partsPage.addPartsMenu.button).toHaveCount(0);
      });
    });
});
