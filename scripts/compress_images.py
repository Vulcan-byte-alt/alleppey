"""Compress site images to WebP using every CPU core.

For each PNG/JPG in the project root and houseboat/ it writes:
  <name>.webp       (max 1600px wide, near-lossless visual quality)
  <name>-640.webp   (mobile size, only when the source is wider than 640px)
plus favicons and 1200x630 social share images in og/.
Sources are never modified. Re-run after adding images: python scripts/compress_images.py
"""
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
DIRS = [ROOT, ROOT / "houseboat"]
SKIP_PREFIXES = ("logo1",)
MAX_W, SMALL_W = 1600, 640
QUALITY, SMALL_QUALITY = 78, 72


def save_webp(img, path, quality):
    # method=6 is the slowest/smallest encoder setting; fine on a multi-core CPU
    img.save(path, "WEBP", quality=quality, method=6, exact=False)


def resized(img, width):
    if img.width <= width:
        return img
    return img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)


def process(src):
    src = Path(src)
    img = ImageOps.exif_transpose(Image.open(src))
    img = img.convert("RGBA" if img.mode in ("RGBA", "LA", "P") else "RGB")
    is_logo = src.name == "logo.png"
    full = resized(img, 320 if is_logo else MAX_W)
    out = src.with_suffix(".webp")
    save_webp(full, out, 90 if is_logo else QUALITY)
    small = None
    if not is_logo and full.width > SMALL_W:
        save_webp(resized(img, SMALL_W), src.with_name(src.stem + "-640.webp"), SMALL_QUALITY)
        small = SMALL_W
    rel = src.relative_to(ROOT).as_posix()
    return rel, {"w": full.width, "h": full.height, "small": small, "before": src.stat().st_size, "after": out.stat().st_size}


def extras():
    logo = Image.open(ROOT / "logo.png").convert("RGBA")
    logo.thumbnail((32, 32), Image.LANCZOS)
    logo.save(ROOT / "favicon-32.png", optimize=True)
    icon = Image.new("RGB", (180, 180), "#0a0a0a")
    mark = Image.open(ROOT / "logo.png").convert("RGBA")
    mark.thumbnail((140, 140), Image.LANCZOS)
    icon.paste(mark, ((180 - mark.width) // 2, (180 - mark.height) // 2), mark)
    icon.save(ROOT / "apple-touch-icon.png", optimize=True)
    (ROOT / "og").mkdir(exist_ok=True)
    for name in ("hero.png", "home.jpg", "houseboat.jpg", "houseboat_hero.jpg", "gallery1.png", "gallery3.jpg"):
        im = ImageOps.fit(Image.open(ROOT / name).convert("RGB"), (1200, 630), Image.LANCZOS)
        im.save(ROOT / "og" / (Path(name).stem + ".jpg"), "JPEG", quality=80, optimize=True, progressive=True)


def main():
    sources = [p for d in DIRS for p in sorted(d.iterdir())
               if p.suffix.lower() in (".png", ".jpg", ".jpeg") and not p.name.startswith(SKIP_PREFIXES)
               and p.name not in ("favicon-32.png", "apple-touch-icon.png")]
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as pool:
        manifest = dict(pool.map(process, sources))
    extras()
    (ROOT / "scripts" / "image-manifest.json").write_text(json.dumps(manifest, indent=1))
    before = sum(m["before"] for m in manifest.values())
    after = sum(m["after"] for m in manifest.values())
    print(f"{len(manifest)} images: {before/1e6:.1f} MB -> {after/1e6:.1f} MB (full size WebP)")


if __name__ == "__main__":
    sys.exit(main())
