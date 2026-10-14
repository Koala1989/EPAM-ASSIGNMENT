import { Locator, Page, expect } from '@playwright/test';
import { FormComponent } from './components/form.component';
import { SelectComponent } from './components/select.component';

export type PartFields = {
  name?: string;
  category?: string;
  ipn?: string;
  description?: string;
  revision?: string;
  revisionOf?: string;
  variantOf?: string;
  keywords?: string;
  units?: string;
  link?: string;
};

export type PartFlag =
  | 'component'
  | 'assembly'
  | 'is_template'
  | 'testable'
  | 'trackable'
  | 'purchaseable'
  | 'salable'
  | 'virtual'
  | 'consumable'
  | 'locked'
  | 'active';

export type SupplierFields = { supplier?: string; sku?: string; manufacturer?: string; mpn?: string };

const TEXT_FIELDS: [keyof PartFields, string][] = [
  ['name', 'name'],
  ['ipn', 'IPN'],
  ['description', 'description'],
  ['revision', 'revision'],
  ['keywords', 'keywords'],
  ['units', 'units'],
  ['link', 'link'],
];

/** The Add Part (Create Part) and Duplicate Part forms. */
export class PartFormPage {
  readonly form: FormComponent;
  readonly root: Locator;
  readonly supplierSection: Locator;

  constructor(page: Page) {
    this.form = new FormComponent(page);
    this.root = this.form.root;
    this.supplierSection = this.form.section('Supplier Information');
  }

  get revisionOf(): SelectComponent {
    return this.form.select('related', 'revision_of');
  }

  get variantOf(): SelectComponent {
    return this.form.select('related', 'variant_of');
  }

  async waitUntilOpen() {
    await expect(this.form.submitButton).toBeVisible();
  }

  textField(name: keyof PartFields): Locator {
    const apiName = TEXT_FIELDS.find(([key]) => key === name)?.[1] ?? name;
    return this.form.field('text', apiName);
  }

  async fill(fields: PartFields) {
    for (const [key, apiName] of TEXT_FIELDS) {
      const value = fields[key];
      if (value !== undefined) await this.form.fillText(apiName, value);
    }
    if (fields.category !== undefined) await this.form.select('tree', 'category').select(fields.category);
    if (fields.revisionOf !== undefined) await this.revisionOf.select(fields.revisionOf);
    if (fields.variantOf !== undefined) await this.variantOf.select(fields.variantOf);
  }

  flag(name: PartFlag): Locator {
    return this.form.field('boolean', name);
  }

  async setFlag(name: PartFlag, on: boolean) {
    await this.form.setSwitch(name, on);
  }

  supplierField(name: keyof SupplierFields): Locator {
    return name === 'supplier' || name === 'manufacturer'
      ? this.form.field('related', `initial_supplier.${name}`)
      : this.form.field('text', `initial_supplier.${name}`);
  }

  async fillSupplier(fields: SupplierFields) {
    if (fields.supplier !== undefined)
      await this.form.select('related', 'initial_supplier.supplier').select(fields.supplier);
    if (fields.sku !== undefined) await this.form.fillText('initial_supplier.sku', fields.sku);
    if (fields.manufacturer !== undefined)
      await this.form.select('related', 'initial_supplier.manufacturer').select(fields.manufacturer);
    if (fields.mpn !== undefined) await this.form.fillText('initial_supplier.mpn', fields.mpn);
  }

  async submit() {
    await this.form.submit();
  }

  async cancel() {
    await this.form.cancel();
  }
}
