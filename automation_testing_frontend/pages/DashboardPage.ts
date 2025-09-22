// dashboardpage.ts
import { Page, Locator, expect } from '@playwright/test';

export class DashboardPage {
  readonly page: Page;
  readonly sandboxSection: Locator;

  constructor(page: Page) {
    this.page = page;
    this.sandboxSection = page.getByText(
      'Sandbox private keys accessUse your API key and fictitious bank account details',
      { exact: false }
    );
  }

  async goToSandboxKeys() {
    await this.sandboxSection.waitFor({ timeout: 15000 });
    await this.sandboxSection.click();
  }

  async assertAPIKeyVisible() {
    await expect(
      this.page.getByText('Your Sandbox API Key is:', { exact: false })
    ).toBeVisible();
  }

  async assertAPIKeyValue(expectedKey: string) {
    const apiKeyElement = this.page.getByText(expectedKey, { exact: true });
    await expect(apiKeyElement).toBeVisible();
  }
}
