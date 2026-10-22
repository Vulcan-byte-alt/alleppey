# Alleppey Homes website

Static site for https://alleppeyhomes.com, served by GitHub Pages (GoDaddy holds the DNS).

## Editing pages
- Page content lives in `src/pages/*.html` (front matter + body). Shared header, footer, contact popup and icons live in `partials/`.
- Build with `python scripts/build.py`. It writes the root `*.html` files and regenerates `sitemap.xml`. Commit the generated files too, because GitHub Pages serves them as they are.
- Do not edit the root `*.html` files by hand. Edit `src/pages/` and rebuild.
- Styles are in `ah.css` (design tokens first). Behaviour is in `ah.js`. Bump `VERSION` in `scripts/build.py` and the `?v=` in `partials/head.html` when you change CSS or JS so visitors get the new files.

## Images
- Put originals in the repo root (or `houseboat/`), then run `python scripts/compress_images.py`. It writes a full-size and a 640px WebP next to each image, plus favicons and `og/` share images.
- Use the `.webp` files in pages, with `width`, `height`, `alt` and `loading="lazy"` (not on the hero image).

## Phone numbers
Numbers are not written in the HTML. `contact.js` fills them in at runtime. Use `data-call="1"`, `data-wa="1"` (index into the list in `contact.js`) or `data-phone-text="1"` on elements. To change a number, edit `contact.js` only.
