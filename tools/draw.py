"""Render entry.png for the make.fun news-image-20261121 bounty.

Builds a 1024x1024 newspaper front page summing up the world's news of
Saturday 21 November 2026. Run with Pillow; main.py then copies the
finished image to the grader's output directory.
"""

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

SIDE = 1024
LIBERATION = "/usr/share/fonts/truetype/liberation/"
DEJAVU_HEAVY = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# -- palette ---------------------------------------------------------------
PAGE_BG = (14, 16, 24)       # near-black navy behind the tiles
NEWS = (240, 234, 220)       # warm newsprint
NEWS_FAINT = (205, 200, 190)
GREY = (150, 145, 140)
SCARLET = (226, 54, 40)
EMBER = (255, 140, 30)
BRASS = (220, 190, 110)
SEA_HIGH = (12, 18, 40)
SEA_LOW = (42, 46, 70)
SHORE = (34, 30, 28)
SHORE_TAG = (110, 96, 84)

random.seed(21112026)


class Type:
    """Font loading, by family name and point size."""

    SERIF = "LiberationSerif-Bold.ttf"
    BOLD = "LiberationSans-Bold.ttf"
    REG = "LiberationSans-Regular.ttf"
    NARROW = "LiberationSansNarrow-Bold.ttf"

    @staticmethod
    def face(name, size):
        return ImageFont.truetype(LIBERATION + name, size)


def wrap_text(draw, words, font, max_w):
    """Greedy word wrap; returns the lines that fit inside max_w."""
    lines, cur = [], ""
    for word in words.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def paragraph(draw, x, y, text, font, fill, max_w, leading):
    """Draw a wrapped paragraph; returns the y below its last line."""
    for line in wrap_text(draw, text, font, max_w):
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


