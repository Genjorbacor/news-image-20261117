#!/usr/bin/env python3
"""Draw the entry image, version 4: a dense one-page front page summing up
Tuesday 17 November 2026, built on the pay-line entries' formula:

- giant date masthead + a six-number strip
- 3 illustrated lead stories (Kerch Bridge diagram, Hormuz map, Quad flags)
- 10 pictured stories in a 5-column grid, each with its own visual
- an ALSO list of 30 numbered one-liners (stories 14-43) in 3 columns
- a WHERE IT HAPPENED world map with numbered pins
- a date-honesty footer and a sources line

43 stories in total. Run: python3 draw.py -> writes entry.png (1024x1024,
deterministic). Only Pillow and the system DejaVu fonts are used.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 233)
INK = (22, 22, 22)
MUTED = (96, 92, 82)
RED = (168, 24, 34)
BLUE = (30, 80, 140)
SKY = (178, 205, 226)
SEA = (140, 180, 210)
LAND = (232, 214, 170)
PANEL = (238, 233, 220)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)      # noqa: E731
SERIF = lambda s: font("DejaVuSerif.ttf", s)            # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)              # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)        # noqa: E731


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def starburst(draw, cx, cy, r_outer, r_inner, points, fill):
    pts = []
    for i in range(points * 2):
        r = r_outer if i % 2 == 0 else r_inner
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def caption_bar(draw, box, text):
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y1 - 18, x1, y1], fill=(18, 18, 20))
    draw.text((x0 + 6, y1 - 15), text, font=SANS_B(10), fill=(255, 255, 255))


# ---------------------------------------------------------------- lead panels

def lead_kerch(draw, box):
    """Kerch Strait bridge diagram: deck, a dropped span, smoke, jets."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=SKY)
    sea_y = y0 + 48
    draw.rectangle([x0, sea_y, x1, y1], fill=SEA)
    for yy in range(sea_y + 8, y1 - 6, 12):
        for xx in range(x0 + 12, x1 - 40, 90):
            draw.line([(xx, yy), (xx + 26, yy)], fill=(210, 228, 240), width=2)
    deck_y = y0 + 32
    draw.rectangle([x0, deck_y, x0 + 118, deck_y + 7], fill=(60, 60, 66))
    draw.rectangle([x0 + 178, deck_y, x1, deck_y + 7], fill=(60, 60, 66))
    for px in (x0 + 26, x0 + 78, x0 + 208, x0 + 252):
        draw.rectangle([px, deck_y + 7, px + 5, sea_y], fill=(60, 60, 66))
    draw.polygon([(x0 + 122, deck_y + 4), (x0 + 172, deck_y + 2),
                  (x0 + 166, deck_y + 26), (x0 + 128, deck_y + 24)],
                 fill=(90, 90, 96))
    for cx, cy, r in [(x0 + 148, deck_y - 8, 11), (x0 + 162, deck_y - 20, 14),
                      (x0 + 138, deck_y - 22, 9)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 70, 76))
    starburst(draw, x0 + 150, deck_y + 2, 13, 7, 8, (255, 140, 40))
    for jx, jy in [(x0 + 34, y0 + 12), (x0 + 210, y0 + 8)]:
        draw.polygon([(jx, jy), (jx + 16, jy + 4), (jx, jy + 8)], fill=(40, 40, 46))
    draw.text((x0 + 6, y0 + 4), "CRIMEA", font=SANS_B(9), fill=(70, 70, 76))
    draw.text((x1 - 44, y0 + 4), "RUSSIA", font=SANS_B(9), fill=(70, 70, 76))
    caption_bar(draw, box, "KERCH STRAIT \u00b7 STRUCK FOR A SECOND DAY")


