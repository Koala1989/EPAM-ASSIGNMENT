import { Locator, Page } from '@playwright/test';
import { slug } from '../../utils/names';

/**
 * InvenTree action menus: the button is `action-menu-<menu>`, each item `action-menu-<menu>-<item>`,
 * e.g. `action-menu-add-parts` → `action-menu-add-parts-create-part`.
 */
export class ActionsMenuComponent {
  readonly button: Locator;

  constructor(
    private readonly page: Page,
    private readonly menu: string,
  ) {
    this.button = page.getByRole('button', { name: `action-menu-${menu}` });
  }

  item(label: string): Locator {
    return this.page.getByRole('menuitem', { name: `action-menu-${this.menu}-${slug(label)}` });
  }

  async choose(label: string) {
    await this.button.click();
    await this.item(label).click();
  }
}
