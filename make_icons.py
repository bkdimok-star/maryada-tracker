"""Generate PWA icons: gold 'soul point of light' on indigo. ASCII-only source."""
from PIL import Image, ImageDraw
import math

BG1 = (27, 27, 47)    # indigo
BG2 = (42, 42, 74)    # lighter indigo
GOLD = (232, 160, 75)
GOLD_HI = (242, 181, 107)

def radial_bg(size):
    img = Image.new("RGB", (size, size), BG1)
    px = img.load()
    c = size / 2
    maxd = math.hypot(c, c)
    for y in range(size):
        for x in range(size):
            d = math.hypot(x - c, y - c) / maxd
            t = min(1.0, d)
            px[x, y] = (
                int(BG2[0] + (BG1[0]-BG2[0])*t),
                int(BG2[1] + (BG1[1]-BG2[1])*t),
                int(BG2[2] + (BG1[2]-BG2[2])*t),
            )
    return img

def draw_star(size, pad_ratio):
    # supersample for smooth edges
    ss = 4
    S = size * ss
    img = radial_bg(S).convert("RGBA")
    d = ImageDraw.Draw(img)
    c = S / 2
    R = S * (0.5 - pad_ratio)           # outer ray reach
    r_core = S * 0.10                    # central bright dot
    # 12 rays (4 long cardinal, 4 mid diagonal, 4 short half) — radiant point of light
    for i in range(12):
        ang = math.radians(i * 30)
        if i % 3 == 0:   length, w = R, S*0.018
        elif i % 3 == 1: length, w = R*0.70, S*0.012
        else:            length, w = R*0.52, S*0.009
        x2 = c + math.cos(ang) * length
        y2 = c + math.sin(ang) * length
        d.line([(c, c), (x2, y2)], fill=GOLD, width=max(2, int(w)))
    # subtle glow halo (light, reads as radiance not a disk)
    for rr, alpha in [(r_core*2.4, 22), (r_core*1.7, 45)]:
        d.ellipse([c-rr, c-rr, c+rr, c+rr], fill=(232,160,75,alpha))
    # bright core
    d.ellipse([c-r_core, c-r_core, c+r_core, c+r_core], fill=GOLD)
    rc2 = r_core*0.5
    d.ellipse([c-rc2, c-rc2, c+rc2, c+rc2], fill=GOLD_HI)
    return img.convert("RGB").resize((size, size), Image.LANCZOS)

for sz in (192, 512):
    draw_star(sz, 0.12).save(f"icon-{sz}.png")
draw_star(512, 0.22).save("icon-512-maskable.png")  # extra safe-zone padding
print("icons written")
