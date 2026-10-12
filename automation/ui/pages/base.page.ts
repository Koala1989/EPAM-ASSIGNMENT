import { Locator, Page, expect } from '@playwright/test';
import { ActionsMenuComponent } from './components/actions-menu.component';
import { FormComponent } from './components/form.component';
import { NotificationComponent } from './components/notification.component';

/** What every InvenTree screen has: header navigation, notifications, forms, action menus and panel tabs. */
export class BasePage {
  readonly navigationMenu: Locator;
  readonly searchButton: Locator;
  readonly notificationsButton: Locator;
  readonly notifications: NotificationComponent;

  constructor(readonly page: Page) {
    this.navigationMenu = page.getByRole('button', { name: 'navigation-menu' });
    this.searchButton = page.getByRole('button', { name: 'open-search' });
    this.notificationsButton = page.getByRole('button', { name: 'open-notifications' });
    this.notifications = new NotificationComponent(page);
  }

  /** Opens a path of the web UI and waits until the app shell has rendered. */
  async goto(path: string) {
    await this.page.goto(path);
    await expect(this.navigationMenu).toBeVisible();
  }

  async openHome() {
    await this.goto('/web/home');
  }

  /** The user menu in the header; its accessible name is the logged-in user's display name. */
  userMenu(displayName: string): Locator {
    return this.page.getByRole('button', { name: displayName, exact: true });
  }

  /** Logs out through the user menu and waits for the login screen. */
  async logout(displayName: string) {
    await this.userMenu(displayName).click();
    await this.page.getByRole('menuitem', { name: 'Logout' }).click();
    await expect(this.page.getByRole('textbox', { name: 'login-username' })).toBeVisible();
  }

  /** Top-level navigation tab, e.g. "Parts", "Stock". */
  navTab(name: string): Locator {
    return this.page.getByRole('tab', { name, exact: true }).filter({ has: this.page.getByRole('link', { name }) });
  }

  /** The open modal form. */
  form(): FormComponent {
    return new FormComponent(this.page);
  }

  actionsMenu(menu: string): ActionsMenuComponent {
    return new ActionsMenuComponent(this.page, menu);
  }

  /** A tab in a page's panel group, e.g. panelTab('part', 'Suppliers'). */
  panelTab(group: string, name: string): Locator {
    return this.page.getByRole('tablist', { name: `panel-tabs-${group}` }).getByRole('tab', { name, exact: true });
  }

  panel(name: string): Locator {
    return this.page.getByRole('tabpanel', { name, exact: true });
  }
}
