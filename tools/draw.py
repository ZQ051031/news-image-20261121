"""Draws entry.png: a 1024x1024 front-page poster summing up the world's news
of Saturday 21 November 2026. Run once with Pillow; main.py copies the result.
Authored for the make.fun news-image-20261121 bounty.
"""
import math
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W = H = 1024
FONT_DIR = "/usr/share/fonts/truetype/liberation/"
DEJAVU_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SERIF = "LiberationSerif-Bold.ttf"
SANS_B = "LiberationSans-Bold.ttf"
SANS_R = "LiberationSans-Regular.ttf"
SANS_N = "LiberationSansNarrow-Bold.ttf"

# palette
INK = (14, 16, 24)          # near-black navy (page background)
PAPER = (240, 234, 220)     # warm newsprint
PAPER_DIM = (205, 200, 190)
MUTED = (150, 145, 140)
RED = (226, 54, 40)
ORANGE = (255, 140, 30)
GOLD = (220, 190, 110)
SEA_TOP = (12, 18, 40)
SEA_BOT = (42, 46, 70)
LAND = (34, 30, 28)
LAND_LBL = (110, 96, 84)

random.seed(21112026)

canvas = Image.new("RGB", (W, H), INK)
d = ImageDraw.Draw(canvas)


def text_wrap(draw, words, font, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for w in words.split():
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def block(draw, x, y, text, font, fill, max_w, leading):
    """Draw a wrapped paragraph; returns the y after the last line."""
    for line in text_wrap(draw, text, font, max_w):
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 90], fill=PAPER)
d.text((30, 12), "THE WORLD ON EDGE", font=load(SERIF, 50), fill=INK)
d.text((W - 30, 20), "SATURDAY", font=load(SANS_B, 21), fill=RED, anchor="ra")
d.text((W - 30, 48), "21 NOVEMBER 2026", font=load(SANS_B, 25), fill=INK, anchor="ra")
d.rectangle([0, 90, W, 96], fill=RED)


# ------------------------------------------------------------- hero: Hormuz
HERO_T, HERO_B = 96, 556
hero_h = HERO_B - HERO_T
hero = Image.new("RGB", (W, hero_h), SEA_TOP)
hd = ImageDraw.Draw(hero)

# night sea: vertical gradient, darker at top
for yy in range(hero_h):
    t = yy / hero_h
    hd.line([(0, yy), (W, yy)],
            fill=(int(SEA_TOP[0] + (SEA_BOT[0] - SEA_TOP[0]) * t),
                  int(SEA_TOP[1] + (SEA_BOT[1] - SEA_TOP[1]) * t),
                  int(SEA_TOP[2] + (SEA_BOT[2] - SEA_TOP[2]) * t)))

# land: Iran along the top edge, Oman's Musandam peninsula bottom-right
hd.polygon([(0, 0), (W, 0), (W, 64), (880, 88), (700, 74), (520, 104),
            (360, 88), (200, 112), (80, 100), (0, 124)], fill=LAND)
hd.polygon([(W, hero_h), (W, 218), (968, 240), (912, 292), (872, 352),
            (824, 392), (700, 424), (560, hero_h)], fill=LAND)
