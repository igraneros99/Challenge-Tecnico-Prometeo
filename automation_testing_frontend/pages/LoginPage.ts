import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.locator('#email');
    this.passwordInput = page.locator('#password');
    this.loginButton = page.getByRole('button', { name: /login/i });
  }

  async goto() {
    await this.page.goto('https://dashboard.prometeoapi.com/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.click();
    await this.page.keyboard.type(email);

    await this.passwordInput.click();
    await this.page.keyboard.type(password);

    await this.loginButton.click();
  }
}
