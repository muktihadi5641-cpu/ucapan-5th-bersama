"""Heart-shaped QR — modules form the heart silhouette, finders kept visible
so the result still decodes."""
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math
import cv2

URL = "https://muktihadi5641-cpu.github.io/ucapan-5th-bersama/"

# ---- generate QR matrix (no rendering yet) ----
qr = qrcode.QRCode(
    error_correction=ERROR_CORRECT_H,
    box_size=1,
    border=0,
)
qr.add_data(URL)
qr.make(fit=True)
matrix = qr.get_matrix()
N = len(matrix)
print(f"QR matrix: {N}x{N}")

# ---- canvas ----
MODULE = 24
PAD    = MODULE * 4
SIZE   = N * MODULE + 2 * PAD
RED    = (214, 40, 60)         # romantic red
PINK   = (255, 110, 145)       # pink accent
SHADOW = (180, 30, 60, 80)

img = Image.new("RGB", (SIZE, SIZE), "white")
draw = ImageDraw.Draw(img)

# ---- heart polygon ----
def heart_polygon(cx, cy, scale, n=600):
    pts = []
    for i in range(n + 1):
        t = (i / n) * 2 * math.pi
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2*t)
              - 2 * math.cos(3*t) - math.cos(4*t))
        pts.append((cx + x * scale, cy + y * scale))
    return pts

# Heart sized so it covers the QR modules area generously
heart_scale = SIZE / 36
hcx, hcy    = SIZE // 2, SIZE // 2 + SIZE // 32
heart_pts   = heart_polygon(hcx, hcy, heart_scale)

# ---- heart mask ----
mask = Image.new("L", (SIZE, SIZE), 0)
ImageDraw.Draw(mask).polygon(heart_pts, fill=255)

# ---- helpers ----
def is_finder(r, c):
    return ((r < 7 and c < 7)
         or (r < 7 and c >= N - 7)
         or (r >= N - 7 and c < 7))

def is_finder_area(r, c):
    # 8x8 quiet-zone box around each finder
    return ((r < 8 and c < 8)
         or (r < 8 and c >= N - 8)
         or (r >= N - 8 and c < 8))

# Alignment pattern position for v5 QR
def is_alignment(r, c):
    if N < 25:  # versions 1 only
        return False
    # for version 5 (N=37), alignment center at (30,30); for v4 (N=33) at (26,26) etc.
    centers = []
    if N == 21: centers = []                        # v1: none
    elif N == 25: centers = [18]                    # v2
    elif N == 29: centers = [22]                    # v3
    elif N == 33: centers = [26]                    # v4
    elif N == 37: centers = [30]                    # v5
    elif N == 41: centers = [34]                    # v6
    elif N == 45: centers = [22, 38]                # v7
    for ax in centers:
        for ay in centers:
            if abs(r - ay) <= 2 and abs(c - ax) <= 2:
                return True
    return False

# ---- render: each "1" module → a red square IF inside heart OR structural ----
for r in range(N):
    for c in range(N):
        if not matrix[r][c]:
            continue
        x = PAD + c * MODULE
        y = PAD + r * MODULE
        cx = x + MODULE // 2
        cy = y + MODULE // 2
        # always keep structural patterns
        force = is_finder_area(r, c) or is_alignment(r, c)
        if not force and mask.getpixel((cx, cy)) < 128:
            continue
        draw.rectangle([x, y, x + MODULE, y + MODULE], fill=RED)

# ---- decorative dense heart outline (extra modules along edge) ----
def heart_outline_modules(scale_outer, step_units=0.6):
    out = []
    n = 220
    for i in range(n + 1):
        t = (i / n) * 2 * math.pi
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2*t)
              - 2 * math.cos(3*t) - math.cos(4*t))
        out.append((hcx + x * scale_outer, hcy + y * scale_outer))
    return out

for ring_scale in (heart_scale * 0.99, heart_scale * 0.96):
    pts = heart_outline_modules(ring_scale)
    for px, py in pts:
        ix = int((px - PAD) // MODULE)
        iy = int((py - PAD) // MODULE)
        # don't overlap structural patterns
        if 0 <= ix < N and 0 <= iy < N and not is_finder_area(iy, ix):
            x = PAD + ix * MODULE
            y = PAD + iy * MODULE
            draw.rectangle([x, y, x + MODULE, y + MODULE], fill=RED)

# ---- save raw and test decode ----
RAW = "qr_heart_raw.png"
img.save(RAW)
arr = cv2.imread(RAW)
det = cv2.QRCodeDetector()
data, *_ = det.detectAndDecode(arr)
print(f"raw decode: {data!r}")

# ---- finishing: composite onto cream card with title ----
W, H = SIZE, SIZE + 220
card = Image.new("RGB", (W, H), (255, 248, 242))
card.paste(img, (0, 0))

cd = ImageDraw.Draw(card)
try:
    fbig = ImageFont.truetype("C:/Windows/Fonts/Georgia.ttf", 64)
    fsm  = ImageFont.truetype("C:/Windows/Fonts/Georgia.ttf", 32)
except Exception:
    from PIL import ImageFont as IF
    fbig = IF.load_default()
    fsm  = IF.load_default()

cd.text((W // 2, SIZE + 70),  "scan me",                fill=(150, 30, 60), font=fbig, anchor="mm")
cd.text((W // 2, SIZE + 140), "untuk sebuah kejutan",   fill=(180, 80, 110), font=fsm,  anchor="mm")

OUT = "qrcode_love_heart.png"
card.save(OUT, "PNG", optimize=True)
print(f"wrote {OUT}  size={card.size}")

# verify final decode
arr2 = cv2.imread(OUT)
data2, *_ = det.detectAndDecode(arr2)
print(f"final decode: {data2!r}")

# also export hi-res
hires = card.resize((W * 2, H * 2), Image.LANCZOS)
hires.save("qrcode_love_heart_print.png", "PNG", optimize=True, dpi=(300, 300))
print(f"wrote qrcode_love_heart_print.png  ({hires.size[0]}x{hires.size[1]} px @ 300 DPI)")
