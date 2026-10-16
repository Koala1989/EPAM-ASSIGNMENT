import { Locator, Page } from '@playwright/test';

/**
 * InvenTree's searchable dropdown fields: related-field-* (react-select, searched on the server
 * as you type) and tree-field-* (category and location pickers). Options carry no accessible
 * name, so they are matched by their visible text.
 */
export class SelectComponent {
  constructor(
    private readonly page: Page,
    readonly input: Locator,
  ) {}

  /** The control around the input; its text is the selected option (the input itself has no value). */
  get selectedValue(): Locator {
    // No role or label identifies the selected-value text; it lives two levels above the combobox input.
    return this.input.locator('xpath=../..');
  }

  /** Options currently offered in the open dropdown. */
  get options(): Locator {
    return this.page.getByRole('option');
  }

  /** Types the search text key by key (filling at once does not trigger the server search). */
  async search(text: string) {
    await this.input.click();
    await this.input.pressSequentially(text);
  }

  /** Searches for `text` and picks the first option whose text contains `optionText` (default: `text`). */
  async select(text: string, optionText = text) {
    await this.search(text);
    await this.options.filter({ hasText: optionText }).first().click();
  }

  /**
   * For read-only dropdowns (no search, e.g. the part revision selector): its input is a hidden
   * dummy that cannot be clicked, so it is opened from the keyboard.
   */
  async choose(optionText: string) {
    await this.input.focus();
    await this.input.press('ArrowDown');
    await this.options.filter({ hasText: optionText }).first().click();
  }

  /** Options whose text contains `optionText`, after searching for `text`. */
  async optionsMatching(text: string, optionText = text): Promise<Locator> {
    await this.search(text);
    return this.options.filter({ hasText: optionText });
  }
}
