"""Genera la configuración de redirecciones del servidor a partir de data/redirects.csv.

Produce nginx (server/redirects.nginx.conf) y Apache (server/redirects.htaccess).
Las filas con estado 200 solo se verifican: deben existir como ruta del sitio.
"""

import csv
from pathlib import Path

HUGO_DIR = Path(__file__).resolve().parent.parent
REDIRECTS_CSV = HUGO_DIR / "spec" / "redirects.csv"
ROUTES_CSV = HUGO_DIR / "spec" / "routes.csv"
SERVER_DIR = HUGO_DIR / "server"


def load_rows(path):
    """Lee un CSV como lista de diccionarios."""
    with open(path, encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def check_expected_200(rows, known_urls):
    """Avisa sobre las rutas que deben responder 200 y no existen en el sitio."""
    missing = [row["from"] for row in rows if row["status"] == "200" and row["from"] not in known_urls]
    for url in missing:
        print(f"  AVISO: {url} debe responder 200 y no está en routes.csv (revisar si es un post del blog).")
    return missing


def write_nginx(permanent_rows):
    """Escribe las reglas 301 para nginx."""
    lines = ["# Generado por scripts/gen_redirects.py desde data/redirects.csv. No editar a mano.", ""]
    for row in permanent_rows:
        lines.append(f'location = {row["from"]} {{ return 301 {row["to"]}; }}')
    path = SERVER_DIR / "redirects.nginx.conf"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  {path.name}: {len(permanent_rows)} reglas 301.")


def write_htaccess(permanent_rows):
    """Escribe las reglas 301 para Apache."""
    lines = ["# Generado por scripts/gen_redirects.py desde data/redirects.csv. No editar a mano.", ""]
    for row in permanent_rows:
        lines.append(f'Redirect 301 {row["from"]} {row["to"]}')
    path = SERVER_DIR / "redirects.htaccess"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  {path.name}: {len(permanent_rows)} reglas 301.")


def main():
    """Genera ambos archivos de configuración."""
    SERVER_DIR.mkdir(exist_ok=True)
    rows = load_rows(path=REDIRECTS_CSV)
    known_urls = {route["url"] for route in load_rows(path=ROUTES_CSV)}

    permanent_rows = [row for row in rows if row["status"] == "301"]
    write_nginx(permanent_rows=permanent_rows)
    write_htaccess(permanent_rows=permanent_rows)
    check_expected_200(rows=rows, known_urls=known_urls)
    print("Listo: configuración de redirecciones generada.")


if __name__ == "__main__":
    main()