def lead_hormuz(draw, box):
    """Simplified Gulf map: Iran top, Bahrain left, Qeshm, tanker, drones."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=SEA)
    draw.polygon([(x0, y0), (x1, y0), (x1, y0 + 26), (x0 + 190, y0 + 44),
                  (x0 + 120, y0 + 30), (x0, y0 + 34)], fill=LAND)
    draw.polygon([(x0, y1), (x1, y1), (x1, y1 - 22), (x0 + 220, y1 - 40),
                  (x0 + 90, y1 - 26), (x0, y1 - 30)], fill=LAND)
    draw.ellipse([x0 + 196, y0 + 46, x0 + 252, y0 + 60], fill=LAND)
    draw.ellipse([x0 + 62, y0 + 52, x0 + 84, y0 + 64], fill=LAND)
    for (ax, ay, bx, by) in [(x0 + 210, y0 + 40, x0 + 76, y0 + 58),
                             (x0 + 230, y0 + 44, x0 + 150, y0 + 66)]:
        steps = 8
        for i in range(steps):
            if i % 2:
                continue
            t0, t1 = i / steps, (i + 1) / steps
            draw.line([(ax + (bx - ax) * t0, ay + (by - ay) * t0),
                       (ax + (bx - ax) * t1, ay + (by - ay) * t1)],
                      fill=RED, width=2)
    draw.text((x0 + 120, y0 + 6), "IRAN", font=SANS_B(10), fill=(90, 80, 60))
    draw.text((x0 + 8, y0 + 52), "BAHRAIN", font=SANS_B(9), fill=(90, 80, 60))
    draw.text((x0 + 200, y0 + 62), "QESHM", font=SANS_B(9), fill=(90, 80, 60))
    for cx, cy in [(x0 + 130, y0 + 52), (x0 + 170, y0 + 60)]:
        draw.line([(cx - 6, cy - 6), (cx + 6, cy + 6)], fill=RED, width=3)
        draw.line([(cx - 6, cy + 6), (cx + 6, cy - 6)], fill=RED, width=3)
    tx, ty = x0 + 196, y1 - 40
    draw.rectangle([tx, ty, tx + 62, ty + 10], fill=(24, 24, 28))
    draw.rectangle([tx + 10, ty - 7, tx + 24, ty], fill=(24, 24, 28))
    starburst(draw, tx + 46, ty - 8, 12, 6, 8, (255, 140, 40))
    caption_bar(draw, box, "STRAIT OF HORMUZ \u00b7 US JETS HIT QESHM")


def flag_us(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(178, 34, 52))
    for i in range(4):
        draw.rectangle([x, y + (2 * i + 1) * h // 8, x + w, y + (2 * i + 2) * h // 8],
                       fill=(255, 255, 255))
    draw.rectangle([x, y, x + w * 0.42, y + h * 0.55], fill=(30, 50, 110))


def flag_in(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h // 3], fill=(255, 153, 51))
    draw.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=(255, 255, 255))
    draw.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(19, 136, 8))
    draw.ellipse([x + w // 2 - 4, y + h // 2 - 4, x + w // 2 + 4, y + h // 2 + 4],
                 outline=(0, 70, 140), width=1)


def flag_jp(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    draw.ellipse([x + w // 2 - 6, y + h // 2 - 6, x + w // 2 + 6, y + h // 2 + 6],
                 fill=(188, 0, 45))


def flag_au(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(0, 40, 104))
    for sx, sy in [(x + 8, y + 6), (x + 24, y + 12), (x + 14, y + 18),
                   (x + 30, y + 6), (x + 20, y + 24)]:
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))


def lead_quad(draw, box):
    """Quad summit: four flags behind a table, Manila."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(238, 232, 214))
    flags = [flag_us, flag_in, flag_jp, flag_au]
    names = ["US", "INDIA", "JAPAN", "AUSTRALIA"]
    fw, fh = 44, 28
    step = (x1 - x0 - 24) // 4
    for i, fn in enumerate(flags):
        fx = x0 + 14 + i * step
        draw.rectangle([fx + fw // 2 - 1, y0 + 12, fx + fw // 2 + 1, y0 + 12 + fh + 8],
                       fill=(120, 110, 90))
        fn(draw, fx, y0 + 12, fw, fh)
        draw.text((fx, y0 + 12 + fh + 10), names[i], font=SANS_B(8),
                  fill=(70, 70, 76))
    ty = y0 + 62
    draw.rectangle([x0 + 8, ty, x1 - 8, ty + 10], fill=(122, 84, 48))
    caption_bar(draw, box, "QUAD LEADERS' SUMMIT \u00b7 MANILA")


# ---------------------------------------------------------------- mini icons

def icon_virus(draw, x, y, w, h, colour=RED):
    cx, cy = x + w // 2, y + h // 2
    for a in range(8):
        ang = math.pi * a / 4
        draw.line([(cx + 10 * math.cos(ang), cy + 10 * math.sin(ang)),
                   (cx + 16 * math.cos(ang), cy + 16 * math.sin(ang))],
                  fill=colour, width=2)
    draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=colour)
    draw.ellipse([cx - 4, cy - 4, cx + 1, cy + 1], fill=(255, 255, 255))


