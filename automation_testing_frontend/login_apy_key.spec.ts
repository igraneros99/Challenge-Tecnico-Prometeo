import { test, expect } from '@playwright/test';
import { allure } from 'allure-playwright';
import { LoginPage } from './pages/LoginPage';
import { DashboardPage } from './pages/DashboardPage';
import { credentials } from './config/env';

test.describe('Flujo de Login y validación de API Key', () => {
  test('Login exitoso y navegación a Sandbox API Keys', async ({ page }) => {
    allure.epic('Autenticación y Navegación');
    allure.feature('Dashboard API Key Visibility');
    allure.story('Login exitoso con credenciales válidas');
    allure.owner('ignacio.graneros');
    allure.severity('critical');
    allure.label('testType', 'E2E');

    const loginPage = new LoginPage(page);
    const dashboardPage = new DashboardPage(page);

    const ss = async (nombre: string) => {
      await allure.attachment(nombre, await page.screenshot(), 'image/png');
    };

    await test.step('Navegar a la página de login', async () => {
      await loginPage.goto();
      await ss('Pantalla: Login');
    });

    await test.step('Ingresar email', async () => {
      const email = page.locator('#email');
      await email.click();
      await ss('Click en campo Email');
      await email.fill(credentials.email);
      await ss('Email tipeado');
    });

    await test.step('Ingresar password', async () => {
      const password = page.locator('#password');
      await password.click();
      await password.type(credentials.password);
      await ss('Password tipeado');
    });

    await test.step('Click en Login', async () => {
      await page.getByRole('button', { name: /login/i }).click();
      await page.waitForTimeout(1000);
      await ss('Post Login');
    });

    await test.step('Ir a Sandbox API Keys', async () => {
      const sandboxHeader = page.locator('h5', { hasText: 'Sandbox private keys access' });
      await sandboxHeader.scrollIntoViewIfNeeded();
      await expect(sandboxHeader).toBeVisible();
      await ss('Texto Sandbox Keys visible');
    });

    await test.step('Verificar visibilidad de API Key', async () => {
      await dashboardPage.assertAPIKeyVisible();
      await ss('API Key Visible');
    });

    await test.step('Verificar valor correcto de API Key', async () => {
      const expectedKey = 'Ysh7cIDDglVga6AFrKWVXyyXeihmBILDR1ZDCEVCtnaKGE8jghfcoSMAN5gAZMdB';
      const apiKeyElement = page.getByText(expectedKey, { exact: true });
      await expect(apiKeyElement).toBeVisible();
      await ss('Validación de valor de API Key');
    });
  });
});
