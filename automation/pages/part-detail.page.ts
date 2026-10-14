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

  constructor(page: Page) {
    super(page);
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
    return Number(/\/web\/part\/(\d+)\//.exec(this.page.url())![1]);
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

  /** Switches to another revision of this part with the revision selector, e.g. selectRevision('B'). */
  async selectRevision(revision: string) {
    await this.revisionSelect.choose(`| ${revision}`);
  }

  async chooseAction(action: PartAction) {
    await this.partActions.choose(action);
  }
}
