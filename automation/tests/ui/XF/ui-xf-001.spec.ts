// case: test-cases/Cross_Functional_Scenarios/cross-functional-scenarios.md (UI-XF-001)
import { test, expect } from '../../../fixtures';

test.use({ user: 'allaccess' });

test.describe('Cross-functional scenarios', () => {
  test(
    'UI-XF-001: A part created from the Parts view, with a parameter and a stock item, shows its stock level in the category part list and its parameter value in the parametric view.',
    { tag: ['@smoke', '@regression', '@cross-functional'] },
    async ({ app, partsPage, partForm, partDetail, parameterForm, stockItemForm, data }) => {
      const category = await data.category(data.name('Category'));
      const categoryName = String(category.name);
      const template = await data.parameterTemplate(data.name('Series'));
      const templateName = String(template.name);
      const partName = data.trackPart(data.name('Resistor'));
      const description = 'XF flow part';
      let partId = 0;

      await test.step('1. Open the Add Parts dropdown above the parts table', async () => {
        await partsPage.open();
        await partsPage.addPartsMenu.button.click();
        await expect(partsPage.addPartsMenu.item('Create Part')).toBeVisible();
        await expect(partsPage.addPartsMenu.item('Import from File')).toBeVisible();
      });

      await test.step('2. Select Create Part', async () => {
        await partsPage.addPartsMenu.item('Create Part').click();
        await expect(partForm.root).toBeVisible();
        await partForm.waitUntilOpen();
      });

      await test.step('3. Fill in the form', async () => {
        await partForm.fill({ name: partName, description, category: categoryName });
        await expect(partForm.textField('name')).toHaveValue(partName);
        await expect(partForm.textField('description')).toHaveValue(description);
        await expect(partForm.categoryField).toHaveValue(categoryName);
        await expect(partForm.form.invalidFields).toHaveCount(0);
        await expect(partForm.form.formError).toHaveCount(0);
        await expect(partForm.textField('name')).toHaveJSProperty('required', true);
        await expect(partForm.form.requiredMarks).toHaveCount(1);
      });

      await test.step('4. Press Submit', async () => {
        await partForm.submit();
        await expect(partForm.root).toBeHidden();
        partId = await partDetail.currentPartId();
        await expect(partDetail.title).toHaveText(`Part: ${partName}`);
      });

      await test.step('5. Open the Parameters tab, open the Add Parameters menu, select Create Parameter, choose the template and enter the data, then press Submit', async () => {
        await partDetail.openTab('Parameters');
        await partDetail.addParameter('Create Parameter');
        await expect(parameterForm.templateLabel).toBeVisible();
        await expect(parameterForm.dataField).toHaveJSProperty('required', true);
        await parameterForm.fill({ template: templateName, data: 'E96' });
        await expect(parameterForm.template.selectedValue).toContainText(templateName);
        await expect(parameterForm.dataField).toHaveValue('E96');
        await expect(parameterForm.form.invalidFields).toHaveCount(0);
        await parameterForm.submit();
        await expect(partDetail.parametersTable.row(templateName)).toBeVisible();
        await expect(partDetail.parametersTable.cell(templateName, 'E96')).toBeVisible();
      });

      await test.step('6. Open the Stock tab, press the add stock item button, enter the quantity and press Submit', async () => {
        await partDetail.openTab('Stock');
        await partDetail.addStockItem();
        await expect(stockItemForm.root).toContainText('Add Stock Item');
        await expect(stockItemForm.part.selectedValue).toContainText(partName);
        await stockItemForm.fillQuantity('25');
        await expect(stockItemForm.quantityField).toHaveValue('25');
        await stockItemForm.submit();
        await expect(app.notifications.withText('Stock item created')).toBeVisible();
        await expect(app.page).toHaveURL(/\/web\/stock\/item\/\d+/);
      });

      await test.step('7. Open the part again and its Stock tab', async () => {
        await partDetail.open(partId);
        await partDetail.openTab('Stock');
        // CASE DEFECT: step 7 expects a location but the case gives no value, and the item has none (the cell shows "-").
        // Only the column is asserted until the architect states the expected location in the case.
        await expect(partDetail.stockTable.columnHeader('Location')).toBeVisible();
        await expect(partDetail.stockTable.cell(partName, '25')).toBeVisible();
        await expect(partDetail.stockTable.cell(partName, 'OK')).toBeVisible();
        await expect(partDetail.stockSummary).toHaveText('In Stock: 25');
      });

      await test.step('8. Check the breadcrumb at the top of the part page', async () => {
        await expect(app.breadcrumbs).toHaveText(['Parts', categoryName]);
      });

      await test.step('9. Click the category in the breadcrumb, then open the category\'s Parts tab', async () => {
        await app.openBreadcrumb(categoryName);
        await partsPage.partsTab.click();
        await expect(partsPage.partsTab).toHaveAttribute('aria-selected', 'true');
        await expect(partsPage.partsTable.row(partName)).toBeVisible();
        await expect(partsPage.partsTable.cell(partName, description)).toBeVisible();
        await expect(partsPage.partsTable.cell(partName, categoryName)).toBeVisible();
        await expect(partsPage.partsTable.cell(partName, '25')).toBeVisible();
      });

      await test.step('10. Switch the table to the parametric view with the Parametric View toggle above it', async () => {
        await partsPage.switchView('parametric');
        await expect(partsPage.viewToggle('table')).not.toBeChecked();
        await expect(partsPage.partsTable.columnHeader('Description')).toBeHidden();
        await expect(partsPage.partsTable.columnHeader(templateName)).toBeVisible();
        await expect(partsPage.partsTable.row(partName)).toBeVisible();
        await expect(partsPage.partsTable.cell(partName, '25')).toBeVisible();
        await expect(partsPage.partsTable.cell(partName, 'E96')).toBeVisible();
      });

      await test.step('11. Switch back to the table view and click the part name', async () => {
        await partsPage.switchView('table');
        await expect(partsPage.partsTable.columnHeader('Description')).toBeVisible();
        await partsPage.openPart(partName);
        await expect(partDetail.title).toHaveText(`Part: ${partName}`);
        await partDetail.expectOpen(partId);
      });
    },
  );
});
