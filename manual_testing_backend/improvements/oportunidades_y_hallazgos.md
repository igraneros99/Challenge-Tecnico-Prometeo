# Propuestas de Mejora y Hallazgos Detectados – API /validate-account/

En este readme se resumen los hallazgos que fui encontrando al realizar el relevamiento tecnico del endpoint https://account-validation.sandbox.prometeoapi.com/validate-account/, el readme esta estructurado en hallazgos encontrados de forma general, de forma especifica, propuestas de mejoras y propuestas de mejoras funcionales
---

## 1. Hallazgos Detectados

### Hallazgos Generales

- **Errores 500 ante entradas inválidas:** campos mal formateados como `account_number` o `branch_code` los cuales dan error 50, cuando deberían generar un 400 con un mensaje el cual pueda ser legible para el usuario.
- **Validaciones de tipo inexistentes:** se aceptan letras o símbolos en campos que deberían ser numéricos, lo que da fallas internas.
- **Falta de documentación específica por país:** no hay un detalle de los formatos esperados, bancos disponibles ni estructuras válidas, forzando a hacer la validacion segun la documentacion de prometeo y prueba y error.
- **Mensajes de error inconsistentes:** varían entre países en idioma, estructura y contenido, lo que hace mas dificil el debugging.
- **Sandbox sin cuentas de prueba conocidas:** no hay cuentas oficialmente documentadas como válidas o inválidas para testeo automatizado.
- **Entorno Colombia inoperativo:** no responde correctamente a ninguna solicitud; devuelve errores 500 o queda cargando infinitamente.

### 1.2 Hallazgos por País

#### Argentina
- Errores 500 ante parámetros faltantes o alias mal formateados.
- Alias inexistentes devuelven 500 en lugar de 404 o 422.
- Cuentas fictias son aceptadas como válidas.
- Mensajes genéricos como "Error interno" lo que complica el analisis del response.

#### Brasil
- IBAN mal puesto no reporta el campo incorrecto.
- Alias de otro país genera un error que no es claro para el usuario.
- Documentos mal formateados se aceptan, lo cual deberia de ser validado y advertir en caso de ser incorrecto.
- Un mismo `account_number` es válido con o sin IBAN, generando confusion en el comportamiento del `account_number`.
- Inputs parcialmente erróneos devuelven 404 en lugar de 400.

#### México
- `branch_code` con letras genera error 500.
- Algunos mensajes de error apuntan al campo equivocado (por ejemplo, `country_code` omitido genera mensaje sobre `account_number`).
- Las cuentas válidas están bien soportadas y las inválidas devuelven respuestas esperadas.

#### Colombia
- Sandbox inoperativo al momento de realizar las pruebas y este readme.
- Todas las solicitudes devuelven error 500 o timeout.
- La UI oficial tampoco responde.
- No se puede validar los ejemplos que estan en la documentacion de este endpoint.

---

## 2. Propuestas de Mejora

### 2.1 Técnicas Globales

- **Validaciones de entrada:** verificar tipo, longitud y formato antes de procesar, devolviendo 400 con mensaje específico segun que puede haber fallado.
- **Estandarización de errores:** aplicar una estructura uniforme en todos los países, ejemplo:

```json
{
  "errors": [
    {
      "code": "INVALID_ACCOUNT",
      "message": "El número de cuenta es inválido para el banco seleccionado."
    }
  ]
}
```

- **Documentación técnica detallada por país:** incluir bancos habilitados, formato de cuenta, campos obligatorios y ejemplos válidos/erróneos.
- **Endpoint `/test-accounts`:** permitir acceso a cuentas dummy válidas/invalidas por país, no limitarse a usar cuentas que no existen o son erroneas (Input tipo ABC12345)
- **Gestión controlada de sandbox caídos:** devolver 503 con un mensaje mas claro en caso de que el servicio este caido para colombia.
- **Códigos HTTP consistentes:**
  - 200: validación exitosa (válida o no)
  - 400: error de entrada
  - 500: error interno
  - 503: servicio no disponible

### 2.2 Funcionales

- **Claridad sobre el objetivo de la API:** indicar si valida formato, existencia real o datos ficticios.
- **Diferenciación de ambiente:** incluir `"environment": "sandbox"` o un header como `X-Environment: sandbox` para tener claridad de adonde se estan ejecutando los post.
- **Motivo funcional en errores:** agregar campo `"reason"` con detalle legible.
- **Soporte de mensajes amigables:** incluir `"user_message"` esto ayuda tanto al debugging como para lo que puede mostrarse en el frontend.
- **Listado de bancos soportados:** exponer un JSON por país con códigos y nombres de bancos en la documentacion oficial de prometeo.
- **Indicador de retry:** incluir `"retryable": true/false` en errores transitorios, facilitaria el retry de las llamadas y aportaria robustez al momento de automatizar al no tener endpoints de naturaleza flaky
- **Incorporación de trace ID:** agregar `trace_id` por request para facilitar debugging ( importante )
- **Ejemplos visuales por país:** mostrar estructuras válidas e inválidas en documentación técnica.

---

## 3. Conclusión
Implementar mejoras en validación, documentación y manejo de errores permite escalar esta solución a más países, garantizar pruebas automatizadas más confiables y mejorar significativamente la experiencia de integración para todo el equipo tecnico
