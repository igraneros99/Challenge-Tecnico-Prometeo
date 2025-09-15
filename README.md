
## Ejecución de las Test Suites

Este proyecto cuenta con dos suites de testing automatizado:

- Una suite de **backend** utilizando `pytest` y `allure-pytest`.
- Una suite de **frontend** utilizando `Playwright` con integración de `allure-playwright`.

---

### Backend

Para ejecutar la suite de tests sobre el backend:

1. Posicionarse en la raíz del proyecto y moverse a la carpeta correspondiente:
   ```bash
   cd automation_testing_backend/test_automation/
   ```

2. Ejecutar la suite con generación de reportes Allure:
   ```bash
   pytest --alluredir=allure-results
   ```

   >*Nota:* Todos los tests se ejecutan correctamente. Sin embargo, por un bug conocido en `pytest-allure`, hay **2 test cases de Brasil** que **no aparecen en el reporte** pese a haber sido ejecutados. Esto **no afecta la ejecución real de los tests.**

3. Visualizar el reporte generado:
   ```bash
   allure serve allure-results
   ```

   Este comando abrirá un servidor local (`localhost`) en el navegador para navegar el reporte visual de la corrida de tests.

> En caso de no tener Allure instalado globalmente:
```bash
npm install -g allure-commandline --save-dev
```

---

### Frontend

Para ejecutar la suite de frontend con Playwright:

1. Moverse a la carpeta del frontend:
   ```bash
   cd automation_testing_frontend/
   ```

2. Ejecutar la suite con el reporter ya integrado:
   ```bash
   npx playwright test --reporter=list,allure-playwright
   ```

3. Generar el reporte Allure:
   ```bash
   npx allure generate ./allure-results --clean -o ./allure-report
   ```

4. Abrir el reporte generado:
   ```bash
   npx allure open ./allure-report
   ```

Este reporte incluirá:

- Estructura POM (Page Object Model)
- Validaciones completas de login y API Key
- Screenshots y trazas automáticas por cada test

> **Nota:** Este proyecto ya incluye una ejecución previa de la suite. Si solo se desea visualizar los resultados sin volver a correr los tests, ejecutar directamente el comando de apertura de Allure.
