#!/usr/bin/env bash
# Construye el sitio. Uso: scripts/build.sh [produccion|staging]
set -euo pipefail

ENTORNO="${1:-produccion}"
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
cd "$RAIZ"

echo "→ Generando páginas desde content/site-content.json"
python3 scripts/gen_pages.py

echo "→ Generando redirecciones del servidor"
python3 scripts/gen_redirects.py

if [ "$ENTORNO" = "staging" ]; then
  echo "→ Construyendo staging (robots.txt bloquea la indexación)"
  HUGO_ENV=staging hugo --baseURL "https://staging.lamusica.fm/" --minify --gc
else
  echo "→ Construyendo producción"
  hugo --minify --gc
fi

echo "→ Listo. Salida en $RAIZ/public ($(du -sh public | cut -f1))"
