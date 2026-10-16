import { Locator, Page, expect } from '@playwright/test';
import { FormComponent } from './components/form.component';
import { SelectComponent } from './components/select.component';

/** The Add Parameter form of a part's Parameters tab. */
export class ParameterFormPage {
  readonly form: FormComponent;
  readonly root: Locator;
  /** The Template label; InvenTree appends " *" to the label of a required field. */
  readonly templateLabel: Locator;
  /** The Data text field (a required field is also marked required on the input). */
  readonly dataField: Locator;

  constructor(page: Page) {
    this.form = new FormComponent(page);
    this.root = this.form.root;
    this.templateLabel = this.root.getByText('Template *', { exact: true });
    this.dataField = this.form.field('text', 'data');
  }

  /** The Template dropdown; its selectedValue shows the chosen template. */
  get template(): SelectComponent {
    return this.form.select('related', 'template');
  }

  async waitUntilOpen() {
    await expect(this.form.submitButton).toBeVisible();
  }

  /** Chooses the template and enters the data. */
  async fill(fields: { template?: string; data?: string }) {
    if (fields.template !== undefined) await this.template.select(fields.template);
    if (fields.data !== undefined) await this.form.fillText('data', fields.data);
  }

  async submit() {
    await this.form.submit();
    await expect(this.root).toBeHidden();
  }
}
