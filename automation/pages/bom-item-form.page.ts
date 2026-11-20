import { Locator, Page, expect } from '@playwright/test';
import { FormComponent } from './components/form.component';
import { SelectComponent } from './components/select.component';

/** The Add BOM Item form of an assembly's Bill of Materials tab. */
export class BomItemFormPage {
  readonly form: FormComponent;
  readonly root: Locator;
  /** The Quantity text field (api field raw_amount). */
  readonly quantityField: Locator;

  constructor(page: Page) {
    this.form = new FormComponent(page);
    this.root = this.form.root;
    this.quantityField = this.form.field('text', 'raw_amount');
  }

  /** The Component (sub_part) dropdown; its selectedValue shows the chosen part. */
  get component(): SelectComponent {
    return this.form.select('related', 'sub_part');
  }

  /** Chooses the component part and enters the quantity. */
  async fill(fields: { component?: string; quantity?: string }) {
    if (fields.component !== undefined) await this.component.select(fields.component);
    if (fields.quantity !== undefined) await this.quantityField.fill(fields.quantity);
  }

  /** Submits the form and waits for it to close. */
  async submit() {
    await this.form.submit();
    await expect(this.root).toBeHidden();
  }
}
