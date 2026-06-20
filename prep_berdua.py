"""Convert HEIC year photos to JPG and merge 2026 LDR pair into one frame."""
from pathlib import Path
from PIL import Image
import pillow_heif

pillow_heif.register_heif_opener()

src = Path("photos/berdua")

def fix_orient(im):
    """Honor EXIF orientation so portrait HEIC doesn't end up sideways."""
    try:
        return Image.open(im) if False else ImageOps_exif(im)
    except Exception:
        return im

# safer EXIF handling
from PIL import ImageOps
def open_and_orient(p):
    im = Image.open(p)
    try:
        im = ImageOps.exif_transpose(im)
    except Exception:
        pass
    return im.convert("RGB")

# 1. HEIC -> JPG
for heic, out in [("2024.HEIC", "2024.jpg"), ("2025 (1).HEIC", "2025.jpg")]:
    p = src / heic
    if p.exists():
        im = open_and_orient(p)
        im.save(src / out, "JPEG", quality=88)
        print(f"converted {heic} -> {out}  size={im.size}")

# 2. Merge 2026(1) + 2026(2) side-by-side into one polaroid (4:5 portrait)
def cover_fit(im, w, h):
    iw, ih = im.size
    target_ratio = w / h
    src_ratio   = iw / ih
    if src_ratio > target_ratio:
        new_w = int(ih * target_ratio)
        x = (iw - new_w) // 2
        im = im.crop((x, 0, x + new_w, ih))
    else:
        new_h = int(iw / target_ratio)
        y = (ih - new_h) // 2
        im = im.crop((0, y, iw, y + new_h))
    return im.resize((w, h), Image.LANCZOS)

TARGET = (800, 1000)   # 4:5
GAP    = 6             # cream divider between the two halves
GAP_C  = (246, 231, 221)

half_w = (TARGET[0] - GAP) // 2
a = open_and_orient(src / "2026(1).jpeg")
b = open_and_orient(src / "2026(2).jpeg")

canvas = Image.new("RGB", TARGET, GAP_C)
canvas.paste(cover_fit(a, half_w, TARGET[1]), (0, 0))
canvas.paste(cover_fit(b, half_w, TARGET[1]), (half_w + GAP, 0))
canvas.save(src / "2026.jpg", "JPEG", quality=88)
print(f"merged 2026.jpg  size={canvas.size}")
print("done")
