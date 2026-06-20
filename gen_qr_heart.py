"""Generate a printable pink heart-shaped QR tag for the anniversary site."""
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

URL = "https://muktihadi5641-cpu.github.io/ucapan-5th-bersama/"
OUT = "qrcode_love.png"

# ---------- palette ----------
PINK        = (255, 168, 192, 255)   # heart fill
PINK_DEEP   = (215, 110, 145, 255)   # heart outline
PINK_LIGHT  = (255, 220, 232, 255)   # bg blush
CREAM       = (255, 248, 242, 255)   # canvas
WINE        = (90, 42, 58, 255)      # QR + text
ROSE        = (255, 110, 145, 255)   # accent

# ---------- canvas ----------
W, H = 1200, 1500
img = Image.new("RGBA", (W, H), CREAM)

# soft radial blush behind heart
blush = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bd = ImageDraw.Draw(blush)
for r in range(680, 0, -40):
    a = int(40 * (1 - r/680))
    bd.ellipse([W//2 - r, H//2 + 40 - r, W//2 + r, H//2 + 40 + r],
               fill=(255, 200, 220, a))
blush = blush.filter(ImageFilter.GaussianBlur(30))
img = Image.alpha_composite(img, blush)

# ---------- heart polygon ----------
def heart_path(cx, cy, scale, n=600):
    pts = []
    for i in range(n + 1):
        t = (i / n) * 2 * math.pi
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2*t)
              - 2 * math.cos(3*t) - math.cos(4*t))
        pts.append((cx + x * scale, cy + y * scale))
    return pts

heart_scale = 36
hcx, hcy    = W // 2, H // 2 + 60
heart       = heart_path(hcx, hcy, heart_scale)

# drop shadow
shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.polygon([(p[0] + 6, p[1] + 14) for p in heart], fill=(150, 60, 100, 110))
shadow = shadow.filter(ImageFilter.GaussianBlur(14))
img = Image.alpha_composite(img, shadow)

draw = ImageDraw.Draw(img)

# heart fill
draw.polygon(heart, fill=PINK)

# heart outline (thick line)
draw.line(heart + [heart[0]], fill=PINK_DEEP, width=8)

# inner gentle highlight (small lighter heart on top-left, mimics gloss)
gloss = heart_path(hcx - 80, hcy - 60, heart_scale * 0.35)
draw.polygon(gloss, fill=(255, 220, 232, 120))

# ---------- QR code ----------
qr = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=24,
    border=2,
)
qr.add_data(URL)
qr.make(fit=True)
qr_img = qr.make_image(fill_color=WINE[:3], back_color="white").convert("RGBA")

# white rounded card holding the QR (sits in the upper-wider part of the heart)
qr_size = 600
qr_x = (W - qr_size) // 2
qr_y = hcy - 360                        # nudged up to sit where heart is widest
pad  = 26
draw.rounded_rectangle(
    [qr_x - pad, qr_y - pad, qr_x + qr_size + pad, qr_y + qr_size + pad],
    radius=32, fill="white", outline=PINK_DEEP, width=5,
)

qr_resized = qr_img.resize((qr_size, qr_size), Image.LANCZOS)
img.alpha_composite(qr_resized, (qr_x, qr_y))

# tiny pink heart in the dead-center of the QR (kept tiny so it doesn't block
# scanning — QR high error correction tolerates this)
small = heart_path(W // 2, qr_y + qr_size // 2, 2.6)
draw.polygon(small, fill=ROSE)

# ---------- text ----------
def load_font(name, size):
    candidates = [
        f"C:/Windows/Fonts/{name}",
        f"/usr/share/fonts/truetype/dejavu/{name}",
        f"/Library/Fonts/{name}",
    ]
    for p in candidates:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            pass
    return ImageFont.load_default()

font_big  = load_font("Georgia.ttf", 64)
font_mid  = load_font("Georgia.ttf", 38)
font_sm   = load_font("arial.ttf",   28)

text_cy = qr_y + qr_size + 110
draw.text((W // 2, text_cy), "scan me", fill=WINE, font=font_big, anchor="mm")

# subtitle + a vector heart (so we don't rely on emoji font glyphs)
sub = "untuk sebuah kejutan"
draw.text((W // 2, text_cy + 64), sub, fill=PINK_DEEP, font=font_mid, anchor="mm")

bbox = font_mid.getbbox(sub)
sub_w = bbox[2] - bbox[0]
heart_after = heart_path(W // 2 + sub_w // 2 + 26, text_cy + 64, 1.4)
draw.polygon(heart_after, fill=PINK_DEEP)

draw.text((W // 2, H - 60), "from yours, always & forever",
          fill=PINK_DEEP, font=font_sm, anchor="mm")

# ---------- save ----------
img.save(OUT, "PNG", optimize=True)
print(f"wrote {OUT}  ({img.size[0]}x{img.size[1]} px)")

# also export a high-res 300-DPI variant for crisp print
hires = img.resize((W * 2, H * 2), Image.LANCZOS)
hires.save("qrcode_love_print.png", "PNG", optimize=True, dpi=(300, 300))
print(f"wrote qrcode_love_print.png  ({hires.size[0]}x{hires.size[1]} px @ 300 DPI)")
