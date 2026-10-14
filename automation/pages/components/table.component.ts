import { Locator } from '@playwright/test';

/** InvenTree data tables: search box `table-search-input`, refresh `table-refresh`, rows with `row-action-menu-<n>`. */
export class TableComponent {
  readonly searchInput: Locator;
  readonly refreshButton: Locator;
  readonly rows: Locator;

  constructor(readonly root: Locator) {
    this.searchInput = root.getByRole('textbox', { name: 'table-search-input' });
    this.refreshButton = root.getByRole('button', { name: 'table-refresh' });
    this.rows = root.getByRole('row');
  }

  async search(text: string) {
    await this.searchInput.fill(text);
  }

  row(text: string): Locator {
    return this.rows.filter({ hasText: text });
  }
}
