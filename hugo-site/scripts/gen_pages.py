"""Genera los archivos de contenido del sitio a partir de data/site.json y data/routes.csv.

Los archivos generados solo llevan front matter: el texto visible vive en el JSON
y lo renderizan las plantillas. Volver a ejecutar el script es idempotente.
"""

import csv
import json
import shutil
from pathlib import Path

HUGO_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = HUGO_DIR / "data"
SPEC_DIR = HUGO_DIR / "spec"
CONTENT_DIR = HUGO_DIR / "content"
GENERATED_MARK = "generado: true"


def load_site_content():
    """Lee el JSON que es la fuente de verdad del contenido."""
    with open(DATA_DIR / "site.json", encoding="utf-8") as handle:
        return json.load(handle)


def load_routes():
    """Lee routes.csv como lista de diccionarios page/url/template."""
    with open(SPEC_DIR / "routes.csv", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def url_to_content_path(url):
    """Convierte /servicios/familia/ en la ruta del archivo .md correspondiente."""
    slug = url.strip("/")
    if not slug:
        return CONTENT_DIR / "_index.md"
    return CONTENT_DIR / slug / "_index.md"


def yaml_value(value):
    """Serializa un valor simple para el front matter."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    return json.dumps(value, ensure_ascii=False)


def write_stub(path, front_matter):
    """Escribe un archivo de contenido con solo front matter."""
    lines = ["---", GENERATED_MARK]
    for key, value in front_matter.items():
        lines.append(f"{key}: {yaml_value(value)}")
    lines.append("---")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def remove_previous_generation():
    """Borra los archivos generados en una corrida anterior para no dejar rutas huérfanas."""
    removed = 0
    for path in CONTENT_DIR.rglob("_index.md"):
        if GENERATED_MARK in path.read_text(encoding="utf-8"):
            path.unlink()
            removed += 1
            if not any(path.parent.iterdir()):
                shutil.rmtree(path.parent)
    print(f"Limpieza: {removed} archivos generados previos eliminados.")


def find_family_index(site_content, url):
    """Devuelve la posición de una familia de servicios dentro del JSON."""
    families = site_content["services"]["families"]
    for position, family in enumerate(families):
        if family["slug"] == url:
            return position
    return None


def find_service_position(site_content, url):
    """Devuelve (familia, servicio) de una ficha de servicio dentro del JSON."""
    families = site_content["services"]["families"]
    for family_position, family in enumerate(families):
        for service_position, service in enumerate(family["services"]):
            if service["slug"] == url:
                return family_position, service_position
    return None


def build_front_matter(site_content, route):
    """Arma el front matter de una ruta según su plantilla."""
    template = route["template"]
    url = route["url"]
    front_matter = {
        "title": route["page"],
        "url": url,
        "layout": template.lower(),
    }

    if template == "ServiceFamilyPage":
        family_position = find_family_index(site_content, url)
        if family_position is None:
            raise SystemExit(f"Falta la familia {url} en site.json")
        front_matter["familyIndex"] = family_position
        front_matter["weight"] = family_position + 1

    if template == "ServiceDetailPage":
        position = find_service_position(site_content, url)
        if position is None:
            raise SystemExit(f"Falta el servicio {url} en site.json")
        front_matter["familyIndex"], front_matter["serviceIndex"] = position
        front_matter["weight"] = position[1] + 1

    return front_matter


def collect_aliases(url):
    """Devuelve las URL antiguas que deben redirigir (301) hacia esta ruta."""
    aliases = []
    with open(SPEC_DIR / "redirects.csv", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["status"] == "301" and row["to"] == url:
                aliases.append(row["from"])
    return aliases


def write_routes_data(routes):
    """Publica routes.csv como JSON para que las plantillas armen las migas de pan."""
    target = DATA_DIR / "routes.json"
    target.write_text(json.dumps(routes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Migas de pan: {target.name} con {len(routes)} rutas.")


def main():
    """Genera todas las páginas declaradas en routes.csv."""
    site_content = load_site_content()
    remove_previous_generation()

    routes = load_routes()
    write_routes_data(routes=routes)

    created = 0
    for route in routes:
        front_matter = build_front_matter(site_content=site_content, route=route)
        aliases = collect_aliases(url=route["url"])
        if aliases:
            front_matter["aliases"] = aliases
        write_stub(path=url_to_content_path(url=route["url"]), front_matter=front_matter)
        created += 1
        print(f"  {route['url']:<80} {route['template']}")

    print(f"Listo: {created} páginas generadas desde site.json + routes.csv.")


if __name__ == "__main__":
    main()
