import { Locator, Page, expect } from '@playwright/test';
import { BasePage } from './base.page';
import { TableComponent } from './components/table.component';
import { ActionsMenuComponent } from './components/actions-menu.component';

export type AddPartsOption = 'Create Part' | 'Import from File';

/** The Parts view: Part Categories and Parts panels, the parts table and the Add Parts menu. */
export class PartsPage extends BasePage {
  readonly partsTab: Locator;
  readonly categoriesTab: Locator;
  readonly partsTable: TableComponent;
  readonly addPartsMenu: ActionsMenuComponent;

  constructor(page: Page) {
    super(page);
    this.partsTab = this.panelTab('partcategory', 'Parts');
    this.categoriesTab = this.panelTab('partcategory', 'Part Categories');
    this.partsTable = new TableComponent(this.panel('Parts'));
    this.addPartsMenu = this.actionsMenu('add-parts');
  }

  /** Opens the Parts panel of the top-level Parts view (/web/part/ itself lands on Part Categories). */
  async open() {
    await this.goto('/web/part/category/index/parts');
    await expect(this.partsTable.searchInput).toBeVisible();
  }

  /** Opens the Parts panel of one category. */
  async openCategory(categoryId: number) {
    await this.goto(`/web/part/category/${categoryId}/parts`);
    await expect(this.partsTable.searchInput).toBeVisible();
  }

  async addParts(option: AddPartsOption) {
    await this.addPartsMenu.choose(option);
  }

  async searchParts(text: string) {
    await this.partsTable.search(text);
  }
}
