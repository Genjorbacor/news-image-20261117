#!/usr/bin/env python3
"""Draw the entry image: a newspaper front page summing up Tuesday 17 November 2026.

Run: python3 draw.py  ->  writes entry.png (1024x1024, deterministic).
Only Pillow and the system DejaVu fonts are used; nothing is fetched.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (25, 25, 25)
MUTED = (90, 86, 76)
RED = (163, 22, 33)
SEA = (29, 78, 107)
SAND = (217, 201, 163)
SAND_DARK = (199, 178, 132)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)      # noqa: E731
SERIF = lambda s: font("DejaVuSerif.ttf", s)            # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)              # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)        # noqa: E731


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w, keeping words whole."""
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
    """A spiky explosion star centred on (cx, cy)."""
    pts = []
    for i in range(points * 2):
        r = r_outer if i % 2 == 0 else r_inner
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def draw_strait(draw, box):
    """A stylised Strait of Hormuz: sand on both shores, blue water, a tanker, a blast."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=SEA)
    # northern shore (top) and southern shore (bottom) as sand polygons
    draw.polygon([(x0, y0), (x1, y0), (x1, y0 + 26), (x0 + 620, y0 + 44),
                  (x0 + 420, y0 + 22), (x0, y0 + 40)], fill=SAND)
    draw.polygon([(x0, y1), (x1, y1), (x1, y1 - 24), (x0 + 560, y1 - 48),
                  (x0 + 380, y1 - 22), (x0, y1 - 44)], fill=SAND_DARK)
    # shipping lane dashes
    mid = (y0 + y1) // 2 + 10
    for x in range(x0 + 40, x1 - 40, 64):
        draw.line([(x, mid), (x + 34, mid)], fill=(255, 255, 255), width=3)
    # tanker silhouette, centre-left
    tx, ty = x0 + 250, (y0 + y1) // 2 - 4
    draw.rectangle([tx, ty, tx + 210, ty + 24], fill=(30, 30, 34))
    draw.rectangle([tx + 30, ty - 15, tx + 60, ty], fill=(30, 30, 34))
    draw.rectangle([tx + 150, ty - 9, tx + 172, ty], fill=(30, 30, 34))
    draw.rectangle([tx, ty + 24, tx + 210, ty + 28], fill=RED)
    # blast above the tanker, centre-right: spiky starburst + smoke
    bx, by = tx + 300, ty - 26
    starburst(draw, bx, by, 58, 30, 12, (255, 122, 26))
    starburst(draw, bx, by, 40, 20, 10, (255, 176, 32))
    starburst(draw, bx, by, 22, 11, 8, (255, 224, 130))
    for cx, cy, r in [(bx - 62, by - 44, 14), (bx - 34, by - 58, 11),
                      (bx + 56, by - 50, 13), (bx + 80, by - 28, 10)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(96, 96, 100))
    # small labels on the scene
    lab = SANS_B(16)
    draw.text((x0 + 22, y0 + 10), "IRAN", font=lab, fill=(90, 60, 20))
    draw.text((x0 + 22, y1 - 30), "OMAN", font=lab, fill=(255, 255, 255))
    draw.text((x1 - 196, mid + 26), "STRAIT OF HORMUZ", font=lab,
              fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 48                      # side margin
    cw = W - 2 * mx              # content width

    # double border
    d.rectangle([20, 20, W - 21, H - 21], outline=INK, width=2)
    d.rectangle([28, 28, W - 29, H - 29], outline=INK, width=1)

    # ---- masthead ----
    y = 44
    kick = "THE WORLD IN ONE IMAGE"
    f_kick = SERIF_B(50)
    d.text(((W - d.textlength(kick, font=f_kick)) / 2, y), kick, font=f_kick, fill=INK)
    y += 66
    date = "TUESDAY  ·  17 NOVEMBER 2026"
    f_date = SANS_B(24)
    d.text(((W - d.textlength(date, font=f_date)) / 2, y), date, font=f_date, fill=RED)
    y += 38
    d.line([(mx, y), (W - mx, y)], fill=INK, width=3)
    d.line([(mx, y + 6), (W - mx, y + 6)], fill=INK, width=1)
    y += 18

    # ---- lead headline + deck ----
    lead = "U.S. STRIKES IRAN AS TANKERS BURN IN THE STRAIT OF HORMUZ"
    f_lead = SERIF_B(40)
    lines = wrap(d, lead, f_lead, cw)
    y = text_block(d, mx, y, lines, f_lead, INK, 50)
    y += 6
    deck = ("Warplanes hit missile sites on Qeshm Island after attacks on U.S. forces. "
            "Oman evacuates 24 seafarers from a burning gas tanker as Trump says an "
            "alleged \u201cdirty bomb\u201d plot is being taken seriously.")
    f_deck = SERIF(22)
    y = text_block(d, mx, y, wrap(d, deck, f_deck, cw), f_deck, MUTED, 28)
    y += 12

    # ---- picture panel ----
    panel = (mx, y, W - mx, y + 160)
    draw_strait(d, panel)
    d.rectangle(panel, outline=INK, width=2)
    y = panel[3] + 8
    cap = "THE STRAIT OF HORMUZ, TUESDAY \u2014 A BURNING TANKER AFTER THE LATEST ATTACK"
    f_cap = SANS(16)
    d.text((mx, y), cap, font=f_cap, fill=MUTED)
    y += 26
    d.line([(mx, y), (W - mx, y)], fill=INK, width=2)
    y += 14

    # ---- six stories, two columns x three rows ----
    stories = [
        ("UKRAINE", "Kerch Bridge hit again as a span falls into the sea",
         "Kyiv\u2019s drones strike for a second day; Moscow answers with attacks on Kyiv\u2019s bridges."),
        ("ASIA", "Trump lands in Manila on his way to a three-way summit",
         "Quad talks open the trip; a first-ever meeting with Xi and Putin is set for Thursday in China."),
        ("HEALTH", "America loses its measles-free status",
         "The first loss since 2000, after a year of uninterrupted spread, officials confirm."),
        ("TECHNOLOGY", "Outages ripple across airports, banks and Big Tech",
         "Microsoft and Apple services falter and an NSA system goes dark; officials deny a cyberattack."),
        ("MARKETS", "Nvidia spy scandal shadows record earnings",
         "Its ex-chief is caught in an alleged Chinese agent case as Wall Street slides on tech."),
        ("GAZA", "Winter rains deepen Gaza\u2019s shelter crisis",
         "The UN warns flooding is destroying food and shelter as the West urges Israel to open crossings."),
    ]
    col_w = (cw - 32) // 2
    row_h = 122
    for i, (kicker, head, body) in enumerate(stories):
        col, row = i % 2, i // 2
        x = mx + col * (col_w + 32)
        yy = y + row * row_h
        d.text((x, yy), kicker, font=SANS_B(18), fill=RED)
        yy += 24
        yy = text_block(d, x, yy, wrap(d, head, SERIF_B(24), col_w),
                        SERIF_B(24), INK, 27)
        yy = text_block(d, x, yy + 2, wrap(d, body, SANS(17), col_w),
                        SANS(17), MUTED, 20)
    y += 3 * row_h + 8

    # ---- footer ----
    d.line([(mx, y), (W - mx, y)], fill=INK, width=1)
    foot = "SUMMED UP FROM TUESDAY\u2019S REPORTING  ·  17 NOVEMBER 2026"
    f_foot = SANS_B(17)
    d.text(((W - d.textlength(foot, font=f_foot)) / 2, y + 10), foot,
           font=f_foot, fill=MUTED)

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