class FrontPage:
    """The poster, drawn section by section onto one canvas."""

    def __init__(self):
        self.sheet = Image.new("RGB", (SIDE, SIDE), PAGE_BG)
        self.pen = ImageDraw.Draw(self.sheet)

    # -- masthead ----------------------------------------------------------
    def masthead(self):
        p = self.pen
        p.rectangle([0, 0, SIDE, 90], fill=NEWS)
        p.text((30, 12), "THE WORLD ON EDGE",
               font=Type.face(Type.SERIF, 50), fill=PAGE_BG)
        p.text((SIDE - 30, 20), "SATURDAY",
               font=Type.face(Type.BOLD, 21), fill=SCARLET, anchor="ra")
        p.text((SIDE - 30, 48), "21 NOVEMBER 2026",
               font=Type.face(Type.BOLD, 25), fill=PAGE_BG, anchor="ra")
        p.rectangle([0, 90, SIDE, 96], fill=SCARLET)

    # -- hero: the Strait of Hormuz ----------------------------------------
    def hero(self):
        top, bottom = 96, 556
        height = bottom - top
        sea = Image.new("RGB", (SIDE, height), SEA_HIGH)
        hd = ImageDraw.Draw(sea)
        for yy in range(height):
            t = yy / height
            hd.line([(0, yy), (SIDE, yy)], fill=(
                int(SEA_HIGH[0] + (SEA_LOW[0] - SEA_HIGH[0]) * t),
                int(SEA_HIGH[1] + (SEA_LOW[1] - SEA_HIGH[1]) * t),
                int(SEA_HIGH[2] + (SEA_LOW[2] - SEA_HIGH[2]) * t)))
        # Iran along the top edge; Oman's Musandam peninsula bottom-right.
        hd.polygon([(0, 0), (SIDE, 0), (SIDE, 64), (880, 88), (700, 74),
                    (520, 104), (360, 88), (200, 112), (80, 100), (0, 124)],
                   fill=SHORE)
        hd.polygon([(SIDE, height), (SIDE, 218), (968, 240), (912, 292),
                    (872, 352), (824, 392), (700, 424), (560, height)],
                   fill=SHORE)
        hd.text((56, 26), "IRAN", font=Type.face(Type.BOLD, 28), fill=SHORE_TAG)
        hd.text((898, 396), "OMAN", font=Type.face(Type.BOLD, 23), fill=SHORE_TAG)
        hd.text((884, 372), "Khasab", font=Type.face(Type.REG, 15),
                fill=(150, 135, 120))
        hd.text((SIDE // 2, height - 34), "STRAIT OF HORMUZ",
                font=Type.face(Type.BOLD, 15), fill=(90, 120, 160), anchor="ma")
        # Dashed shipping lane across the strait.
        for xx in range(0, SIDE, 34):
            x2 = xx + 17
            y1 = 244 + 18 * math.sin(xx / 130)
            y2 = 244 + 18 * math.sin(x2 / 130)
            hd.line([(xx, y1), (x2, y2)], fill=(70, 100, 140), width=2)
        self._tanker(hd, sea, 300, 296, 1.22, True)
        self._tanker(hd, sea, 688, 232, 0.88, True)
        self._drone(hd, 838, 148)
        self.sheet.paste(sea, (0, top))

    @staticmethod
    def _tanker(hd, sea, cx, cy, s, ablaze):
        """A crude-oil tanker seen side-on; ablaze adds glow, flames, smoke."""
        hull = [(cx - 92 * s, cy), (cx + 102 * s, cy),
                (cx + 82 * s, cy + 26 * s), (cx - 82 * s, cy + 26 * s)]
        hd.polygon(hull, fill=(18, 18, 22))
        hd.rectangle([cx + 42 * s, cy - 30 * s, cx + 80 * s, cy],
                     fill=(28, 28, 34))
        hd.rectangle([cx - 72 * s, cy - 8 * s, cx + 30 * s, cy],
                     fill=(42, 42, 48))
        hd.rectangle([cx - 92 * s, cy - 4 * s, cx + 102 * s, cy + 2 * s],
                     fill=(60, 30, 26))
        if not ablaze:
            return
        glow = Image.new("RGBA", sea.size, (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        gd.ellipse([cx - 150 * s, cy - 140 * s, cx + 130 * s, cy + 50 * s],
                   fill=(255, 110, 20, 110))
        glow = glow.filter(ImageFilter.GaussianBlur(int(38 * s)))
        sea.paste(glow, (0, 0), glow)
        for _ in range(55):
            fx = cx - 25 * s + random.gauss(0, 24 * s)
            fy = cy - abs(random.gauss(0, 48 * s))
            r = random.uniform(5, 15) * s
            col = random.choice([(255, 200, 60), EMBER, SCARLET, (255, 90, 20)])
            hd.ellipse([fx - r, fy - r, fx + r, fy + r], fill=col)
        for i in range(22):
            sx = cx - 30 * s + i * 6 * s + random.gauss(0, 9)
            sy = cy - 84 * s - i * 9 * s
            r = (13 + i * 1.5) * s
            g = 58 + random.randint(0, 26)
            hd.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(g, g, g + 6))

    @staticmethod
    def _drone(hd, dx, dy):
        """A US MQ-9 silhouette, crossed out in red, with a caption."""
        hd.polygon([(dx - 58, dy), (dx + 58, dy - 6), (dx + 58, dy + 6)],
                   fill=(170, 175, 185))
        hd.line([(dx - 8, dy - 38), (dx + 18, dy + 38)],
                fill=(170, 175, 185), width=8)
        hd.line([(dx + 38, dy - 28), (dx + 8, dy + 28)],
                fill=(170, 175, 185), width=5)
        for k in range(4):
            hd.line([(dx + 58 + k * 13, dy - 6 - k * 11),
                     (dx + 68 + k * 13, dy - 12 - k * 11)],
                    fill=(120, 120, 130), width=3)
        hd.line([(dx - 32, dy - 32), (dx + 32, dy + 32)], fill=SCARLET, width=9)
        hd.line([(dx - 32, dy + 32), (dx + 32, dy - 32)], fill=SCARLET, width=9)
        hd.text((dx, dy + 50), "US MQ-9 'downed'",
                font=Type.face(Type.BOLD, 15),
                fill=(220, 220, 230), anchor="ma")

    # -- headline band -------------------------------------------------------
    def band(self):
        p = self.pen
        top, bottom = 452, 556
        p.rectangle([0, top, SIDE, bottom], fill=(0, 0, 0))
        p.rectangle([30, top + 14, 138, top + 42], fill=SCARLET)
        p.text((84, top + 28), "TOP STORY", font=Type.face(Type.BOLD, 16),
               fill=NEWS, anchor="mm")
        p.text((152, top + 10), "TANKERS HIT IN HORMUZ",
               font=Type.face(Type.BOLD, 42), fill=NEWS)
        p.text((30, top + 58),
               "Second tanker struck off Oman on Saturday  •  Iran says it downed a US drone  •  US–Iran talks stall",
               font=Type.face(Type.REG, 16), fill=NEWS_FAINT)
        p.text((30, top + 80),
               "COP31 overtime  •  Russia's huge Ukraine strike spills into Poland  •  G-3 summit afterglow",
               font=Type.face(Type.REG, 16), fill=GREY)

    # -- story tiles ---------------------------------------------------------
    def tiles(self):
        p = self.pen
        top = 568
        cols, rows = 3, 2
        gap = 12
        margin = 24
        tw = (SIDE - 2 * margin - (cols - 1) * gap) // cols
        th = (SIDE - top - 48 - (rows - 1) * gap) // rows
        art_h = th - 72
        cards = [
            ((30, 70, 56), "COP31 goes to overtime",
             ["Antalya talks stall as draft deal",
              "drops all mention of fossil fuels"],
             self._art_cop),
            ((36, 40, 70), "Russia pounds Ukraine",
             ["400+ drones, 110+ missiles; strays",
              "land in Poland; Denmark expels attaché"],
             self._art_ukraine),
            ((70, 30, 34), "After the 'G-3' summit",
             ["Trump, Xi, Putin met in Shenzhen;",
              "deal on humans-in-the-loop military AI"],
             self._art_g3),
            ((40, 40, 44), "US outages, cyber chief out",
             ["Banks, flights, systems down; Trump",
              "fires National Cyber Director"],
             self._art_outage),
            ((60, 48, 28), "Myanmar guilty of genocide",
             ["ICJ landmark ruling on the Rohingya;",
              "9–6, first time a state is found guilty"],
             self._art_icj),
            ((28, 58, 74), "UK and EU seal reset deal",
             ["Youth mobility for 100,000 a year;",
              "food trade eased, carbon markets linked"],
             self._art_ukeu),
        ]
        for i, (bg, title, lines, art) in enumerate(cards):
            c, r = i % cols, i // cols
            x0 = margin + c * (tw + gap)
            y0 = top + r * (th + gap)
            p.rounded_rectangle([x0, y0, x0 + tw, y0 + th], 10, fill=bg)
            art(x0, y0, x0 + tw, y0 + art_h)
            p.text((x0 + 13, y0 + art_h + 6), title,
                   font=Type.face(Type.BOLD, 21), fill=NEWS)
            yy = y0 + art_h + 34
            for ln in lines:
                p.text((x0 + 13, yy), ln, font=Type.face(Type.REG, 13),
                       fill=(220, 215, 205))
                yy += 16

    # -- tile artwork ----------------------------------------------------------
    def _art_cop(self, x0, y0, x1, y1):
        """A warming globe with a clock running past the deadline."""
        p = self.pen
        cx, cy = (x0 + x1) // 2 - 30, (y0 + y1) // 2 + 4
        p.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], fill=(40, 110, 160))
        p.polygon([(cx - 28, cy - 18), (cx - 4, cy - 32), (cx + 10, cy - 8),
                   (cx - 8, cy + 10), (cx - 26, cy + 2)], fill=(70, 150, 80))
        p.polygon([(cx + 12, cy + 8), (cx + 32, cy + 4), (cx + 26, cy + 28),
                   (cx + 12, cy + 26)], fill=(70, 150, 80))
        kx, ky = cx + 74, cy - 18
        p.ellipse([kx - 21, ky - 21, kx + 21, ky + 21], fill=NEWS)
        p.line([(kx, ky), (kx, ky - 14)], fill=PAGE_BG, width=3)
        p.line([(kx, ky), (kx + 11, ky + 4)], fill=SCARLET, width=3)
        ox, oy = cx + 72, cy + 22
        p.polygon([(ox, oy - 24), (ox - 14, oy + 2), (ox + 14, oy + 2)],
                  fill=PAGE_BG)
        p.ellipse([ox - 14, oy - 11, ox + 14, oy + 17], fill=PAGE_BG)
        p.line([(ox - 20, oy - 24), (ox + 20, oy + 20)], fill=SCARLET, width=4)

    def _art_ukraine(self, x0, y0, x1, y1):
        """Ukrainian flag with incoming missile streaks and a Poland marker."""
        p = self.pen
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
        p.rectangle([x0 + 28, cy - 12, x1 - 28, cy + 12], fill=(0, 87, 183))
        p.rectangle([x0 + 28, cy + 12, x1 - 28, cy + 38], fill=(255, 215, 0))
        for mx, my in [(cx - 58, cy - 18), (cx - 4, cy - 26), (cx + 54, cy - 14)]:
            p.line([(mx - 28, my - 28), (mx, my)],
                   fill=(235, 235, 235), width=6)
            p.polygon([(mx, my), (mx - 11, my - 2), (mx - 2, my - 11)],
                      fill=SCARLET)
        p.text((x1 - 30, y0 + 10), "PL", font=Type.face(Type.BOLD, 17),
               fill=SCARLET, anchor="ra")

    def _art_g3(self, x0, y0, x1, y1):
        """Three linked rings: Washington, Beijing, Moscow."""
        p = self.pen
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 + 4
        for dx, col, lab in [(-60, (60, 90, 200), "US"),
                             (0, (220, 40, 40), "CN"),
                             (60, (240, 240, 240), "RU")]:
            p.ellipse([cx + dx - 34, cy - 34, cx + dx + 34, cy + 34],
                      outline=col, width=7)
            p.text((cx + dx, cy), lab, font=Type.face(Type.BOLD, 19),
                   fill=col, anchor="mm")

    def _art_outage(self, x0, y0, x1, y1):
        """A power line that snaps mid-span; the grid goes dark after it."""
        p = self.pen
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
        pts = [(x0 + 22, cy), (cx - 48, cy), (cx - 34, cy - 32),
               (cx - 14, cy + 32), (cx, cy - 8), (cx + 8, cy)]
        p.line(pts, fill=(80, 255, 140), width=4)
        p.line([(cx + 8, cy), (x1 - 22, cy)], fill=(80, 80, 80), width=4)
        p.text((cx + 58, cy - 32), "ERR", font=Type.face(Type.BOLD, 25),
               fill=SCARLET, anchor="mm")
        p.text((cx + 58, cy + 28), "✈ $ ⚠",
               font=ImageFont.truetype(DEJAVU_HEAVY, 21),
               fill=(230, 230, 230), anchor="mm")

    def _art_icj(self, x0, y0, x1, y1):
        """Scales of justice, tipped toward the victims."""
        p = self.pen
        cx, cy = (x0 + x1) // 2, y0 + 20
        p.line([(cx, cy), (cx, y1 - 8)], fill=BRASS, width=5)
        p.line([(cx - 66, cy + 8), (cx + 66, cy + 8)], fill=BRASS, width=5)
        p.rectangle([cx - 28, y1 - 12, cx + 28, y1 - 4], fill=BRASS)
        for sx, drop in [(-66, 20), (66, 2)]:
            px, py = cx + sx, cy + 8
            p.line([(px, py), (px - 20, py + 38 + drop)], fill=BRASS, width=2)
            p.line([(px, py), (px + 20, py + 38 + drop)], fill=BRASS, width=2)
            p.pieslice([px - 26, py + 24 + drop, px + 26, py + 54 + drop],
                       0, 180, fill=BRASS)

    def _art_ukeu(self, x0, y0, x1, y1):
        """EU stars beside a Union Jack, with the youth-mobility figure."""
        p = self.pen
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 6
        p.ellipse([cx - 78, cy - 34, cx - 6, cy + 34], fill=(0, 51, 153))
        for k in range(12):
            a = -math.pi / 2 + k * math.pi / 6
            sx, sy = cx - 42 + 24 * math.cos(a), cy + 24 * math.sin(a)
            p.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 204, 0))
        p.rectangle([cx + 6, cy - 34, cx + 78, cy + 34], fill=(1, 33, 105))
        p.line([(cx + 6, cy - 34), (cx + 78, cy + 34)], fill=NEWS, width=5)
        p.line([(cx + 6, cy + 34), (cx + 78, cy - 34)], fill=NEWS, width=5)
        p.line([(cx + 42, cy - 34), (cx + 42, cy + 34)], fill=NEWS, width=8)
        p.line([(cx + 6, cy), (cx + 78, cy)], fill=NEWS, width=8)
        p.text((cx, y1 - 14), "100,000 a year",
               font=Type.face(Type.BOLD, 16), fill=NEWS, anchor="ma")

    # -- footer ------------------------------------------------------------------
    def footer(self):
        self.pen.text(
            (SIDE // 2, SIDE - 24),
            "Also: Basra pipeline blast kills at least 4  •  US–Iran talks stall as Hormuz attacks continue  •  NATO chief to visit Warsaw",
            font=Type.face(Type.REG, 14), fill=(170, 165, 155), anchor="mm")

    def build(self):
        self.masthead()
        self.hero()
        self.band()
        self.tiles()
        self.footer()
        return self.sheet


if __name__ == "__main__":
    page = FrontPage()
    out = Path(__file__).resolve().parent.parent / "entry.png"
    page.build().save(out, optimize=True)
    print(out, out.stat().st_size)
