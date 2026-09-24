# LaMúsica.fm — Hugo

Static site built from the Simply Static WordPress export in `../wordpress-export/`.

    hugo server        # preview at http://localhost:1313
    hugo               # build into ./public

## Layout

    hugo-site/
      content/
        _index.md        landing page - the original WordPress homepage, verbatim
        posts/           272 blog posts (one .md each)
        *.md             10 standalone pages (quienes-somos, servicios, contacto, ...)
      layouts/           templates for the blog; the landing page bypasses these
      static/css/        site.css - the blog stylesheet
      archetypes/        template used by `hugo new`
      scripts/convert.py regenerates content/ from the export
      hugo.toml          config, menu, mounts

    wordpress-export/    the original export - source material, never edited

## Two designs, on purpose

- **Landing page (`/`)** is the original Divi homepage, byte-for-byte. It is stored as
  raw content and emitted by `layouts/index.html` without a wrapper, so Hugo does not
  reformat it. Its CSS and JS come from the export via the mounts in `hugo.toml`.
- **Everything else** uses the light theme in `layouts/` + `static/css/site.css`.

## URLs

Post URLs keep the original WordPress shape (`/slug/`), so old links still resolve.
The blog listing is at `/blog/`.

## Media

`hugo.toml` mounts the export's `wp-content` and `wp-includes` instead of copying them,
so the 1.8 GB of media stays in one place. Note that `hugo` copies mounted files into
`public/`, making a full build ~1.9 GB - worth trimming before deploying.
