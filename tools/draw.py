"""Renders entry.png (run once with Pillow; main.py just copies the result)."""
import math
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W = H = 1024
F = "/usr/share/fonts/truetype/liberation/"
def font(name, size): return ImageFont.truetype(F + name, size)
BOLD, REG, NAR, SERIF = "LiberationSans-Bold.ttf", "LiberationSans-Regular.ttf", "LiberationSansNarrow-Bold.ttf", "LiberationSerif-Bold.ttf"

INK = (14, 16, 24)
PAPER = (240, 234, 220)
RED = (226, 54, 40)
ORANGE = (255, 140, 30)
random.seed(21112026)

img = Image.new("RGB", (W, H), INK)
d = ImageDraw.Draw(img)

# ---------- masthead ----------
d.rectangle([0, 0, W, 92], fill=PAPER)
d.text((32, 14), "THE WORLD ON EDGE", font=font(SERIF, 52), fill=INK)
d.text((W - 32, 22), "SATURDAY", font=font(BOLD, 22), fill=RED, anchor="ra")
d.text((W - 32, 50), "21 NOVEMBER 2026", font=font(BOLD, 26), fill=INK, anchor="ra")
d.rectangle([0, 92, W, 98], fill=RED)

# ---------- hero: Strait of Hormuz ----------
HT, HB = 98, 560
hero = Image.new("RGB", (W, HB - HT), (10, 24, 44))
hd = ImageDraw.Draw(hero)
hh = HB - HT
for y in range(hh):  # night sky / sea gradient
    t = y / hh
    hd.line([(0, y), (W, y)], fill=(int(12 + 30 * t), int(18 + 28 * t), int(40 + 30 * t)))
# land masses: Iran (top) and Musandam peninsula (bottom right)
hd.polygon([(0, 0), (W, 0), (W, 70), (860, 95), (720, 80), (560, 110), (420, 95), (260, 120), (120, 105), (0, 130)], fill=(34, 30, 28))
hd.polygon([(1024, 462), (1024, 230), (960, 250), (900, 300), (870, 360), (820, 400), (700, 430), (560, 462)], fill=(34, 30, 28))
hd.text((60, 30), "IRAN", font=font(BOLD, 30), fill=(110, 96, 84))
hd.text((900, 405), "OMAN", font=font(BOLD, 24), fill=(110, 96, 84))
hd.text((890, 380), "Khasab", font=font(REG, 16), fill=(150, 135, 120))
# shipping lane
for x in range(0, W, 36):
    hd.line([(x, 250 + 20 * math.sin(x / 140)), (x + 18, 250 + 20 * math.sin((x + 18) / 140))], fill=(70, 100, 140), width=2)

