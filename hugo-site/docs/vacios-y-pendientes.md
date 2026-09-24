# Vacíos, contradicciones y recursos faltantes

Reporte de la implementación. Ninguno de estos puntos se resolvió inventando
contenido ni tomando decisiones editoriales: donde falta información, la página
queda estructurada y el texto pendiente está señalado.

## 1. Contenido que no viene en el paquete

| Punto | Dónde | Estado en el sitio |
|---|---|---|
| Casos y experiencias | `routes.csv` pide `/ecosistema/casos-y-experiencias/` con plantilla `CaseIndexPage`, pero `site-content.json` no trae ningún arreglo de casos. | Página construida con enlaces a rutas relacionadas y una nota de que los casos se publican cuando estén documentados. Falta el contenido. |
| Proyectos propios | Tampoco hay un arreglo de proyectos. | Se deriva de `ecosystem.entities` filtrando los tipos «marca y proyecto» y «marca y producto». Confirmar si esa es la lista correcta. |
| Medellín Ciudad de Música | `cityVision.sections` trae los 10 títulos, pero solo `purpose` tiene texto. | Los 10 tramos se muestran como índice. Faltan nueve cuerpos de texto. |
| Política de privacidad | `privacy` solo trae la URL. | Página construida con los datos del responsable y una nota; falta el texto legal vigente. |
| Equipo | `implementation-spec.md` pide «equipo» en AboutPage; `about` no lo incluye. | No se renderiza ninguna sección de equipo. |
| Blog: autor e imagen social | La especificación los pide; el JSON no trae autoría. | Se usan fecha, fecha de actualización y `featured_image` de los posts heredados. Falta el dato de autor. |

## 2. Recursos faltantes

- **Diploma CoCrea**: `cityVision.document.path` apunta a `assets/documents/diploma-cocrea.pdf`,
  que no existe en el paquete. El visor muestra el aviso de archivo pendiente y no
  inventa un enlace. Al cargar el PDF en `static/documents/diploma-cocrea.pdf` el
  visor y la descarga aparecen solos.
- **URLs externas**: cinco de las siete entidades tienen `externalUrl: null`
  (LaMúsica.fm, Carbonero, Jardín de Audiencias, AiiA, Colombian Sync Market).
  Siguiendo el contrato del componente, esas fichas no muestran botón externo.
  Faltan las URLs definitivas.
- **Tipografías**: se cargan desde Google Fonts con `display=swap`. Para cumplir
  del todo el requisito de rendimiento conviene alojarlas en el servidor; hace
  falta confirmar la licencia y las variantes que se usarán.
- **Identificadores de analítica**: no se recibieron; no hay ningún script de
  medición en el sitio.

## 3. Contradicciones entre documentos

- **Color de tinta**: `implementation-spec.md` fija `#151713`; el prototipo usa
  `#1a1a18`. Se aplicó el valor de la especificación.
- **`brandAssets`**: la especificación dice que el componente toma los logos de
  «`brandAssets` en el JSON», como si fuera una clave global. En el archivo los
  logos están dentro de cada entidad (`ecosystem.entities[].brandAssets`). Se
  implementó según el archivo.
- **Vocabulario del mapa**: los filtros pedidos son empresa, marca, proyecto,
  servicio y visión de ciudad, pero los tipos del JSON son «empresa», «marca y
  proyecto» y «marca y producto». Los filtros funcionan por coincidencia parcial;
  conviene unificar el vocabulario en el JSON.
- **Relaciones del mapa**: el contrato dice que los nodos solo se conectan cuando
  hay una relación cargada en los datos, pero no existe ningún arreglo de
  relaciones. Hoy el mapa solo dibuja la pertenencia al articulador, que sí está
  declarada. Las relaciones adicionales se cargan en `data/connections.json`.
- **Formulario, paso 3**: `routeDetails` es de tipo `conditionalFields` pero no
  define ni campos ni condiciones. Se implementó como un campo de texto abierto.
  Faltan las condiciones reales.
- **Formulario, paso 4**: `contactData` trae solo los identificadores de los
  campos. Las etiquetas visibles están en `data/form_fields.json` y son una
  propuesta pendiente de aprobación editorial.
- **Categorías del blog**: `blog.categories` lista siete categorías nuevas que no
  coinciden con las de los 272 artículos heredados de WordPress. Hace falta
  decidir si se reclasifican los artículos o si la lista nueva aplica solo a los
  próximos.
- **Años de archivo**: `history.archiveYears` enumera 2016–2024, pero del archivo
  de WordPress solo se pudieron recuperar dos interfaces (portada e historia de
  2023). Faltan los materiales de los demás años.

## 4. Decisiones tomadas durante la implementación

Se reportan por transparencia; ninguna cambia contenido ni diseño aprobado.

- `/historia-lamusica-fm/` estaba ocupada por un artículo heredado de WordPress
  («Conoce Nuestra Historia»). `routes.csv` asigna esa URL a `HistoryPage`, así
  que la página nueva la toma y el artículo se conservó en
  `/archivo/historia-2023/`, enlazado desde la sección de archivo de Historia.
- La portada Divi anterior se conservó en `/archivo/portada-2023/` como pieza de
  archivo, sin sus scripts.
- Las páginas de WordPress sustituidas por rutas nuevas o por redirecciones 301 se
  movieron a `archive-legacy/`, fuera del sitio construido.
- `/2023-recap/` debe responder 200 según `redirects.csv`: lo resuelve el artículo
  heredado del mismo nombre, que se conserva.
- Las páginas heredadas del export (por ejemplo `/artistas/`) conservan su marcado
  Divi original, que incluye enlaces `href="#"`. Ninguna página del sitio nuevo
  los tiene. Falta decidir si esas páginas heredadas se mantienen, se rehacen o se
  retiran.