hd.text((56, 26), "IRAN", font=load(SANS_B, 28), fill=LAND_LBL)
hd.text((898, 396), "OMAN", font=load(SANS_B, 23), fill=LAND_LBL)
hd.text((884, 372), "Khasab", font=load(SANS_R, 15), fill=(150, 135, 120))
hd.text((W // 2, hero_h - 34), "STRAIT OF HORMUZ",
        font=load(SANS_B, 15), fill=(90, 120, 160), anchor="ma")

# shipping lane: a dashed sine curve across the strait
for xx in range(0, W, 34):
    x2 = xx + 17
    y1 = 244 + 18 * math.sin(xx / 130)
    y2 = 244 + 18 * math.sin(x2 / 130)
    hd.line([(xx, y1), (x2, y2)], fill=(70, 100, 140), width=2)


def draw_tanker(cx, cy, s, on_fire):
    """A crude-oil tanker seen side-on; on_fire adds glow, flames, smoke."""
    hull = [(cx - 92 * s, cy), (cx + 102 * s, cy),
            (cx + 82 * s, cy + 26 * s), (cx - 82 * s, cy + 26 * s)]
    hd.polygon(hull, fill=(18, 18, 22))
    hd.rectangle([cx + 42 * s, cy - 30 * s, cx + 80 * s, cy], fill=(28, 28, 34))
    hd.rectangle([cx - 72 * s, cy - 8 * s, cx + 30 * s, cy], fill=(42, 42, 48))
    hd.rectangle([cx - 92 * s, cy - 4 * s, cx + 102 * s, cy + 2 * s],
                 fill=(60, 30, 26))
    if not on_fire:
        return
    glow = Image.new("RGBA", hero.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([cx - 150 * s, cy - 140 * s, cx + 130 * s, cy + 50 * s],
               fill=(255, 110, 20, 110))
    glow = glow.filter(ImageFilter.GaussianBlur(int(38 * s)))
    hero.paste(glow, (0, 0), glow)
    for _ in range(55):
        fx = cx - 25 * s + random.gauss(0, 24 * s)
        fy = cy - abs(random.gauss(0, 48 * s))
        r = random.uniform(5, 15) * s
        col = random.choice([(255, 200, 60), ORANGE, RED, (255, 90, 20)])
        hd.ellipse([fx - r, fy - r, fx + r, fy + r], fill=col)
    for i in range(22):
        sx = cx - 30 * s + i * 6 * s + random.gauss(0, 9)
        sy = cy - 84 * s - i * 9 * s
        r = (13 + i * 1.5) * s
        g = 58 + random.randint(0, 26)
        hd.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(g, g, g + 6))


draw_tanker(300, 296, 1.22, True)
draw_tanker(688, 232, 0.88, True)


def draw_downed_drone(dx, dy):
    """A US MQ-9 silhouette, crossed out in red, with a caption."""
    hd.polygon([(dx - 58, dy), (dx + 58, dy - 6), (dx + 58, dy + 6)],
               fill=(170, 175, 185))
    hd.line([(dx - 8, dy - 38), (dx + 18, dy + 38)], fill=(170, 175, 185), width=8)
    hd.line([(dx + 38, dy - 28), (dx + 8, dy + 28)], fill=(170, 175, 185), width=5)
    for k in range(4):
        hd.line([(dx + 58 + k * 13, dy - 6 - k * 11),
                 (dx + 68 + k * 13, dy - 12 - k * 11)],
                fill=(120, 120, 130), width=3)
    hd.line([(dx - 32, dy - 32), (dx + 32, dy + 32)], fill=RED, width=9)
    hd.line([(dx - 32, dy + 32), (dx + 32, dy - 32)], fill=RED, width=9)
    hd.text((dx, dy + 50), "US MQ-9 'downed'", font=load(SANS_B, 15),
            fill=(220, 220, 230), anchor="ma")


draw_downed_drone(838, 148)
canvas.paste(hero, (0, HERO_T))


# ---------------------------------------------------------- headline band
BAND_T, BAND_B = 452, HERO_B
d.rectangle([0, BAND_T, W, BAND_B], fill=(0, 0, 0))
d.rectangle([30, BAND_T + 14, 138, BAND_T + 42], fill=RED)
d.text((84, BAND_T + 28), "TOP STORY", font=load(SANS_B, 16), fill=PAPER, anchor="mm")
d.text((152, BAND_T + 10), "TANKERS HIT IN HORMUZ", font=load(SANS_B, 42), fill=PAPER)
d.text((30, BAND_T + 58),
       "Second tanker struck off Oman on Saturday  •  Iran says it downed a US drone  •  US–Iran talks stall",
       font=load(SANS_R, 16), fill=PAPER_DIM)
d.text((30, BAND_T + 80),
       "COP31 overtime  •  Russia's huge Ukraine strike spills into Poland  •  G-3 summit afterglow",
       font=load(SANS_R, 16), fill=MUTED)

# ------------------------------------------------------------------- tiles
TILES_T = 568
COLS, ROWS = 3, 2
GAP = 12
MARGIN = 24
TW = (W - 2 * MARGIN - (COLS - 1) * GAP) // COLS
TH = (H - TILES_T - 48 - (ROWS - 1) * GAP) // ROWS
ART_H = TH - 72


def tile(i, bg, title, lines, art):
    c, r = i % COLS, i // COLS
    x0 = MARGIN + c * (TW + GAP)
    y0 = TILES_T + r * (TH + GAP)
    d.rounded_rectangle([x0, y0, x0 + TW, y0 + TH], 10, fill=bg)
    art(x0, y0, x0 + TW, y0 + ART_H)
    d.text((x0 + 13, y0 + ART_H + 6), title, font=load(SANS_B, 21), fill=PAPER)
    yy = y0 + ART_H + 34
    for ln in lines:
        d.text((x0 + 13, yy), ln, font=load(SANS_R, 13), fill=(220, 215, 205))
        yy += 16


def art_cop(x0, y0, x1, y1):
    """A warming globe with a clock running past the deadline."""
    cx, cy = (x0 + x1) // 2 - 30, (y0 + y1) // 2 + 4
    d.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], fill=(40, 110, 160))
    d.polygon([(cx - 28, cy - 18), (cx - 4, cy - 32), (cx + 10, cy - 8),
               (cx - 8, cy + 10), (cx - 26, cy + 2)], fill=(70, 150, 80))
    d.polygon([(cx + 12, cy + 8), (cx + 32, cy + 4), (cx + 26, cy + 28),
               (cx + 12, cy + 26)], fill=(70, 150, 80))
    kx, ky = cx + 74, cy - 18
    d.ellipse([kx - 21, ky - 21, kx + 21, ky + 21], fill=PAPER)
    d.line([(kx, ky), (kx, ky - 14)], fill=INK, width=3)
    d.line([(kx, ky), (kx + 11, ky + 4)], fill=RED, width=3)
    ox, oy = cx + 72, cy + 22
    d.polygon([(ox, oy - 24), (ox - 14, oy + 2), (ox + 14, oy + 2)], fill=INK)
    d.ellipse([ox - 14, oy - 11, ox + 14, oy + 17], fill=INK)
    d.line([(ox - 20, oy - 24), (ox + 20, oy + 20)], fill=RED, width=4)


