"""Strip near-white backgrounds from flower webp files, keeping colored petals.

Heuristic: only fade a pixel out when it's bright AND grayscale-ish
(R/G/B close to each other). That spares the colored interior of the flower
even if it has bright pinks/whites in the petal.
"""
from PIL import Image
from pathlib import Path

src_dir = Path("photos")

GRAY_SPREAD_MAX = 40    # tolerate slight color tint in "white" pixels (jpeg/webp artifacts)
BRIGHT_MIN      = 180
BRIGHT_FULL     = 225

def whiten_to_alpha(im):
    im = im.convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            spread = max(r, g, b) - min(r, g, b)
            if spread > GRAY_SPREAD_MAX:
                continue                  # colored pixel — keep
            avg = (r + g + b) / 3
            if avg < BRIGHT_MIN:
                continue                  # dark grayscale — keep (shadow, line)
            if avg >= BRIGHT_FULL:
                px[x, y] = (r, g, b, 0)
            else:
                t = (avg - BRIGHT_MIN) / (BRIGHT_FULL - BRIGHT_MIN)
                px[x, y] = (r, g, b, int(a * (1 - t)))
    return im

for n in range(1, 6):
    src = src_dir / f"{n}.webp"
    if not src.exists():
        print(f"skip {src} (missing)")
        continue
    out = src_dir / f"{n}.png"
    im = Image.open(src)
    out_im = whiten_to_alpha(im)
    out_im.save(out, "PNG", optimize=True)
    print(f"{src.name} -> {out.name}  {out_im.size}")
print("done")
