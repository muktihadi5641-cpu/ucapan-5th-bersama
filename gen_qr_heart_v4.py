"""v4: a bold pink heart silhouette wrapped around a square QR.
QR stays square (scannable). The heart shape + scattered ornaments around it
make the whole composition read as a heart — QR is the focal jewel."""
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math, cv2

URL = "https://muktihadi5641-cpu.github.io/ucapan-5th-bersama/"

# ---------- palette ----------
PINK_L  = (255, 220, 232)
PINK    = (255, 158, 184)
PINK_D  = (215, 110, 145)
PINK_DD = (180, 60, 100)
CREAM   = (255, 248, 242)
WINE    = (90, 42, 58)
ROSE    = (255, 110, 145)

W, H = 1400, 1700
img  = Image.new("RGBA", (W, H), CREAM + (255,))

# ---------- soft radial blush behind the heart ----------
blush = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bd = ImageDraw.Draw(blush)
for r in range(800, 0, -50):
    a = int(45 * (1 - r / 800))
    bd.ellipse([W//2 - r, H//2 + 50 - r, W//2 + r, H//2 + 50 + r],
               fill=(255, 200, 220, a))
blush = blush.filter(ImageFilter.GaussianBlur(40))
img = Image.alpha_composite(img, blush)

# ---------- heart polygon helper ----------
def heart_path(cx, cy, scale, n=600):
    pts = []
    for i in range(n + 1):
        t = (i / n) * 2 * math.pi
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2*t)
              - 2 * math.cos(3*t) - math.cos(4*t))
        pts.append((cx + x * scale, cy + y * scale))
    return pts

heart_scale = 42
hcx, hcy    = W // 2, H // 2 + 60
heart_pts   = heart_path(hcx, hcy, heart_scale)

# drop shadow
shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(shadow).polygon(
    [(p[0] + 10, p[1] + 18) for p in heart_pts], fill=(150, 60, 100, 110))
shadow = shadow.filter(ImageFilter.GaussianBlur(18))
img = Image.alpha_composite(img, shadow)

draw = ImageDraw.Draw(img)

# heart fill + soft top-left highlight (mimic 3D gloss)
draw.polygon(heart_pts, fill=PINK + (255,))
gloss = heart_path(hcx - 60, hcy - 60, heart_scale * 0.55)
draw.polygon(gloss, fill=(255, 210, 226, 160))

# thick rose outline
for w in (12, 10, 8, 6, 4):
    draw.line(heart_pts + [heart_pts[0]], fill=PINK_D + (255,), width=w)

# ---------- QR ----------
qr = qrcode.QRCode(
    error_correction=ERROR_CORRECT_H,
    box_size=20,
    border=2,
)
qr.add_data(URL)
qr.make(fit=True)
qr_img = qr.make_image(fill_color=WINE, back_color="white").convert("RGBA")

# place QR centered, slightly above heart center so heart-point shows below
qr_size = 680
qr_x = (W - qr_size) // 2
qr_y = hcy - qr_size // 2 - 50

# white card under QR
pad = 28
card_box = [qr_x - pad, qr_y - pad, qr_x + qr_size + pad, qr_y + qr_size + pad]
draw.rounded_rectangle(card_box, radius=36, fill="white",
                       outline=PINK_D + (255,), width=6)
# subtle inner border
inner = [card_box[0] + 8, card_box[1] + 8, card_box[2] - 8, card_box[3] - 8]
draw.rounded_rectangle(inner, radius=28,
                       outline=PINK_L + (255,), width=2)

qr_resized = qr_img.resize((qr_size, qr_size), Image.LANCZOS)
img.alpha_composite(qr_resized, (qr_x, qr_y))

# tiny pink heart at QR center (H-correction handles this)
mini = heart_path(W // 2, qr_y + qr_size // 2, 3.2)
draw.polygon(mini, fill=ROSE + (235,))

# ---------- decorative scattered hearts ----------
decor = [
    ( 110,  240, 11, PINK_D),
    (1290,  240, 11, PINK_D),
    ( 170, 1380,  8, PINK_D),
    (1230, 1380,  8, PINK_D),
    (  60,  820,  5, PINK_DD),
    (1340,  820,  5, PINK_DD),
    (W//2 - 240,  220, 6, PINK_DD),
    (W//2 + 240,  220, 6, PINK_DD),
    (W//2 - 360, 1380, 4, PINK_DD),
    (W//2 + 360, 1380, 4, PINK_DD),
]
for cx, cy, s, col in decor:
    pts = heart_path(cx, cy, s)
    draw.polygon(pts, fill=col + (255,))

# four-pointed sparkles
spark = [(240, 700, 4), (1160, 700, 4),
         (340, 1320, 3), (1060, 1320, 3),
         (W//2 - 480, 540, 2), (W//2 + 480, 540, 2)]
for cx, cy, r in spark:
    draw.polygon([
        (cx, cy - r*4), (cx + r, cy - r), (cx + r*4, cy),
        (cx + r, cy + r), (cx, cy + r*4), (cx - r, cy + r),
        (cx - r*4, cy), (cx - r, cy - r),
    ], fill=PINK_D + (255,))

# ---------- text ----------
def load_font(name, size):
    for p in (f"C:/Windows/Fonts/{name}",
              f"/usr/share/fonts/truetype/dejavu/{name}",
              f"/Library/Fonts/{name}"):
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            pass
    return ImageFont.load_default()

font_big = load_font("Georgia.ttf", 72)
font_mid = load_font("Georgia.ttf", 38)
font_sm  = load_font("arial.ttf", 30)

text_cy = qr_y + qr_size + 130
draw.text((W // 2, text_cy), "scan me",
          fill=WINE + (255,), font=font_big, anchor="mm")

sub = "untuk sebuah kejutan"
draw.text((W // 2, text_cy + 68), sub,
          fill=PINK_D + (255,), font=font_mid, anchor="mm")
# tiny heart after the subtitle text
bbox  = font_mid.getbbox(sub)
sub_w = bbox[2] - bbox[0]
trail = heart_path(W // 2 + sub_w // 2 + 28, text_cy + 68, 1.8)
draw.polygon(trail, fill=PINK_D + (255,))

draw.text((W // 2, H - 80), "from yours, always & forever",
          fill=PINK_D + (255,), font=font_sm, anchor="mm")

# ---------- save + verify scan ----------
OUT = "qrcode_love.png"
img.convert("RGB").save(OUT, "PNG", optimize=True)

det  = cv2.QRCodeDetector()
data = det.detectAndDecode(cv2.imread(OUT))[0]
print(f"saved {OUT}  size={img.size}  decode={data!r}")

hires = img.resize((W * 2, H * 2), Image.LANCZOS)
hires.convert("RGB").save("qrcode_love_print.png", "PNG",
                          optimize=True, dpi=(300, 300))
print(f"saved qrcode_love_print.png  ({hires.size[0]}x{hires.size[1]} @ 300 DPI)")