def tanker(cx, cy, s, burning):
    hull = [(cx - 90 * s, cy), (cx + 100 * s, cy), (cx + 80 * s, cy + 26 * s), (cx - 80 * s, cy + 26 * s)]
    hd.polygon(hull, fill=(20, 20, 24))
    hd.rectangle([cx + 40 * s, cy - 30 * s, cx + 78 * s, cy], fill=(28, 28, 34))
    hd.rectangle([cx - 70 * s, cy - 8 * s, cx + 30 * s, cy], fill=(40, 40, 46))
    if burning:
        glow = Image.new("RGBA", hero.size, (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        gd.ellipse([cx - 160 * s, cy - 150 * s, cx + 120 * s, cy + 40 * s], fill=(255, 110, 20, 120))
        glow = glow.filter(ImageFilter.GaussianBlur(40 * s))
        hero.paste(glow, (0, 0), glow)
        for i in range(60):
            fx = cx - 30 * s + random.gauss(0, 22 * s)
            fy = cy - abs(random.gauss(0, 45 * s))
            r = random.uniform(5, 16) * s
            col = random.choice([(255, 200, 60), ORANGE, RED, (255, 90, 20)])
            hd.ellipse([fx - r, fy - r, fx + r, fy + r], fill=col)
        for i in range(25):  # smoke
            sx = cx - 40 * s + i * 6 * s + random.gauss(0, 10)
            sy = cy - 80 * s - i * 9 * s
            r = (14 + i * 1.6) * s
            g = 60 + random.randint(0, 25)
            hd.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(g, g, g + 6))

tanker(300, 300, 1.25, True)
tanker(680, 235, 0.9, True)
# downed drone
dx, dy = 840, 150
hd.polygon([(dx - 60, dy), (dx + 60, dy - 6), (dx + 60, dy + 6)], fill=(170, 175, 185))
hd.line([(dx - 10, dy - 40), (dx + 20, dy + 40)], fill=(170, 175, 185), width=8)
hd.line([(dx + 40, dy - 30), (dx + 10, dy + 30)], fill=(170, 175, 185), width=5)
for k in range(5):
    hd.line([(dx + 60 + k * 14, dy - 8 - k * 12), (dx + 70 + k * 14, dy - 14 - k * 12)], fill=(120, 120, 130), width=3)
hd.line([(dx - 34, dy - 34), (dx + 34, dy + 34)], fill=RED, width=9)
hd.line([(dx - 34, dy + 34), (dx + 34, dy - 34)], fill=RED, width=9)
hd.text((dx, dy + 52), "US MQ-9 'downed'", font=font(BOLD, 16), fill=(220, 220, 230), anchor="ma")
img.paste(hero, (0, HT))

# hero headline
d.rectangle([0, 455, W, HB], fill=(0, 0, 0))
d.rectangle([32, 470, 140, 498], fill=RED)
d.text((86, 484), "TOP STORY", font=font(BOLD, 17), fill=PAPER, anchor="mm")
d.text((156, 466), "TANKERS HIT IN HORMUZ", font=font(BOLD, 44), fill=PAPER)
d.text((32, 514), "Two tankers struck off Oman  •  Iran claims it downed a US drone  •  Trump threatens war over 'dirty bomb' plot", font=font(REG, 17), fill=(205, 200, 190))
d.text((32, 536), "COP31 overtime  •  Russia's massive Ukraine strike spills into Poland  •  G-3 summit afterglow",
       font=font(REG, 17), fill=(150, 145, 140))

# ---------- tiles ----------
TILES_T = 572
cols, rows = 3, 2
gap = 12
tw = (W - 2 * 24 - (cols - 1) * gap) // cols
th = (H - TILES_T - 52 - (rows - 1) * gap) // rows

def tile(i, bg, title, sub, art):
    c, r = i % cols, i // cols
    x0 = 24 + c * (tw + gap)
    y0 = TILES_T + r * (th + gap)
    d.rounded_rectangle([x0, y0, x0 + tw, y0 + th], 10, fill=bg)
    art(x0, y0, x0 + tw, y0 + th - 70)
    d.text((x0 + 14, y0 + th - 66), title, font=font(BOLD, 22), fill=PAPER)
    yy = y0 + th - 38
    for line in sub:
        d.text((x0 + 14, yy), line, font=font(REG, 14), fill=(220, 215, 205))
        yy += 16

def art_cop(x0, y0, x1, y1):
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 + 6
    d.ellipse([cx - 42, cy - 42, cx + 42, cy + 42], fill=(40, 110, 160))
    d.polygon([(cx - 30, cy - 20), (cx - 5, cy - 34), (cx + 10, cy - 10), (cx - 10, cy + 8), (cx - 28, cy)], fill=(70, 150, 80))
    d.polygon([(cx + 12, cy + 6), (cx + 34, cy + 2), (cx + 28, cy + 30), (cx + 14, cy + 28)], fill=(70, 150, 80))
    # clock past deadline
    kx, ky = cx + 70, cy - 20
    d.ellipse([kx - 22, ky - 22, kx + 22, ky + 22], fill=PAPER)
    d.line([(kx, ky), (kx, ky - 15)], fill=INK, width=3)
    d.line([(kx, ky), (kx + 12, ky + 4)], fill=RED, width=3)
    # oil drop crossed
    ox, oy = cx - 72, cy - 14
    d.polygon([(ox, oy - 26), (ox - 15, oy + 2), (ox + 15, oy + 2)], fill=INK)
    d.ellipse([ox - 15, oy - 12, ox + 15, oy + 18], fill=INK)
    d.line([(ox - 22, oy - 26), (ox + 22, oy + 22)], fill=RED, width=4)

def art_ukraine(x0, y0, x1, y1):
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rectangle([x0 + 30, cy - 14, x1 - 30, cy + 14], fill=(0, 87, 183))
    d.rectangle([x0 + 30, cy + 14, x1 - 30, cy + 42], fill=(255, 215, 0))
    for k, (mx, my) in enumerate([(cx - 60, cy - 20), (cx - 5, cy - 28), (cx + 55, cy - 16)]):
        d.line([(mx - 30, my - 30), (mx, my)], fill=(230, 230, 230), width=6)
        d.polygon([(mx, my), (mx - 12, my - 2), (mx - 2, my - 12)], fill=RED)
    d.text((x1 - 34, y0 + 12), "PL", font=font(BOLD, 18), fill=RED, anchor="ra")

def art_g3(x0, y0, x1, y1):
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 + 4
    for dx, col, lab in [(-62, (60, 90, 200), "US"), (0, (220, 40, 40), "CN"), (62, (240, 240, 240), "RU")]:
        d.ellipse([cx + dx - 36, cy - 36, cx + dx + 36, cy + 36], outline=col, width=7)
        d.text((cx + dx, cy), lab, font=font(BOLD, 20), fill=col, anchor="mm")

def art_outage(x0, y0, x1, y1):
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    pts = [(x0 + 24, cy), (cx - 50, cy), (cx - 35, cy - 34), (cx - 15, cy + 34), (cx, cy - 10), (cx + 10, cy)]
    d.line(pts, fill=(80, 255, 140), width=4)
    d.line([(cx + 10, cy), (x1 - 24, cy)], fill=(80, 80, 80), width=4)
    d.text((cx + 60, cy - 34), "ERR", font=font(BOLD, 26), fill=RED, anchor="mm")
    d.text((cx + 60, cy + 30), "✈ $ ⚠", font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22), fill=(230, 230, 230), anchor="mm")

