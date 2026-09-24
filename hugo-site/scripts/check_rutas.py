"""Verifica que el sitio construido cumpla routes.csv y redirects.csv.

Se ejecuta sobre ./public después de `hugo`. No reemplaza las pruebas en el
servidor, pero detecta rutas faltantes antes de desplegar.
"""

import csv
from pathlib import Path

HUGO_DIR = Path(__file__).resolve().parent.parent
PUBLIC_DIR = HUGO_DIR / "public"
SPEC_DIR = HUGO_DIR / "spec"


def page_exists(url):
    """Indica si una URL quedó construida como página."""
    return (PUBLIC_DIR / url.strip("/") / "index.html").exists()


def check_routes():
    """Todas las rutas de routes.csv deben existir."""
    missing = []
    with open(SPEC_DIR / "routes.csv", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if not page_exists(row["url"]):
                missing.append(row["url"])
    print(f"Rutas: {'todas presentes' if not missing else 'faltan ' + ', '.join(missing)}")
    return missing


def check_redirects():
    """Las filas 200 deben existir y las 301 deben tener alias construido."""
    problems = []
    with open(SPEC_DIR / "redirects.csv", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if not page_exists(row["from"]):
                problems.append(f"{row['from']} ({row['status']})")
    print(f"Redirecciones: {'todas resueltas' if not problems else 'revisar ' + ', '.join(problems)}")
    return problems


def check_single_h1():
    """Cada página construida del sitio nuevo debe tener un solo H1."""
    problems = []
    with open(SPEC_DIR / "routes.csv", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            page = PUBLIC_DIR / row["url"].strip("/") / "index.html"
            if page.exists() and page.read_text(encoding="utf-8").count("<h1") != 1:
                problems.append(row["url"])
    print(f"Encabezados H1: {'correctos' if not problems else 'revisar ' + ', '.join(problems)}")
    return problems


def main():
    """Ejecuta las tres verificaciones y reporta el resultado."""
    if not PUBLIC_DIR.exists():
        raise SystemExit("No existe ./public. Ejecuta scripts/build.sh primero.")
    failures = check_routes() + check_redirects() + check_single_h1()
    print("Resultado:", "sin hallazgos" if not failures else f"{len(failures)} hallazgos")


if __name__ == "__main__":
    main()
