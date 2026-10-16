import { Locator, Page, expect } from '@playwright/test';
import { BasePage } from './base.page';
import { ActionsMenuComponent } from './components/actions-menu.component';
import { SelectComponent } from './components/select.component';
import { TableComponent } from './components/table.component';

export type PartAction = 'Duplicate' | 'Edit' | 'Delete';

/** A part's detail page: header, panel tabs (Part Details, Stock, Suppliers, ...), actions menu, revision selector. */
export class PartDetailPage extends BasePage {
  /** Header line "Part: <display name>", e.g. "Part: ENCAB | Encabulator | A". */
  readonly title: Locator;
  readonly detailsPanel: Locator;
  readonly partActions: ActionsMenuComponent;
  readonly revisionSelect: SelectComponent;
  /** Supplier parts table in the Suppliers tab (accordion section "Suppliers"). */
  readonly supplierPartsTable: TableComponent;
  /** Manufacturer parts table in the Suppliers tab (accordion section "Manufacturers"). */
  readonly manufacturerPartsTable: TableComponent;

  /** Header stock summary, e.g. "In Stock: 25". */
  readonly stockSummary: Locator;
  /** Parameters tab: the parameters table. */
  readonly parametersTable: TableComponent;
  /** Parameters tab: the Add Parameters menu. */
  readonly addParametersMenu: ActionsMenuComponent;
  /** Stock tab: the stock items table. */
  readonly stockTable: TableComponent;
  /** Stock tab: the add stock item button. */
  readonly addStockItemButton: Locator;

  constructor(page: Page) {
    super(page);
    this.stockSummary = page.getByText(/^In Stock: /);
    this.parametersTable = new TableComponent(this.panel('Parameters'));
    this.addParametersMenu = this.actionsMenu('add-parameters');
    this.stockTable = new TableComponent(this.panel('Stock'));
    this.addStockItemButton = page.getByRole('button', { name: 'action-button-add-stock-item' });
    this.title = page.getByText(/^Part: /);
    this.detailsPanel = this.panel('Part Details');
    this.partActions = this.actionsMenu('part-actions');
    this.revisionSelect = new SelectComponent(page, page.getByRole('combobox', { name: 'part-revision-select' }));
    this.supplierPartsTable = new TableComponent(this.accordionSection('Suppliers'));
    this.manufacturerPartsTable = new TableComponent(this.accordionSection('Manufacturers'));
  }

  async open(partId: number) {
    await this.goto(`/web/part/${partId}/details`);
    await expect(this.title).toBeVisible();
  }

  /** Waits until the browser is on a part detail page and returns that part's ID. */
  async currentPartId(): Promise<number> {
    await expect(this.page).toHaveURL(/\/web\/part\/\d+\//);
    const match = /\/web\/part\/(\d+)\//.exec(this.page.url());
    if (!match) throw new Error(`Not on a part detail page: ${this.page.url()}`);
    return Number(match[1]);
  }

  /** Waits until the browser is on this part's detail page. */
  async expectOpen(partId: number) {
    await expect(this.page).toHaveURL(new RegExp(`/web/part/${partId}/`));
  }

  /** The content region of an accordion item inside the Suppliers tab, found by its header button's name. */
  private accordionSection(name: string): Locator {
    return this.panel('Suppliers').getByRole('region', { name, exact: true });
  }

  tab(name: string): Locator {
    return this.panelTab('part', name);
  }

  async openTab(name: string) {
    await this.tab(name).click();
    await expect(this.panel(name)).toBeVisible();
  }

  /** Value cell of a row in the Part Details panel, by its label, e.g. detail('IPN'). Rows are: label, value, copy button. */
  detail(label: string): Locator {
    return this.detailsPanel
      .getByRole('row')
      .filter({ has: this.page.getByRole('cell', { name: label, exact: true }) })
      .getByRole('cell')
      .nth(1);
  }

  /** Parameters tab: opens the Add Parameters menu and selects an option, e.g. addParameter('Create Parameter'). */
  async addParameter(option: 'Create Parameter' | 'Import from File') {
    await this.addParametersMenu.choose(option);
    await expect(this.form().submitButton).toBeVisible();
  }

  /** Stock tab: presses the add stock item button and waits for the Add Stock Item form. */
  async addStockItem() {
    await this.addStockItemButton.click();
    await expect(this.form().submitButton).toBeVisible();
  }

  /** Switches to another revision of this part with the revision selector, e.g. selectRevision('B'). */
  async selectRevision(revision: string) {
    await this.revisionSelect.choose(`| ${revision}`);
  }

  async chooseAction(action: PartAction) {
    await this.partActions.choose(action);
  }
}
