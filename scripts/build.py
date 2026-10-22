"""Build the static site: src/pages/*.html + partials/ -> root *.html, plus sitemap.xml.

Run from anywhere:  python scripts/build.py

Page source format (src/pages/<name>.html):

    ---
    slug: houseboat.html            output file name (default: <name>.html)
    title: ...                      <title>
    description: ...                meta description
    nav: houseboat                  which nav link is current (home, houseboat, homestay, packages, blog, contact)
    image: og/houseboat.jpg         1200x630 social image (default og/hero.jpg)
    type: website                   og:type (article for blog posts)
    og_title: ...                   optional shorter social title
    robots: index, follow, ...      optional
    priority: 0.8                   sitemap priority
    changefreq: monthly             sitemap changefreq
    lastmod: 2026-10-22             sitemap lastmod (default: today)
    ---
    <script type="application/ld+json">...</script>     (anything above the marker goes into <head>)
    <!--BODY-->
    <section>...</section>                              (page content, placed inside <main>)
"""
import datetime
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "pages"
PARTIALS = ROOT / "partials"
SITE = "https://alleppeyhomes.com"
VERSION = "20261041"
TODAY = datetime.date.today().isoformat()
NOTES = {
    "boats": (
        '<div class="wrap"><p class="note">Images are for illustration only, and some scenery and food images are digitally generated. '
        'Houseboat layouts, interiors, amenities and menus vary by boat, category and plan. '
        'Please confirm the details of your booking with us.</p></div>'
    ),
}
DEFAULT_ROBOTS = "index, follow, max-image-preview:large, max-snippet:-1"


def read(p):
    return Path(p).read_text(encoding="utf-8")


def parse(path):
    text = read(path).replace("\r\n", "\n")
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    if not m:
        sys.exit(f"{path.name}: missing front matter")
    meta = {}
    for line in m.group(1).split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    rest = m.group(2)
    head_extra, _, body = rest.partition("<!--BODY-->")
    if not _:
        head_extra, body = "", rest
    return meta, head_extra.strip(), body.strip()


def esc(s):
    return html.escape(s, quote=True)


def render(meta, head_extra, body, head, foot, icons):
    slug = meta["slug"]
    canonical = SITE + "/" if slug == "index.html" else f"{SITE}/{slug}"
    nav = meta.get("nav", "")
    if meta.get("base"):
        head = head.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">\n    <base href="' + meta["base"] + '">', 1)
    page = head + "\n" + body + "\n" + foot
    page = re.sub(r"\{\{cur:(\w+)\}\}", lambda m: 'aria-current="page"' if m.group(1) == nav else "", page)
    values = {
        "title": esc(meta["title"]),
        "description": esc(meta["description"]),
        "robots": meta.get("robots", DEFAULT_ROBOTS),
        "canonical": canonical,
        "type": meta.get("type", "website"),
        "og_title": esc(meta.get("og_title", meta["title"])),
        "image": meta.get("image", "og/hero.jpg"),
        "v": VERSION,
        "head_extra": head_extra,
        "icons": icons,
        "note": NOTES.get(meta.get("note", ""), ""),
    }
    for k, v in values.items():
        page = page.replace("{{" + k + "}}", v)
    left = re.findall(r"\{\{[^}]+\}\}", page)
    if left:
        sys.exit(f"{slug}: unresolved placeholders {left}")
    return page


def main():
    head, foot, icons = (read(PARTIALS / f) for f in ("head.html", "foot.html", "icons.html"))
    urls = []
    for src in sorted(SRC.glob("*.html")):
        meta, head_extra, body = parse(src)
        meta.setdefault("slug", src.name)
        out = ROOT / meta["slug"]
        out.write_text(render(meta, head_extra, body, head, foot, icons), encoding="utf-8", newline="\n")
        urls.append(meta)
        print("built", meta["slug"])

    # Pages not migrated to src/ yet stay in the sitemap
    built = {m["slug"] for m in urls}
    for f in sorted(ROOT.glob("*.html")):
        if f.name not in built and f.name != "404.html":
            urls.append({"slug": f.name, "priority": "0.5"})

    items = []
    for m in sorted((m for m in urls if m.get("sitemap") != "no"), key=lambda m: -float(m.get("priority", "0.6"))):
        loc = SITE + "/" if m["slug"] == "index.html" else f"{SITE}/{m['slug']}"
        items.append(
            "  <url>\n"
            f"    <loc>{loc}</loc>\n"
            f"    <lastmod>{m.get('lastmod', TODAY)}</lastmod>\n"
            f"    <changefreq>{m.get('changefreq', 'monthly')}</changefreq>\n"
            f"    <priority>{m.get('priority', '0.6')}</priority>\n"
            "  </url>"
        )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(items)
        + "\n</urlset>\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"sitemap.xml: {len(items)} urls")


if __name__ == "__main__":
    main()
