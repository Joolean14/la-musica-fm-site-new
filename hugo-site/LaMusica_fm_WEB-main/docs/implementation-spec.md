# LaMúsica.fm - especificación de implementación

## Resultado esperado

Construir el sitio institucional y comercial de LaMúsica.fm en el repositorio `alejosanto/LaMusica_fm_WEB`, integrarlo al servidor y conservar el dominio `https://lamusica.fm`.

El paquete define rutas, contenido visible, componentes, comportamiento, accesibilidad, SEO y migración. No define un framework nuevo: se conserva el stack existente del repositorio y del servidor. Si el repositorio todavía no tiene stack, Julián debe documentar la elección técnica en el README antes de comenzar la implementación.

## Fuentes de verdad dentro del paquete

1. `content/site-content.json`: textos, navegación, familias, servicios, precios y datos globales.
2. `docs/routes.csv`: rutas que deben existir.
3. `docs/redirects.csv`: respuestas 200 y redirecciones 301.
4. `docs/component-contracts.md`: comportamiento de cada componente.
5. `prototype/portada-v01/`: referencia visual y responsiva del inicio.
6. `assets/brand/logo-lamusica.png`: logo que debe usarse; no reconstruirlo.
7. `docs/brand-assets.md`: uso y convivencia de las identidades del ecosistema.

## Estructura global

- Encabezado: logo, cinco entradas principales y CTA `Cuéntanos qué necesitas`.
- Contenido principal con un solo H1.
- Migas de pan en todas las páginas excepto Inicio.
- Pie con navegación, datos legales, dirección y privacidad.
- El contenido se carga desde una estructura reutilizable; las 21 fichas de servicios no se escriben como plantillas independientes.

## Plantillas de página

### HomePage
Orden: Hero -> selector de necesidades -> familias -> ecosistema -> Medellín Ciudad de Música -> historia -> contacto.

### ServicesIndexPage
Introducción, selector de necesidades, seis familias y contacto. Cada familia enlaza a su página y cada servicio a su ficha.

### ServiceFamilyPage
Título, introducción, servicios de la familia y CTA. El contenido viene de `services.families`.

### ServiceDetailPage
Pregunta de entrada, resumen, entregables, condición comercial pública, límites y CTA. El CTA debe abrir `/contacto/` con necesidad, familia y servicio precargados.

### EcosystemPage
Introducción, entidades, proyectos, casos y mapa de conexiones. Las marcas mantienen su identidad dentro de sus fichas y páginas. El componente toma logos y variantes desde `brandAssets` en el JSON.

### CityVisionPage
Propósito, oportunidad de ciudad, origen, reconocimiento CoCrea, modelo, proyectos, estado actual, futuro, participación y archivo público. Incluir visor y descarga del diploma.

### HistoryPage
Introducción, cronología, archivo de interfaces anteriores, presente, futuro y enlace al ecosistema.

### AboutPage
Definición, propósito, visión, capacidades, método, equipo y datos empresariales.

### ContactPage
Formulario guiado por perfil y necesidad. Debe conservar la selección proveniente de Inicio, Servicios o una ficha.

### BlogIndexPage y ArticlePage
Categorías, listado, búsqueda básica, autor, fecha, fecha de actualización, imagen social, contenido y CTA relacionado.

## Sistema visual

- Fondo principal `#F5F2E8`.
- Texto principal `#151713`; texto secundario `#606060`.
- Verde principal `#43661A`; verde medio `#537C21`; oliva `#9BAB14`; lima `#BBCD19`.
- Tipografía de interfaz: Manrope. Títulos editoriales: Source Serif 4.
- Ancho máximo de contenido: 1280 px.
- El hexágono se usa como nodo, conexión o ruta; no como relleno decorativo.
- Fotografías y documentos se presentan con contexto. No aplicar filtros que alteren su lectura documental.
- LaMúsica.fm conserva la retícula, navegación y jerarquía común del sitio.
- Cuando una página pertenece a una marca o proyecto, incorporar sus recursos reales sin recolorear, redibujar ni fusionar logos.
- Cuando intervienen varias marcas, cada identidad ocupa un módulo propio sobre una superficie neutral; la conexión se expresa con estructura, proximidad, líneas o nodos de LaMúsica.fm.
- La mezcla visual debe explicar relaciones entre servicios, empresas y proyectos. No usar marcas como textura o decoración.