def icon_globe(draw, x, y, w, h):
    cx, cy = x + w // 2, y + h // 2
    draw.ellipse([cx - 16, cy - 14, cx + 16, cy + 14], fill=(60, 130, 200))
    draw.ellipse([cx - 10, cy - 8, cx - 2, cy + 2], fill=(80, 180, 90))
    draw.ellipse([cx + 2, cy + 2, cx + 12, cy + 10], fill=(80, 180, 90))
    draw.ellipse([cx - 16, cy - 14, cx + 16, cy + 14], outline=INK, width=1)


def icon_chip(draw, x, y, w, h):
    cx, cy = x + w // 2, y + h // 2
    draw.rectangle([cx - 12, cy - 10, cx + 12, cy + 10], fill=(20, 90, 60))
    draw.rectangle([cx - 5, cy - 4, cx + 5, cy + 4], fill=(120, 220, 160))
    for dx in (-8, 0, 8):
        draw.line([(cx + dx, cy - 14), (cx + dx, cy - 10)], fill=INK, width=2)
        draw.line([(cx + dx, cy + 10), (cx + dx, cy + 14)], fill=INK, width=2)


def icon_tents(draw, x, y, w, h):
    for tx in (x + 6, x + 26):
        draw.polygon([(tx, y + 26), (tx + 10, y + 8), (tx + 20, y + 26)],
                     fill=(210, 200, 170), outline=INK)
    draw.rectangle([x + 8, y + 30, x + 44, y + 36], fill=(180, 60, 50))


def icon_doc(draw, x, y, w, h):
    draw.rectangle([x + 14, y + 4, x + 40, y + 34], fill=(255, 255, 255),
                   outline=INK)
    for yy in (y + 10, y + 16, y + 22):
        draw.line([(x + 18, yy), (x + 36, yy)], fill=MUTED, width=2)
    draw.ellipse([x + 30, y + 24, x + 42, y + 36], fill=RED)


def icon_parliament(draw, x, y, w, h):
    cx, cy = x + w // 2, y + h - 6
    for a in range(9):
        ang = math.pi * (1 - a / 8)
        px, py = cx + 18 * math.cos(ang), cy - 18 * math.sin(ang)
        draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=BLUE)
    draw.line([(x + 6, cy), (x + w - 6, cy)], fill=INK, width=2)


def icon_factory(draw, x, y, w, h):
    draw.rectangle([x + 8, y + 16, x + 44, y + 34], fill=(120, 120, 126))
    draw.rectangle([x + 34, y + 6, x + 40, y + 16], fill=(120, 120, 126))
    for cx, cy, r in [(x + 44, y + 8, 5), (x + 48, y + 14, 4)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 150, 156))


def icon_plane(draw, x, y, w, h):
    cx, cy = x + w // 2, y + h // 2
    draw.polygon([(cx - 20, cy), (cx + 18, cy - 5), (cx + 22, cy),
                  (cx + 18, cy + 5)], fill=(60, 60, 66))
    draw.polygon([(cx - 4, cy - 4), (cx + 2, cy - 14), (cx + 6, cy - 4)],
                 fill=(60, 60, 66))
    draw.polygon([(cx - 4, cy + 4), (cx + 2, cy + 12), (cx + 6, cy + 4)],
                 fill=(60, 60, 66))


def icon_radiation(draw, x, y, w, h):
    cx, cy = x + w // 2, y + h // 2
    draw.ellipse([cx - 15, cy - 13, cx + 15, cy + 13], fill=(24, 24, 24))
    for a in (90, 210, 330):
        draw.pieslice([cx - 12, cy - 11, cx + 12, cy + 11],
                      start=a - 28, end=a + 28, fill=(255, 210, 0))
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 210, 0))