def art_icj(x0, y0, x1, y1):
    cx, cy = (x0 + x1) // 2, y0 + 22
    d.line([(cx, cy), (cx, y1 - 10)], fill=(220, 190, 110), width=5)
    d.line([(cx - 70, cy + 10), (cx + 70, cy + 10)], fill=(220, 190, 110), width=5)
    d.rectangle([cx - 30, y1 - 14, cx + 30, y1 - 6], fill=(220, 190, 110))
    for sx, drop in [(-70, 22), (70, 2)]:
        px, py = cx + sx, cy + 10
        d.line([(px, py), (px - 22, py + 40 + drop)], fill=(220, 190, 110), width=2)
        d.line([(px, py), (px + 22, py + 40 + drop)], fill=(220, 190, 110), width=2)
        d.pieslice([px - 28, py + 26 + drop, px + 28, py + 56 + drop], 0, 180, fill=(220, 190, 110))

def art_protest(x0, y0, x1, y1):
    for k, (px, txt) in enumerate([(x0 + 60, "RENT"), ((x0 + x1) // 2, "SCHOOLS"), (x1 - 60, "FUTURE")]):
        top = y0 + 20 + (k % 2) * 14
        d.line([(px, top + 30), (px, y1)], fill=(160, 120, 80), width=5)
        d.rectangle([px - 46, top, px + 46, top + 36], fill=PAPER)
        d.text((px, top + 18), txt, font=font(NAR, 17), fill=INK, anchor="mm")

tile(0, (30, 70, 56), "COP31 goes to overtime", ["Antalya talks stall as draft deal", "drops all mention of fossil fuels"], art_cop)
tile(1, (36, 40, 70), "Russia pounds Ukraine", ["Hundreds of drones & missiles; strays", "land in Poland; Denmark expels attaché"], art_ukraine)
tile(2, (70, 30, 34), "After the 'G-3' summit", ["Trump, Xi, Putin met in Shenzhen;", "deal on humans-in-the-loop military AI"], art_g3)
tile(3, (40, 40, 44), "US outages, cyber chief out", ["Banks, flights, systems down; Trump", "fires National Cyber Director"], art_outage)
tile(4, (60, 48, 28), "Myanmar guilty of genocide", ["ICJ landmark ruling on the Rohingya", "reverberates around the world"], art_icj)
tile(5, (76, 40, 70), "Europe's youth march on", ["Protests over rent, schools and", "military spending enter the weekend"], art_protest)

# footer
d.text((W // 2, H - 26), "Also: UK and EU seal youth-mobility & food-trade deal  •  Basra pipeline blast kills 8  •  Gaza braces for winter",
       font=font(REG, 15), fill=(170, 165, 155), anchor="mm")

out = Path(__file__).resolve().parent.parent / "entry.png"
img.save(out, optimize=True)
print(out, out.stat().st_size)