def art_ukraine(x0, y0, x1, y1):
    """Ukrainian flag with incoming missile streaks and a Poland marker."""
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rectangle([x0 + 28, cy - 12, x1 - 28, cy + 12], fill=(0, 87, 183))
    d.rectangle([x0 + 28, cy + 12, x1 - 28, cy + 38], fill=(255, 215, 0))
    for mx, my in [(cx - 58, cy - 18), (cx - 4, cy - 26), (cx + 54, cy - 14)]:
        d.line([(mx - 28, my - 28), (mx, my)], fill=(235, 235, 235), width=6)
        d.polygon([(mx, my), (mx - 11, my - 2), (mx - 2, my - 11)], fill=RED)
    d.text((x1 - 30, y0 + 10), "PL", font=load(SANS_B, 17), fill=RED, anchor="ra")


def art_g3(x0, y0, x1, y1):
    """Three linked rings: Washington, Beijing, Moscow."""
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 + 4
    for dx, col, lab in [(-60, (60, 90, 200), "US"),
                         (0, (220, 40, 40), "CN"),
                         (60, (240, 240, 240), "RU")]:
        d.ellipse([cx + dx - 34, cy - 34, cx + dx + 34, cy + 34],
                  outline=col, width=7)
        d.text((cx + dx, cy), lab, font=load(SANS_B, 19), fill=col, anchor="mm")


