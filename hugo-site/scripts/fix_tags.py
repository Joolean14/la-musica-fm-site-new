"""Rebuild post tags from the /tag archives, reading only the post listings.

The first pass scanned whole archive pages, so every tag also picked up the
site's menu and footer links - which gave the static pages all 733 tags.
"""
import glob
import html
import os
import re

EXPORT = "../wordpress-export"
ARTICLE = re.compile(r"<article\b[^>]*>(.*?)</article>", re.S)
POST_LINK = re.compile(r'href="/([^"/]+)/"')


def tag_name(page_html, fallback):
    """The tag's display name, from the archive page title."""
    match = re.search(r"<title>(.*?)</title>", page_html, re.S)
    if not match:
        return fallback
    name = html.unescape(match.group(1)).split(" - ")[0].strip()
    return re.sub(r"^Archivos de\s+|\s+archivos$", "", name).strip() or fallback


def build_tag_map():
    """Map post slug -> tag names, using only links inside <article> blocks."""
    tag_map = {}
    for slug in sorted(os.listdir(os.path.join(EXPORT, "tag"))):
        index_path = os.path.join(EXPORT, "tag", slug, "index.html")
        if not os.path.exists(index_path):
            continue
        page_html = open(index_path, encoding="utf-8", errors="replace").read()
        name = tag_name(page_html, slug)
        for article_html in ARTICLE.findall(page_html):
            for linked in set(POST_LINK.findall(article_html)):
                tag_map.setdefault(linked, set()).add(name)
    return tag_map


def apply_tags(tag_map):
    """Rewrite the tags: line in every content file."""
    changed = 0
    for path in glob.glob("content/*.md") + glob.glob("content/posts/*.md"):
        text = open(path, encoding="utf-8").read()
        slug_match = re.search(r'^slug: "(.*?)"', text, re.M)
        if not slug_match:
            continue
        tags = sorted(tag_map.get(slug_match.group(1), []))
        line = "tags: [%s]" % ", ".join('"%s"' % t.replace('"', '\\"') for t in tags)
        if re.search(r"^tags: \[.*\]$", text, re.M):
            text = re.sub(r"^tags: \[.*\]$", line if tags else "", text, count=1, flags=re.M)
            text = text.replace("\n\n---\n", "\n---\n", 1)
        elif tags:
            text = text.replace("\nslug: ", "\n" + line + "\nslug: ", 1)
        open(path, "w", encoding="utf-8").write(text)
        changed += 1
    return changed


tag_map = build_tag_map()
print("tags resolved for %d posts" % len(tag_map))
print("updated %d content files" % apply_tags(tag_map))
