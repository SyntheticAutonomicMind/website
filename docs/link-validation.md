# Link Validation

How this site keeps internal links, anchors, and prev/next chains honest.

## Before every commit

```bash
# 1. Full internal + external link check
python3 scripts/validate-links.py

# 2. Start a local server and click through changed pages
python3 -m http.server 8000
```

## What to check

| Check | How |
|-------|-----|
| Internal links resolve | `python3 scripts/validate-links.py` |
| External links resolve | `python3 scripts/validate-links.py --external` (if supported) or manual spot-check |
| In-page TOC anchors | TOC `href="#..."` values must match an `id="..."` on the same page |
| Prev/next chains | `data-prev`/`data-next` on `<article class="doc-page">` must point at existing pages, and the label after `\|` must match the target page's `<title>` prefix |
| New pages | Listed in the product `index.html` card grid and in `sitemap.xml`, with unique title, meta description, and canonical |
| Removed/renamed pages | Remove from `sitemap.xml`, fix every inbound link, re-stitch the prev/next chain |

## Redirect stubs

Retired URLs that were indexed by search engines are kept as redirect stubs
(`ai-coding-assistant-macos.html` and friends). Each stub must have:

- `<link rel="canonical">` pointing at the **target** page
- `<meta http-equiv="refresh" content="0; url=...">` plus a JS `location.replace()` and a plain link
- `robots: noindex`, and **not** listed in `sitemap.xml`

## Notes

- One-off migration scripts from past restructures are not kept in the
  deployed tree. If you need a bulk fixer, write it in `scratch/` (gitignored),
  run it, and delete it.
- The site is HTML-first: there is no build step, so a broken link in a
  committed `.html` file is live within minutes of push.