def art_outage(x0, y0, x1, y1):
    """A power line that snaps mid-span; the grid goes dark after it."""
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    pts = [(x0 + 22, cy), (cx - 48, cy), (cx - 34, cy - 32),
           (cx - 14, cy + 32), (cx, cy - 8), (cx + 8, cy)]
    d.line(pts, fill=(80, 255, 140), width=4)
    d.line([(cx + 8, cy), (x1 - 22, cy)], fill=(80, 80, 80), width=4)
    d.text((cx + 58, cy - 32), "ERR", font=load(SANS_B, 25), fill=RED, anchor="mm")
    d.text((cx + 58, cy + 28), "✈ $ ⚠",
           font=ImageFont.truetype(DEJAVU_BOLD, 21),
           fill=(230, 230, 230), anchor="mm")


def art_icj(x0, y0, x1, y1):
    """Scales of justice, tipped toward the victims."""
    cx, cy = (x0 + x1) // 2, y0 + 20
    d.line([(cx, cy), (cx, y1 - 8)], fill=GOLD, width=5)
    d.line([(cx - 66, cy + 8), (cx + 66, cy + 8)], fill=GOLD, width=5)
    d.rectangle([cx - 28, y1 - 12, cx + 28, y1 - 4], fill=GOLD)
    for sx, drop in [(-66, 20), (66, 2)]:
        px, py = cx + sx, cy + 8
        d.line([(px, py), (px - 20, py + 38 + drop)], fill=GOLD, width=2)
        d.line([(px, py), (px + 20, py + 38 + drop)], fill=GOLD, width=2)
        d.pieslice([px - 26, py + 24 + drop, px + 26, py + 54 + drop],
                   0, 180, fill=GOLD)


def art_ukeu(x0, y0, x1, y1):
    """EU stars beside a Union Jack, with the youth-mobility figure."""
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 6
    d.ellipse([cx - 78, cy - 34, cx - 6, cy + 34], fill=(0, 51, 153))
    for k in range(12):
        a = -math.pi / 2 + k * math.pi / 6
        sx, sy = cx - 42 + 24 * math.cos(a), cy + 24 * math.sin(a)
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 204, 0))
    d.rectangle([cx + 6, cy - 34, cx + 78, cy + 34], fill=(1, 33, 105))
    d.line([(cx + 6, cy - 34), (cx + 78, cy + 34)], fill=PAPER, width=5)
    d.line([(cx + 6, cy + 34), (cx + 78, cy - 34)], fill=PAPER, width=5)
    d.line([(cx + 42, cy - 34), (cx + 42, cy + 34)], fill=PAPER, width=8)
    d.line([(cx + 6, cy), (cx + 78, cy)], fill=PAPER, width=8)
    d.text((cx, y1 - 14), "100,000 a year", font=load(SANS_B, 16),
           fill=PAPER, anchor="ma")


tile(0, (30, 70, 56), "COP31 goes to overtime",
     ["Antalya talks stall as draft deal", "drops all mention of fossil fuels"], art_cop)
tile(1, (36, 40, 70), "Russia pounds Ukraine",
     ["400+ drones, 110+ missiles; strays", "land in Poland; Denmark expels attaché"], art_ukraine)
tile(2, (70, 30, 34), "After the 'G-3' summit",
     ["Trump, Xi, Putin met in Shenzhen;", "deal on humans-in-the-loop military AI"], art_g3)
tile(3, (40, 40, 44), "US outages, cyber chief out",
     ["Banks, flights, systems down; Trump", "fires National Cyber Director"], art_outage)
tile(4, (60, 48, 28), "Myanmar guilty of genocide",
     ["ICJ landmark ruling on the Rohingya;", "9–6, first time a state is found guilty"], art_icj)
tile(5, (28, 58, 74), "UK and EU seal reset deal",
     ["Youth mobility for 100,000 a year;", "food trade eased, carbon markets linked"], art_ukeu)

# ------------------------------------------------------------------- footer
d.text((W // 2, H - 24),
       "Also: Basra pipeline blast kills at least 4  •  US–Iran talks stall as Hormuz attacks continue  •  NATO chief to visit Warsaw",
       font=load(SANS_R, 14), fill=(170, 165, 155), anchor="mm")

out = Path(__file__).resolve().parent.parent / "entry.png"
img = canvas
img.save(out, optimize=True)
print(out, out.stat().st_size)

