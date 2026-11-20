// case: test-cases/Attributes/part-attributes.md (UI-ATT-013)
import { test, expect } from '../../../fixtures';

test.use({ user: 'engineer' });

test.describe('Part attributes', () => {
  test('UI-ATT-013: An Assembly part has a BOM to which a Component part can be added', { tag: ['@smoke', '@regression'] },
    async ({ partDetail, bomItemForm, data }) => {
      const assemblyName = data.name('Assembly Main');
      const componentName = data.name('Component One');
      const assembly = await data.part(assemblyName, { description: assemblyName, assembly: true });
      const component = await data.part(componentName, { description: componentName, component: true });

      await partDetail.open(Number(assembly.pk));
      await partDetail.openTab('Bill of Materials');

      await test.step('1. Add a BOM line.', async () => {
        await partDetail.addBomItem();
        await bomItemForm.fill({ component: componentName, quantity: '2' });
        await expect(bomItemForm.component.selectedValue).toContainText(componentName);
        await expect(bomItemForm.quantityField).toHaveValue('2');
        await bomItemForm.submit();
        await expect(bomItemForm.root).toBeHidden();
      });

      await test.step('2. Check the BOM table.', async () => {
        await expect(partDetail.bomTable.row(componentName)).toBeVisible();
        await expect(partDetail.bomTable.cell(componentName, '2')).toBeVisible();
      });

      await test.step("3. Open the Component part's Used In tab.", async () => {
        await partDetail.open(Number(component.pk));
        await partDetail.openTab('Used In');
        await expect(partDetail.usedInTable.row(assemblyName)).toBeVisible();
      });
    });
});
