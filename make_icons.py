"""Generate PWA icons: BK-style radiant sun (orange-red rays, yellow core). ASCII-only source."""
from PIL import Image, ImageDraw
import math

WHITE  = (255, 255, 255)
CENTER = (252, 206, 84)    # warm yellow (inner)
EDGE   = (214, 40, 18)     # deep red-orange (outer)
CORE   = (255, 248, 214)   # bright core glow

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def draw_sun(size, pad, rays=22, ray_fill=0.58):
    ss = 4
    S = size * ss
    img = Image.new("RGB", (S, S), WHITE)
    d = ImageDraw.Draw(img)
    c = S / 2
    R = S * (0.5 - pad)
    # radial gradient disk via concentric circles (edge=red -> center=yellow)
    steps = int(R)
    for i in range(steps, 0, -1):
        t = i / steps                 # 1 at edge, 0 at center
        d.ellipse([c - i, c - i, c + i, c + i], fill=lerp(CENTER, EDGE, t))
    # carve gaps between rays (white wedges from center) -> triangular rays widening outward
    gap = (2 * math.pi / rays) * (1 - ray_fill)
    Rout = R * 1.08
    for k in range(rays):
        a = (k + 0.5) * (2 * math.pi / rays)   # gap center (between two rays)
        a1, a2 = a - gap / 2, a + gap / 2
        d.polygon([
            (c, c),
            (c + math.cos(a1) * Rout, c + math.sin(a1) * Rout),
            (c + math.cos(a2) * Rout, c + math.sin(a2) * Rout),
        ], fill=WHITE)
    # bright core (hides center convergence)
    rc = S * 0.11
    d.ellipse([c - rc, c - rc, c + rc, c + rc], fill=CORE)
    rc2 = S * 0.045
    d.ellipse([c - rc2, c - rc2, c + rc2, c + rc2], fill=(255, 255, 245))
    return img.resize((size, size), Image.LANCZOS)

for sz in (192, 512):
    draw_sun(sz, 0.06).save(f"icon-{sz}.png")
draw_sun(512, 0.20).save("icon-512-maskable.png")   # extra safe-zone padding
print("sun icons written")
