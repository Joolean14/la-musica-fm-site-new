# Entrega para implementación - LaMúsica.fm

Este paquete contiene lo necesario para que Julián construya el sitio en el repositorio y lo lleve al servidor.

## Orden de lectura
1. `docs/implementation-spec.md`
2. `content/site-content.json`
3. `docs/brand-assets.md`
4. `docs/routes.csv`
5. `docs/component-contracts.md`
6. `docs/redirects.csv`
7. `docs/server-checklist.md`
8. `prototype/portada-v01/`

## Regla de implementación
El JSON es la fuente del contenido. Las fichas de familia y servicio deben generarse con componentes reutilizables. El prototipo define la dirección visual de la portada; debe adaptarse al stack existente, no copiarse como código final sin integración.

Las páginas del ecosistema usan los recursos reales de cada marca. LaMúsica.fm conserva la estructura general; cada identidad se incorpora únicamente en los bloques, fichas y conexiones que le corresponden. Las reglas y rutas de los activos están en `docs/brand-assets.md` y `content/site-content.json`.

## Configuración necesaria para publicar
- Acceso y procedimiento de despliegue del servidor.
- Sistema receptor del formulario y sus credenciales como variables de entorno.
- Identificadores de analítica, si se usarán.
- Diploma CoCrea y recursos visuales definitivos.
- URLs externas definitivas de empresas, marcas y proyectos.

No deben subirse secretos, bases de datos ni copias del servidor al repositorio.
