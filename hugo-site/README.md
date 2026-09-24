# LaMúsica.fm — sitio web

Implementación del paquete de entrega `LaMusica_fm_WEB` sobre el stack Hugo que ya
existía en este repositorio. El contenido visible vive en `content/site-content.json`;
las plantillas lo renderizan. Las 21 fichas de servicio y las 6 familias se generan
desde esos datos, no como páginas escritas a mano.

Rama de trabajo: `implementacion/sitio-v02`. No se toca producción directamente.

---

## Stack

| Pieza | Versión / elección | Por qué |
|---|---|---|
| Generador | Hugo extended 0.166 | Ya estaba en el repositorio y sirve el archivo heredado de WordPress. |
| Contenido | JSON + CSV (`content/site-content.json`, `spec/routes.csv`, `spec/redirects.csv`) | Fuentes de verdad del paquete de entrega. |
| Estilos | CSS propio en `assets/css/site.css` | Sin framework: el sistema visual es específico. |
| JavaScript | `assets/js/site.js`, sin librerías | Progresivo: menú, mapa, formulario y blog funcionan sin él. |
| Tipografías | Manrope y Source Serif 4 vía Google Fonts (`display=swap`) | Pendiente: alojarlas localmente antes de publicar (ver Vacíos). |
| Formulario | PHP-FPM en `server/contacto.php`, expuesto en `/api/contacto` | Validación y credenciales del lado del servidor. |
| Servidor | nginx + PHP-FPM (`server/*.nginx.conf`) | Configuración de referencia; ajustar al servidor real. |
| Python | 3.10+ solo para los scripts de generación | No hace falta en el servidor. |

## Instalación local

    # Requisitos: hugo extended >= 0.140, python3 >= 3.10
    hugo version
    python3 --version

    cd hugo-site
    python3 scripts/gen_pages.py     # genera content/ desde el JSON
    hugo server                      # http://localhost:1313

Para iterar rápido sin copiar los 1.8 GB del archivo de WordPress:

    hugo server --config hugo.toml,hugo.check.toml

## Construcción

    scripts/build.sh              # producción → ./public
    scripts/build.sh staging      # staging, con robots.txt que bloquea indexación

`build.sh` regenera las páginas desde el JSON, regenera las redirecciones del
servidor y luego construye. Después:

    python3 scripts/check_rutas.py   # verifica routes.csv, redirects.csv y un H1 por página

## Variables de entorno

Solo las necesita el servidor, para el formulario. Nunca se versionan.
Plantilla en `server/variables-de-entorno.txt`.

| Variable | Uso |
|---|---|
| `LMFM_CONTACT_TO` | Destinatario de las consultas del formulario. |
| `LMFM_CONTACT_FROM` | Remitente autenticado del servidor de correo. |
| `LMFM_CONTACT_LOG` | Archivo de registro, fuera del docroot. |
| `LMFM_CONTACT_ORIGIN` | Origen permitido, `https://lamusica.fm`. |
| `HUGO_ENV` | `staging` para construir la versión no indexable. |

## Despliegue

1. Copia recuperable del sitio y la base de datos actuales (ver `docs/server-checklist.md`
   del paquete de entrega).
2. `scripts/build.sh staging` y publicar en `staging.lamusica.fm`, protegido con
   `auth_basic` según `server/staging.nginx.conf`. Verificar que no sea indexable.
3. Pruebas del checklist: rutas, 301, formulario real, teclado, móvil, SEO.
4. `scripts/build.sh` y sincronizar `public/` al servidor:

       rsync -az --delete public/ usuario@servidor:/var/www/lamusica/public/
       rsync -az server/ usuario@servidor:/var/www/lamusica/server/

5. Recargar nginx (`nginx -t && systemctl reload nginx`) con
   `server/lamusica.nginx.conf`, que incluye `server/redirects.nginx.conf`.
6. Verificar 200, 301, HTTPS, canonical, sitemap y recepción del formulario.

## Reversión

La copia anterior se conserva hasta cerrar la verificación.

    # 1. devolver el sitio anterior
    rsync -az --delete /var/www/lamusica/respaldo-AAAAMMDD/ /var/www/lamusica/public/
    # 2. devolver la configuración del servidor
    cp /etc/nginx/sites-available/lamusica.conf.respaldo /etc/nginx/sites-available/lamusica.conf
    nginx -t && systemctl reload nginx
    # 3. en el repositorio
    git revert <commit>   # o volver a la rama anterior; no se reescribe historia

El sitio es estático: revertir es reemplazar `public/`. La base de datos de
WordPress no se modifica en ningún paso de este despliegue.

---

## Estructura

    hugo-site/
      content/site-content.json   fuente de verdad del contenido visible
      content/                    páginas generadas (solo front matter) + 272 posts heredados
      content/archivo/            interfaces anteriores conservadas como documento
      spec/                       routes.csv y redirects.csv del paquete de entrega
      data/                       site.json, routes.json, connections.json, form_fields.json
      layouts/_default/           una plantilla por tipo de página de routes.csv
      layouts/partials/           componentes de docs/component-contracts.md
      assets/css, assets/js       sistema visual y JavaScript progresivo
      static/brand/               logos reales de cada identidad, sin alterar
      server/                     nginx, staging, redirecciones y receptor del formulario
      scripts/                    generación, construcción y verificación
      archive-legacy/             páginas de WordPress sustituidas, conservadas como referencia

## Reglas que el código respeta

- El JSON manda: cambiar un texto de servicio es editar `content/site-content.json`
  y volver a ejecutar `scripts/gen_pages.py`.
- Contraste: verde oscuro con blanco, lima solo con tinta oscura, hueso con tinta
  o verde oscuro. No hay texto blanco sobre lima en ninguna parte.
- El hexágono aparece como nodo, hito o marca de ruta. Nunca como relleno.
- Los logos se usan tal cual, eligiendo variante clara u oscura según la superficie
  (`layouts/partials/brand-logo.html`). Ninguno se recolorea, recorta ni combina.
- El mapa de conexiones siempre trae su lista textual equivalente.
- El formulario conserva `need`, `family`, `service` y `route` de la URL.
