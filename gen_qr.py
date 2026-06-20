import qrcode
from PIL import Image, ImageDraw, ImageFont
import math

data = "http://120.118.242.117:8080/index.html?skip"

qr = qrcode.QRCode(
    version=5,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=15,
    border=4,
)
qr.add_data(data)
qr.make(fit=True)

img = qr.make_image(fill_color="#4a1230", back_color="#ffffff").convert('RGBA')
w, h = img.size

# Create a transparent overlay for the heart
overlay = Image.new('RGBA', img.size, (255,255,255,0))
draw = ImageDraw.Draw(overlay)

def draw_heart(d, cx, cy, size, fill, outline=None, width=0):
    # parametric equation of heart:
    # x = 16 sin^3(t)
    # y = 13 cos(t) - 5 cos(2t) - 2 cos(3t) - cos(4t)
    points = []
    for t in range(0, 360, 1):
        rad = math.radians(t)
        x = 16 * math.sin(rad)**3
        y = 13 * math.cos(rad) - 5 * math.cos(2*rad) - 2 * math.cos(3*rad) - math.cos(4*rad)
        # Invert Y because image coordinates go down
        points.append((cx + x * size, cy - y * size))
    d.polygon(points, fill=fill, outline=outline, width=width)

cx, cy = w // 2, h // 2
# White outline
draw_heart(draw, cx, cy-10, size=5.5, fill="white")
# Pink heart
draw_heart(draw, cx, cy-10, size=4.5, fill="#e87a96")

# Composite
img = Image.alpha_composite(img, overlay)

# Save
out_path = r"c:\Claude\Project\ucapan-5th-bersama\qrcode_love.png"
img.save(out_path)
print("QR Code generated at:", out_path)
