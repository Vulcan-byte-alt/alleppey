"""Remove embedded metadata (EXIF, XMP, content credentials, text chunks) from site images.

PNG and JPEG sources are re-saved with their pixels only. Run before compress_images.py:
    python scripts/strip_metadata.py
Then verify:
    python scripts/strip_metadata.py --check
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
DIRS = [ROOT, ROOT / "houseboat"]
MARKERS = (b"c2pa", b"jumb", b"caBX", b"trainedAlgorithmicMedia", b"Content Credentials", b"OpenAI", b"DigitalSourceType")


def images():
    for d in DIRS:
        for p in sorted(d.iterdir()):
            if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
                yield p


def has_markers(path):
    data = path.read_bytes()
    return [m.decode() for m in MARKERS if m in data]


def strip(path):
    if not has_markers(path) and not Image.open(path).info:
        return False
    im = Image.open(path)
    im.load()
    clean = Image.new(im.mode, im.size)
    clean.putdata(list(im.getdata()))
    if path.suffix.lower() == ".png":
        clean.save(path, "PNG", optimize=True)
    elif path.suffix.lower() in (".jpg", ".jpeg"):
        clean.save(path, "JPEG", quality=95, optimize=True)
    else:
        clean.save(path, "WEBP", quality=90, method=6)
    return True


def main():
    if "--check" in sys.argv:
        dirty = [(p.relative_to(ROOT).as_posix(), has_markers(p)) for p in images() if has_markers(p)]
        for name, found in dirty:
            print("still tagged:", name, found)
        print("clean" if not dirty else f"{len(dirty)} files still carry metadata")
        return
    changed = [p.relative_to(ROOT).as_posix() for p in images() if strip(p)]
    print(f"stripped {len(changed)} files")


if __name__ == "__main__":
    main()
