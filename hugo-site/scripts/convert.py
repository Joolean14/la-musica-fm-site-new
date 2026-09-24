"""Convert the Simply Static WordPress export into Hugo content files."""
import html
import json
import os
import re
import sys
from urllib.parse import unquote

BACKUP_DIR = "/home/joolean14/Documents/la-musica-fm-desde-wp"
SITE_DIR = os.path.join(BACKUP_DIR, "hugo-site")


def read_text(path):
    """Read a file as utf-8, ignoring bad bytes."""
    with open(path, encoding="utf-8", errors="replace") as handle:
        return handle.read()


def slugs_from_sitemap(sitemap_name):
    """Return the url slugs listed in one sitemap file."""
    xml_text = read_text(os.path.join(BACKUP_DIR, sitemap_name))
    found_slugs = []
    for loc in re.findall(r"<loc>(.*?)</loc>", xml_text):
        slug = html.unescape(loc).strip("/").split("/")[-1]
        if slug and not slug.endswith(".xml"):
            found_slugs.append(slug)
    return found_slugs


def extract_div(page_html, class_name):
    """Return the inner HTML of the first div with this class, matching nesting."""
    start = re.search(r'<div[^>]*class="[^"]*\b%s\b[^"]*"[^>]*>' % class_name, page_html)
    if not start:
        return ""
    pos = start.end()
    depth = 1
    for tag in re.finditer(r"<(/?)div\b[^>]*>", page_html[pos:]):
        depth += -1 if tag.group(1) else 1
        if depth == 0:
            return page_html[pos:pos + tag.start()]
    return page_html[pos:]


def meta_value(page_html, attr, name):
    """Read one <meta> tag value from the page head."""
    pattern = r'<meta[^>]*%s="%s"[^>]*content="([^"]*)"' % (attr, re.escape(name))
    match = re.search(pattern, page_html)
    return html.unescape(match.group(1)) if match else ""


def yoast_article(page_html):
    """Return the Article node of the Yoast JSON-LD graph, if present."""
    match = re.search(r'class="yoast-schema-graph">(.*?)</script>', page_html, re.S)
    if not match:
        return {}
    try:
        graph = json.loads(match.group(1)).get("@graph", [])
    except json.JSONDecodeError:
        return {}
    for node in graph:
        if node.get("@type") in ("Article", "WebPage"):
            return node
    return {}


def build_tag_map():
    """Map each post slug to the tag names whose archive pages list it."""
    tag_map = {}
    tag_root = os.path.join(BACKUP_DIR, "tag")
    for tag_slug in sorted(os.listdir(tag_root)):
        index_path = os.path.join(tag_root, tag_slug, "index.html")
        if not os.path.exists(index_path):
            continue
        page_html = read_text(index_path)
        title_match = re.search(r"<title>(.*?)</title>", page_html, re.S)
        tag_name = html.unescape(title_match.group(1)).split(" - ")[0].strip() if title_match else tag_slug
        tag_name = re.sub(r"^Archivos de\s+", "", tag_name).strip()
        body = extract_div(page_html, "et_pb_posts") or page_html
        for linked in set(re.findall(r'href="/([a-z0-9\-%._À-￿]+)/"', body)):
            tag_map.setdefault(linked, set()).add(tag_name)
    return tag_map


def category_of(page_html):
    """Read the post category name from its archive link."""
    match = re.search(r'href="/category/[^"]*"[^>]*>(.*?)</a>', page_html, re.S)
    return html.unescape(re.sub(r"<[^>]+>", "", match.group(1))).strip() if match else ""


def yaml_quote(text):
    """Quote a value for YAML front matter."""
    return '"%s"' % text.replace("\\", "\\\\").replace('"', '\\"')


def convert(slug, section, tag_map):
    """Write one Hugo content file from an exported page."""
    slug = unquote(slug)  # sitemap urls percent-encode emoji in slugs
    source = os.path.join(BACKUP_DIR, slug, "index.html")
    if not os.path.exists(source):
        return False
    page_html = read_text(source)
    body = extract_div(page_html, "entry-content")
    if not body.strip():
        return False

    article = yoast_article(page_html)
    title = article.get("headline") or meta_value(page_html, "property", "og:title").split(" - ")[0]
    date = article.get("datePublished") or meta_value(page_html, "property", "article:published_time")
    modified = article.get("dateModified") or meta_value(page_html, "property", "article:modified_time")
    description = meta_value(page_html, "name", "description") or meta_value(page_html, "property", "og:description")
    image = meta_value(page_html, "property", "og:image")
    category = category_of(page_html)
    tags = sorted(tag_map.get(slug, []))

    lines = ["---", "title: %s" % yaml_quote(html.unescape(title or slug))]
    if date:
        lines.append("date: %s" % date)
    if modified:
        lines.append("lastmod: %s" % modified)
    if description:
        lines.append("description: %s" % yaml_quote(description))
    if image:
        lines.append("featured_image: %s" % yaml_quote(image))
    if category:
        lines.append("categories: [%s]" % yaml_quote(category))
    if tags:
        lines.append("tags: [%s]" % ", ".join(yaml_quote(t) for t in tags))
    lines.append("slug: %s" % yaml_quote(slug))
    lines += ["---", "", body.strip(), ""]

    out_dir = os.path.join(SITE_DIR, "content", section) if section else os.path.join(SITE_DIR, "content")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "%s.md" % slug), "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))
    return True


def main():
    """Convert every post and page found in the sitemaps."""
    print("Reading sitemaps...")
    post_slugs = slugs_from_sitemap("post-sitemap.xml")
    page_slugs = [s for s in slugs_from_sitemap("page-sitemap.xml") if s not in post_slugs]
    print("  posts: %d, pages: %d" % (len(post_slugs), len(page_slugs)))

    print("Building tag map from /tag archives...")
    tag_map = build_tag_map()
    print("  tagged slugs: %d" % len(tag_map))

    written_posts = sum(convert(slug=s, section="posts", tag_map=tag_map) for s in post_slugs)
    written_pages = sum(convert(slug=s, section="", tag_map=tag_map) for s in page_slugs)
    print("Wrote %d posts and %d pages." % (written_posts, written_pages))


main()
