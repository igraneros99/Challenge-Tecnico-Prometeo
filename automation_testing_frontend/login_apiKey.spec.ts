import { test } from '@playwright/test';
import { allure } from 'allure-playwright';
import { LoginPage } from './pages/LoginPage';
import { DashboardPage } from './pages/DashboardPage';
import { credentials } from './config/env';

test.describe('Login y validacion de API Key', () => {
  let loginPage: LoginPage;
  let dashboardPage: DashboardPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    dashboardPage = new DashboardPage(page);

    await loginPage.goto();
    await loginPage.login(credentials.email, credentials.password);
  });

  test('Successful login with valid credentials', async ({ page }) => {
    allure.epic('Auth/Nav');
    allure.feature('Login');
    allure.story('Happy Path: Login');
    allure.owner('ignacio.graneros');
    allure.severity('critical');
    allure.label('testType', 'E2E');

    await allure.attachment('Screenshot: credenciales login', await page.screenshot(), 'image/png');
  });

  test('API Key is displayed after login', async ({ page }) => {
    allure.epic('Nav/Val');
    allure.feature('Dashboard API Key');
    allure.story('Happy path: API Key is displayed after the login');
    allure.owner('ignacio.graneros');
    allure.severity('critical');
    allure.label('testType', 'E2E');

    await test.step('Ir a Sandbox API Keys', async () => {
      await dashboardPage.goToSandboxKeys();
      await allure.attachment('Screenshot: Texto de sandbox keys', await page.screenshot(), 'image/png');
    });

    await test.step('Verificar visibilidad de API Key', async () => {
      await dashboardPage.assertAPIKeyVisible();
      await allure.attachment('Screenshot: asercion de que el API Key es visible', await page.screenshot(), 'image/png');
    });

    await test.step('Verificar valor correcto de API Key', async () => {
      await dashboardPage.assertAPIKeyValue(credentials.apiKey);
      await allure.attachment('API Key Validada', await page.screenshot(), 'image/png');
    });
  });
});