# ---------------------------------------------------------------- world map

def draw_map(draw, box):
    """Stylised world map: tan continents on pale sea, numbered pins.
    Continents are defined in a 640x192 space and scaled into the box."""
    x0, y0, x1, y1 = box
    sx = (x1 - x0) / 640.0
    sy = (y1 - y0) / 192.0

    def P(px, py):
        return (x0 + px * sx, y0 + py * sy)

    def poly(pts):
        draw.polygon([P(px, py) for px, py in pts], fill=LAND,
                     outline=(180, 160, 120))

    draw.rectangle(box, fill=(196, 218, 232))
    poly([(22, 30), (96, 12), (132, 30), (118, 62), (78, 74), (44, 66), (26, 48)])
    poly([(108, 92), (148, 88), (158, 122), (138, 158), (118, 132)])
    poly([(300, 26), (336, 16), (352, 34), (336, 52), (306, 48)])
    poly([(300, 66), (348, 60), (362, 92), (344, 128), (318, 118), (302, 92)])
    poly([(360, 18), (470, 8), (540, 26), (528, 62), (470, 78), (420, 66), (372, 48)])
    poly([(500, 138), (556, 132), (566, 152), (530, 162), (502, 154)])
    pins = [(1, 330, 34), (2, 392, 46), (3, 318, 40), (4, 322, 96),
            (5, 452, 44), (6, 250, 84), (7, 138, 122), (8, 540, 148),
            (9, 96, 40), (10, 480, 30), (11, 356, 78), (12, 420, 56),
            (13, 500, 120)]
    for num, px, py in pins:
        cx, cy = P(px, py)
        draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED,
                     outline=(255, 255, 255), width=1)
        draw.text((cx - 3, cy - 5), str(num), font=SANS_B(8),
                  fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36
    cw = W - 2 * mx

    d.rectangle([16, 16, W - 17, H - 17], outline=INK, width=2)
    d.rectangle([24, 24, W - 25, H - 25], outline=INK, width=1)

    # ---- top line ----
    y = 32
    d.text((mx, y), "THE WORLD'S NEWS IN ONE PICTURE", font=SANS_B(13), fill=RED)
    right = "43 STORIES \u00b7 6 CONTINENTS \u00b7 ALL FROM TUESDAY"
    d.text((W - mx - d.textlength(right, font=SANS_B(12)), y + 1), right,
           font=SANS_B(12), fill=MUTED)

    # ---- giant date masthead (shrink until it fits the content width) ----
    mast = "Tuesday 17 November 2026"
    f_mast = SERIF_B(64)
    while d.textlength(mast, font=f_mast) > cw and f_mast.size > 40:
        f_mast = SERIF_B(f_mast.size - 2)
    mast_y = 46
    d.text(((W - d.textlength(mast, font=f_mast)) / 2, mast_y), mast,
           font=f_mast, fill=INK)
    rule_y = mast_y + f_mast.size + 14
    d.line([(mx, rule_y), (W - mx, rule_y)], fill=INK, width=2)

    # ---- number strip ----
    numbers = [
        ("1,441", "drones Russia says downed"),
        ("$115.8bn", "Nvidia quarterly sales"),
        ("-849", "Dow points"),
        ("1.4m", "in Gaza face hunger"),
        ("140/250", "Serbia student MPs"),
        ("19", "Siberia air crash"),
    ]
    cell_w = cw / 6
    y = rule_y + 8
    for i, (num, label) in enumerate(numbers):
        cx = mx + i * cell_w
        d.text((cx + 6, y), num, font=SANS_B(21), fill=RED if i % 2 == 0 else INK)
        d.text((cx + 6, y + 26), label, font=SANS(11), fill=MUTED)
        if i:
            d.line([(cx, y + 2), (cx, y + 40)], fill=(200, 194, 182), width=1)
    y += 46
    d.line([(mx, y), (W - mx, y)], fill=INK, width=1)
    y += 8

    # ---- 3 illustrated leads ----
    leads = [
        (lead_kerch, "1", "EUROPE \u00b7 UKRAINE WAR",
         "Ukraine says a Crimean Bridge span fell into the sea",
         "Second strike in two days. The Kremlin vows to rebuild."),
        (lead_hormuz, "2", "MIDDLE EAST \u00b7 IRAN WAR",
         "Iran drones target US radar; US strikes Iran",
         "US says the drones were downed; US jets then hit Qeshm. Iran claims two tankers hit mines."),
        (lead_quad, "3", "ASIA \u00b7 DIPLOMACY",
         "Trump holds his first Quad summit, in Manila",
         "Critical-minerals deals unveiled; Putin heads to Shenzhen for Thursday's talks."),
    ]
    col_w = (cw - 40) // 3
    for i, (fn, num, tag, head, deck) in enumerate(leads):
        x = mx + i * (col_w + 20)
        fn(d, (x, y, x + col_w, y + 80))
        d.rectangle([x, y, x + col_w, y + 80], outline=INK, width=1)
        yy = y + 88
        d.ellipse([x, yy + 1, x + 15, yy + 16], fill=RED)
        d.text((x + 5, yy + 3), num, font=SANS_B(10), fill=(255, 255, 255))
        d.text((x + 21, yy + 3), tag, font=SANS_B(11), fill=RED)
        yy += 20
        yy = text_block(d, x, yy, wrap(d, head, SERIF_B(19), col_w),
                        SERIF_B(19), INK, 22)
        yy = text_block(d, x, yy + 2, wrap(d, deck, SANS(12), col_w),
                        SANS(12), MUTED, 15)
    y += 192

    # ---- 10 pictured stories, 5 columns x 2 rows ----
    stories = [
        (4, icon_virus, "AFRICA \u00b7 HEALTH", "Ebola in DR Congo passes 11,000 cases",
         "WHO: cases doubled in 3 months."),
        (5, icon_globe, "GLOBAL \u00b7 CLIMATE", "COP31 divided over a fossil-fuel phase-out",
         "Draft weighed; talks end Friday."),
        (6, icon_virus, "AMERICAS \u00b7 HEALTH", "US, Mexico, Bolivia lose measles-free status",
         "PAHO cites a year of spread."),
        (7, icon_chip, "US \u00b7 BUSINESS", "Nvidia's quarterly sales double to $115.8bn",
         "Dow fell 849 points earlier."),
        (8, icon_tents, "MIDDLE EAST \u00b7 GAZA", "Gaza truce at risk of collapse, UN is told",
         "1.4m face acute hunger."),
        (9, icon_doc, "ASIA \u00b7 POLITICS", "Mongolia's president says he will resign",
         "He denies a $25m bribe claim."),
        (10, icon_parliament, "EUROPE \u00b7 POLITICS", "Serbia's student-led majority takes its seats",
         "Student List holds 140 of 250."),
        (11, icon_factory, "ASIA \u00b7 LABOUR", "Bangladesh police tear-gas garment workers",
         "They want Tk 30,000 a month."),
        (12, icon_plane, "RUSSIA \u00b7 AIR CRASH", "Russian An-12 crash in Siberia kills all 19",
         "Plane came down near Kemerovo."),
        (13, icon_radiation, "WORLD \u00b7 SECURITY", "Iran 'dirty-bomb plot' report rattles",
         "US intel, reported by CNN."),
    ]
    gcol_w = (cw - 4 * 16) // 5
    grow_h = 110
    for i, (num, icon, tag, head, deck) in enumerate(stories):
        col, row = i % 5, i // 5
        x = mx + col * (gcol_w + 16)
        yy = y + row * grow_h
        # visual panel with centred icon
        d.rectangle([x, yy, x + gcol_w, yy + 44], fill=PANEL, outline=INK, width=1)
        icon(d, x + (gcol_w - 56) // 2, yy + 2, 56, 40)
        ty = yy + 50
        d.ellipse([x, ty + 1, x + 13, ty + 14], fill=RED)
        d.text((x + 4, ty + 3), str(num), font=SANS_B(9), fill=(255, 255, 255))
        d.text((x + 17, ty + 3), tag, font=SANS_B(9), fill=RED)
        ty += 16
        ty = text_block(d, x, ty, wrap(d, head, SERIF_B(13), gcol_w),
                        SERIF_B(13), INK, 15)
        d.text((x, ty), deck, font=SANS(10), fill=MUTED)
    y += 2 * grow_h + 6

    # ---- ALSO list, stories 14-43, 3 columns x 10 rows ----
    d.line([(mx, y), (W - mx, y)], fill=INK, width=1)
    y += 8
    d.text((mx, y), "ALSO ON TUESDAY 17 NOVEMBER", font=SANS_B(13), fill=RED)
    y += 20
    also = [
        "Mozambique: Mondlane trial opens; 5 charges",
        "UN: Ukraine's civilian deaths top all of 2025",
        "Prague: two trains collide; 46 people injured",
        "France: public-sector strike, 146,000 march",
        "Poland: Tusk survives a no-confidence vote",
        "Germany: Deutsche Bank shares fall in data leak",
        "Moldova: shuts airspace as drone nears capital",
        "Turkey: police seize opposition channel Sozcu TV",
        "India: Cyclone Akvan strengthens; Odisha evacuates",
        "Japan: protests a Russian airspace intrusion",
        "China-Canada: more tariff cuts after Xi talks",
        "Thailand: pledges to scrap tariffs on US goods",
        "S. Korea: IMF lifts 2026 growth forecast to 3.9%",
        "Indonesia: M6.6 quake off Banda Sea; no tsunami",
        "Cook Islands: Cyclone Xavier reaches Category 3",
        "Apple: Pay, iCloud, App Store outage; not a hack",
        "Space: Voyager 1 nears one light-day from Earth",
        "Sudan: UN verifies 2,230 civilian deaths, Jan-Oct",
        "UK: sanctions 8 settlement firms and Tzav 9",
        "Israel: Kahana elected Knesset speaker, 66-52",
        "West Bank: settlers kill a woman, 72, near Jericho",
        "Oman: Iran's Araghchi holds shipping-safety talks",
        "Kuwait: air defences repel drones",
        "Vatican: Pope Leo XIV back from S. America tour",
        "Football: Norway beat Denmark 3-2; Haaland scores",
        "India: bus falls into Uttarakhand gorge, 8 dead",
        "Malaysia: Macron visit seals strategic pact",
        "Kenya: WFP aids 30,000 who fled Ethiopia clashes",
        "Haiti: Aristide's party will field no candidates",
        "Australia: eases planned backpacker visa curbs",
    ]
    acol_w = (cw - 2 * 24) // 3
    for i, line in enumerate(also):
        col, row = i % 3, i // 3
        x = mx + col * (acol_w + 24)
        yy = y + row * 14
        d.text((x, yy), str(14 + i), font=SANS_B(11), fill=RED)
        d.text((x + 24, yy), line, font=SANS(11), fill=INK)
    y += 10 * 14 + 8

    # ---- WHERE IT HAPPENED map ----
    d.line([(mx, y), (W - mx, y)], fill=INK, width=1)
    y += 8
    d.text((mx, y), "WHERE IT HAPPENED", font=SANS_B(13), fill=RED)
    y += 20
    map_h = 140
    draw_map(d, (mx, y, mx + 640, y + map_h))
    d.rectangle([mx, y, mx + 640, y + map_h], outline=INK, width=1)
    lx = mx + 656
    legend = [("Americas", RED), ("Europe", BLUE), ("Middle East", (200, 130, 40)),
              ("Asia", (120, 60, 160)), ("Africa", (40, 140, 60)),
              ("Oceania", (0, 150, 160)), ("Global & space", (90, 90, 96))]
    ly = y + 2
    for name, colour in legend:
        d.ellipse([lx, ly + 2, lx + 10, ly + 12], fill=colour)
        d.text((lx + 16, ly), name, font=SANS(12), fill=INK)
        ly += 19
    d.text((lx, ly + 2), "Pins: stories 1\u201313", font=SANS(11), fill=MUTED)
    y += map_h + 10

    # ---- footer ----
    d.line([(mx, y), (W - mx, y)], fill=INK, width=1)
    foot = ("Every story here happened or was first reported on Tuesday 17 November 2026. "
            "Contested claims are marked as claims.  Sources: Reuters, AP, AFP, BBC, Al Jazeera, WHO, UN.")
    y = text_block(d, mx, y + 6, wrap(d, foot, SANS(10), cw), SANS(10), MUTED, 13)

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
