# Oportunidades de mejora - QA Manual

## Registro

1. **Validación en tiempo real**
   - No se ve ninguna validación mientras se completan los campos. Por ejemplo, si ponés un mail sin "@" o una contraseña muy simple, no hay nada que avise hasta después de enviarlo. Estaría bueno que se indique al instante, sobre todo en formularios con varios campos.

2. **Requisitos de contraseña**
   - No se muestran en ningún lado las condiciones que tiene que cumplir la contraseña (mínimo de caracteres, mayúsculas, símbolos, etc.). Es bastante común que el usuario se equivoque por esto. Incluso después de errarla, la validacion salta una vez que el usuario manda la contraseña, no mientras se escribe.

3. **Manejo de errores**
   - Si algún campo tiene un error, no queda claro cuál fue el problema. El mensaje de error es genérico. Debería indicarse qué campo falló y por qué. Además, el diseño no diferencia si es un error del usuario o si pasó algo del lado del servidor ( La network solo devuelve el mismo error que se ve en la UI )

4. **Mejoras de experiencia de usuario**
   - No hay ningún tipo de ayuda visual: ni tooltips, ni textos debajo de los campos explicando qué se espera en cada uno. Sería útil para reducir errores de usuarios no tan entrenados en el uso de herramientas de este estilo.

5. **Seguridad básica**
   - No hay captcha ni ningún tipo de validación que bloquee registros automáticos. Esto puede ser problemático si se deja abierto en producción ( Se pueden automatizar registros usando PlayWright o otras herramientas de ataque de flood de usuarios a la aplicacion )
   - Tampoco hay ningún detalle visual que refuerce que el registro es seguro (como un ícono de candado o alguna leyenda tipo "Tus datos están protegidos").

---

## Inicio de sesión

1. **Validaciones básicas**
   - Podés enviar el formulario con los campos vacíos sin que pase nada visual. No hay una alerta inmediata que avise que te faltó completar algo.
   - Tampoco se explicita qué requisitos debe cumplir la contraseña, aunque existan y se muestren en el registro de la cuenta.

2. **Feedback de errores**
   - Si te equivocás en la contraseña, te tira un mensaje genérico (“Credenciales inválidas”), pero no sabés si erraste la contraseña o si ese usuario directamente no existe. Estaría bueno separar esos casos o al menos dar un feedback más claro.
   - Además, si hacés clic varias veces en “Iniciar sesión”, el botón no se bloquea y se puede mandar varias veces el mismo request. Esto puede generar problemas si alguien automatiza envíos con Playwright u otra herramienta ( Mencionado tambien en el register )

3. **Mejoras de UX**
   - Falta una opción para mantener la sesión iniciada (“Recordarme”).
   - Después de iniciar sesión con éxito, te manda directo al dashboard, pero no hay ningún mensaje de bienvenida ni confirmación visual. Algo como “Bienvenido/a” o “Sesión iniciada con éxito” seria provechoso para la experiencia del usuario.

4. **Accesibilidad**
   - No se nota un foco claro al navegar con teclado. Sería útil revisar si se respeta un orden lógico de tabulación.
   - Tampoco parece haber etiquetas accesibles para los lectores de pantalla. Esto puede ser un problema para usuarios con discapacidades visuales.

---

## Visualización de API Key

1. **Seguridad**
   - Apenas entrás al dashboard, la API Key está ahí visible, en texto plano. No hay botón para mostrar u ocultar.
   - Lo ideal sería que esté oculta por defecto, y que haya un botón tipo “Mostrar” con algún control de seguridad básico. Más si es una clave que puede usarse en producción.

2. **Copiar la clave**
   - No se puede copiar la clave con un clic. Tenés que seleccionarla a mano. Estaría bueno que tenga un botón de “Copiar” con algún feedback visual que confirme que se copió bien (un ícono que cambie, un toast, etc.).

3. **Gestión de claves**
   - Solo hay una clave visible. No hay forma de generar otra, ni de eliminarla, ni de rotarla. Tampoco se especifica si esa clave expira, si se puede usar en múltiples entornos o si es revocable ( Entiendo que hay una rotacion de api keys como secret, pero no es visiblemente entendible por el usuario )
   - Estaría bueno tener una pequeña sección de administración de claves, aunque sea mínima (regenerar, ver historial de uso, etc.).

4. **Contexto de uso**
   - No hay ningún texto explicativo que indique para qué sirve esa API Key, cómo se usa o si está asociada a un entorno sandbox, producción, etc. Algo de contexto ayudaría, especialmente si alguien nuevo entra por primera vez.
   - Seria de ayuda para el usuario que cuando haga un login exitoso, se haga un tour por el dashboard, en el cual se explique la funcionalidad del mismo.

5. **Diseño y visibilidad**
   - La tarjeta donde está la clave no resalta en el diseño general. Si no la estás buscando, pasa desapercibida.
   - Además, no hay ningún texto o aviso que diga en qué entorno estás trabajando. Por ejemplo, si es un entorno de pruebas, estaría bueno que eso se aclare visualmente para evitar errores.