### Contraste obligatorio
- `#BBCD19` con texto `#151713`.
- `#43661A` con texto blanco.
- `#F5F2E8` con texto `#151713`, `#606060` o `#43661A`.
- No usar blanco sobre `#BBCD19` ni gris claro sobre `#F5F2E8`.

## Comportamiento responsivo

- >=1081 px: navegación completa y retículas de hasta tres columnas.
- 761-1080 px: menú colapsado y retículas de dos columnas cuando el contenido lo permita.
- <=760 px: una columna, menú modal o panel, CTA visibles y tablas transformadas en tarjetas o desplazamiento accesible.
- Ningún contenido debe producir desplazamiento horizontal en 320 px de ancho.
- Objetivos táctiles mínimos de 44 x 44 px.

## Accesibilidad

- HTML semántico, enlace para saltar al contenido, jerarquía correcta de encabezados y regiones identificadas.
- Navegación completa por teclado, foco visible y cierre con Escape en menús o diálogos.
- Texto alternativo útil; imágenes decorativas con alt vacío.
- Formularios con label, instrucciones, mensajes de error asociados y resumen de errores.
- No depender del color, sonido, movimiento o mapa visual para transmitir información.
- Respetar `prefers-reduced-motion` y no reproducir audio o video automáticamente.

## SEO y migración

- Mantener las URL principales indicadas con estado 200.
- Implementar las redirecciones 301 de `docs/redirects.csv` antes de cambiar producción.
- Un H1, title, meta description, canonical y Open Graph por página.
- Generar sitemap XML y robots.txt.
- Datos estructurados: Organization en el sitio; Service en servicios; Article en blog; BreadcrumbList en páginas internas.
- No publicar páginas vacías, rutas de prueba ni parámetros de formulario en el índice.

## Formulario y datos

- Destino del formulario configurado en el servidor, nunca dentro del JavaScript público.
- Validación de servidor, control anti-spam y registro de errores.
- Consentimiento obligatorio con enlace a la política de privacidad.
- Campos y comportamiento definidos en `content/site-content.json`.
- El correo o sistema receptor se configura como variable del entorno del servidor.

## Rendimiento

- Imágenes en AVIF o WebP con dimensiones, `srcset` y carga diferida debajo del primer tramo.
- Logo en formato original aprobado; servir una versión optimizada sin redibujarlo.
- Fuentes alojadas localmente o cargadas con estrategia que evite bloqueo y salto de diseño.
- JavaScript progresivo: navegación, lectura y contenido básico funcionan aunque una interacción avanzada falle.
- Evitar librerías para comportamientos que puedan resolverse con HTML y CSS nativos.

## Repositorio y despliegue

- Trabajar en rama de implementación y usar pull request para integrar a producción.
- No incluir credenciales, copias de bases de datos ni archivos `.env`.
- Preparar ambiente de staging con la misma versión de runtime y configuración relevante del servidor.
- Hacer copia del sitio y base de datos actuales antes del cambio.
- Verificar redirecciones, formulario, HTTPS, canonical, sitemap y analítica después del despliegue.
- Documentar en el README del repositorio: stack, requisitos, instalación local, variables de entorno, build, despliegue y rollback.

## Criterios de terminación

- Todas las rutas de `docs/routes.csv` cargan sin error.
- Las 21 fichas de servicios se generan desde los datos estructurados.
- Navegación, menú móvil, formularios y mapa funcionan con teclado.
- El contexto seleccionado llega al formulario.
- No existen textos de prueba, botones vacíos, enlaces `#` ni errores de consola.
- Las URL antiguas responden con el estado indicado.
- La revisión móvil, accesibilidad, SEO, rendimiento y despliegue queda documentada en el pull request.
