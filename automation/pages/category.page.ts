import { Locator, Page, expect } from '@playwright/test';
import { BasePage } from './base.page';
import { TableComponent } from './components/table.component';

/** One part category's page: Subcategories and Parts panels. */
export class CategoryPage extends BasePage {
  readonly subcategoriesTab: Locator;
  readonly partsTab: Locator;
  readonly subcategoriesTable: TableComponent;
  readonly partsTable: TableComponent;

  constructor(page: Page) {
    super(page);
    this.subcategoriesTab = this.panelTab('partcategory', 'Subcategories');
    this.partsTab = this.panelTab('partcategory', 'Parts');
    this.subcategoriesTable = new TableComponent(this.panel('Subcategories'));
    this.partsTable = new TableComponent(this.panel('Parts'));
  }

  /** Shows the Parts panel of the open category (includes parts of its subcategories) and waits for its table. */
  async openPartsTab() {
    await this.partsTab.click();
    await expect(this.partsTable.searchInput).toBeVisible();
  }

  /** Opens a direct subcategory by clicking its name in the Subcategories list and waits for its page. */
  async openSubcategory(name: string) {
    const before = this.page.url();
    // The Name cell is the first cell with this exact text (the Path cell of a top-level row repeats it).
    await this.subcategoriesTable.cell(name, name).first().click();
    await expect(this.page).not.toHaveURL(before);
    await expect(this.subcategoriesTable.searchInput).toBeVisible();
  }
}
