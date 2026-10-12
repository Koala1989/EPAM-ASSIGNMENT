import { Locator, Page } from '@playwright/test';
import { SelectComponent } from './select.component';

export type FieldKind = 'text' | 'number' | 'boolean' | 'related' | 'tree' | 'tags';

/**
 * InvenTree's modal forms. Fields are labelled `<kind>-field-<api field name>`, e.g.
 * `text-field-name`, `boolean-field-purchaseable`, `related-field-revision_of`, `tree-field-category`.
 * An invalid field has aria-invalid="true" and its error text in its accessible description.
 */
export class FormComponent {
  readonly root: Locator;
  readonly submitButton: Locator;
  readonly cancelButton: Locator;
  /** The form-level "Form Error" alert shown when any field is invalid. */
  readonly formError: Locator;
  /** All fields currently marked invalid. */
  readonly invalidFields: Locator;

  constructor(private readonly page: Page) {
    this.root = page.getByRole('dialog');
    this.submitButton = this.root.getByRole('button', { name: 'Submit' });
    this.cancelButton = this.root.getByRole('button', { name: 'Cancel' });
    this.formError = this.root.getByRole('alert').filter({ hasText: 'Form Error' });
    this.invalidFields = this.root.locator('[aria-invalid="true"]');
  }

  field(kind: FieldKind, name: string): Locator {
    if (kind === 'boolean') return this.root.getByRole('switch', { name: `boolean-field-${name}` });
    return this.root.getByLabel(`${kind}-field-${name}`, { exact: true });
  }

  select(kind: 'related' | 'tree', name: string): SelectComponent {
    return new SelectComponent(this.page, this.field(kind, name));
  }

  /** A collapsible section header, e.g. "Supplier Information". */
  section(title: string): Locator {
    return this.root.getByRole('button', { name: title });
  }

  async fillText(name: string, value: string) {
    await this.field('text', name).fill(value);
  }

  async setSwitch(name: string, on: boolean) {
    await this.field('boolean', name).setChecked(on);
  }

  async submit() {
    await this.submitButton.click();
  }

  async cancel() {
    await this.cancelButton.click();
  }
}
