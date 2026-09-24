"""Store the static pages verbatim.

Divi builder pages keep their layout in Theme Builder sections outside
entry-content, so extracting that div yields an almost empty page. These
pages are served exactly as exported instead, the same way the landing
page is.
"""
import glob
import html
import os
import re

EXPORT = "../wordpress-export"


def page_meta(page_html, slug):
    """Title and description for the page's front matter."""
    title = re.search(r"<title>(.*?)</title>", page_html, re.S)
    title = html.unescape(title.group(1)).split(" - ")[0].strip() if title else slug
    desc = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]*)"', page_html)
    return title, html.unescape(desc.group(1)) if desc else ""


def rebuild(slug):
    """Write one page as raw, unmodified HTML."""
    source = os.path.join(EXPORT, slug, "index.html")
    if not os.path.exists(source):
        return False
    page_html = open(source, encoding="utf-8", errors="replace").read()
    title, desc = page_meta(page_html, slug)
    front = ['---', 'title: "%s"' % title.replace('"', '\\"')]
    if desc:
        front.append('description: "%s"' % desc.replace('"', '\\"'))
    front += ['url: "/%s/"' % slug, 'layout: "wp"', '---', '', '']
    open("content/%s.md" % slug, "w", encoding="utf-8").write("\n".join(front) + page_html)
    return True


slugs = [os.path.basename(p)[:-3] for p in glob.glob("content/*.md")
         if os.path.basename(p) != "_index.md"]
done = sum(rebuild(slug=s) for s in slugs)
print("stored %d pages verbatim: %s" % (done, ", ".join(sorted(slugs))))
