import { Locator, Page } from '@playwright/test';

/** Pop-up notifications (role alert), e.g. "Login successful". */
export class NotificationComponent {
  constructor(private readonly page: Page) {}

  withText(text: string | RegExp): Locator {
    return this.page.getByRole('alert').filter({ hasText: text });
  }
}
