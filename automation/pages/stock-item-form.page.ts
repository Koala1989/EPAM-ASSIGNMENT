import { Locator, Page, expect } from '@playwright/test';
import { FormComponent } from './components/form.component';
import { SelectComponent } from './components/select.component';

/** The Add Stock Item form (opened from a part's Stock tab; the part is pre-filled). */
export class StockItemFormPage {
  readonly form: FormComponent;
  readonly root: Locator;
  /** The Stock Quantity field. */
  readonly quantityField: Locator;

  constructor(page: Page) {
    this.form = new FormComponent(page);
    this.root = this.form.root;
    this.quantityField = this.form.field('number', 'quantity');
  }

  async waitUntilOpen() {
    await expect(this.form.submitButton).toBeVisible();
  }

  /** Enters the stock quantity. */
  async fillQuantity(quantity: string) {
    await this.quantityField.fill(quantity);
  }

  /** The Part field; its selectedValue shows the part the item is added to. */
  get part(): SelectComponent {
    return this.form.select('related', 'part');
  }

  /** Presses Submit and waits for the dialog to close. */
  async submit() {
    await this.form.submit();
    await expect(this.root).toBeHidden();
  }
}
