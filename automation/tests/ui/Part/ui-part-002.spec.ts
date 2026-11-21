// case: test-cases/Part_Creation_and_Import/part-creation-flow.md (UI-Part-002)
import { test, expect } from '../../../fixtures';

test.use({ user: 'engineer' });

test.describe('Part creation flow', () => {
  test('UI-Part-002: Add Parts dropdown offers create and import options', { tag: ['@smoke', '@regression'] },
    async ({ partsPage }) => {
      await test.step('1. Open the Parts view', async () => {
        await partsPage.open();
        await expect(partsPage.partsTable.searchInput).toBeVisible();
        await expect(partsPage.addPartsMenu.button).toBeVisible();
      });

      await test.step('2. Open the Add Parts dropdown', async () => {
        await partsPage.addPartsMenu.button.click();
        await expect(partsPage.addPartsMenu.item('Create Part')).toBeVisible();
        await expect(partsPage.addPartsMenu.item('Import from File')).toBeVisible();
      });

      // TEMPORARY (2026-11-21): deliberate failure to check that Jenkins keeps the video, trace and screenshot of a
      // failed test. Not part of the case. Remove this step after the check.
      await test.step('TEMPORARY: deliberate failure (CI artifact check)', async () => {
        await expect(partsPage.addPartsMenu.item('Deliberate failure: no such option'),
          'Deliberate failure to check CI artifacts').toBeVisible({ timeout: 5_000 });
      });
    });
});
