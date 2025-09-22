import { test } from '@playwright/test';
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

    await test.step('Login con credenciales válidas', async () => {
      await loginPage.login(credentials.email, credentials.password);
      await ss('Post Login');
    });

    await test.step('Ir a Sandbox API Keys', async () => {
      await dashboardPage.goToSandboxKeys();
      await ss('Sandbox Keys abierto');
    });

    await test.step('Verificar visibilidad de API Key', async () => {
      await dashboardPage.assertAPIKeyVisible();
      await ss('API Key Visible');
    });

    await test.step('Verificar valor correcto de API Key', async () => {
      await dashboardPage.assertAPIKeyValue(credentials.apiKey);
      await ss('API Key Validada');
    });
  });
});
