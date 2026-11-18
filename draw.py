#!/usr/bin/env python3
"""Draw the entry image, version 2: a newspaper front page summing up Tuesday 17 November 2026.

Run: python3 draw.py  ->  writes entry.png (1024x1024, deterministic).
Only Pillow and the system DejaVu fonts are used; nothing is fetched.
Compared with v1: a much larger, dusk-lit hero scene of the Strait of Hormuz,
bigger type, four stories in a 2x2 grid, and one line covering the rest.
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


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def draw_hero(draw, box):
    """Dusk over the Strait of Hormuz: a burning tanker and a second tanker escaping."""
    x0, y0, x1, y1 = box
    horizon = y0 + 118
    # sky: dusk gradient, deep blue at top to ember orange at the horizon
    top, bottom = (24, 42, 74), (224, 110, 44)
    for yy in range(y0, horizon):
        t = (yy - y0) / max(1, horizon - y0)
        draw.line([(x0, yy), (x1, yy)], fill=lerp(top, bottom, t))
    # low sun
    sx, sy = x0 + 700, horizon - 26
    draw.ellipse([sx - 34, sy - 34, sx + 34, sy + 34], fill=(255, 214, 140))
    draw.ellipse([sx - 46, sy - 46, sx + 46, sy + 46], outline=(255, 190, 110), width=2)
    # sea: dark blue with lighter wave strokes
    draw.rectangle([x0, horizon, x1, y1], fill=(16, 52, 84))
    for yy in range(horizon + 14, y1 - 8, 18):
        for xx in range(x0 + 30, x1 - 60, 130):
            draw.line([(xx, yy), (xx + 44, yy)], fill=(64, 120, 158), width=2)
    # distant headlands, left and right
    draw.polygon([(x0, horizon), (x0 + 150, horizon), (x0 + 210, horizon - 34),
                  (x0 + 60, horizon - 52), (x0, horizon - 30)], fill=(38, 44, 54))
    draw.polygon([(x1, horizon), (x1 - 130, horizon), (x1 - 190, horizon - 28),
                  (x1 - 70, horizon - 46), (x1, horizon - 26)], fill=(38, 44, 54))
    # burning tanker, centre-left
    tx, ty = x0 + 130, horizon + 66
    draw.rectangle([tx, ty, tx + 300, ty + 34], fill=(18, 18, 22))
    draw.rectangle([tx + 44, ty - 22, tx + 84, ty], fill=(18, 18, 22))
    draw.rectangle([tx + 210, ty - 14, tx + 238, ty], fill=(18, 18, 22))
    draw.rectangle([tx, ty + 34, tx + 300, ty + 40], fill=RED)
    # big fire and smoke over the tanker
    bx, by = tx + 210, ty - 30
    starburst(draw, bx, by, 78, 40, 12, (255, 122, 26))
    starburst(draw, bx, by, 54, 28, 10, (255, 176, 32))
    starburst(draw, bx, by, 30, 15, 8, (255, 224, 130))
    # second tanker sailing away, right
    ux, uy = x0 + 640, horizon + 60
    draw.rectangle([ux, uy, ux + 190, uy + 24], fill=(24, 28, 36))
    draw.rectangle([ux + 26, uy - 16, ux + 56, uy], fill=(24, 28, 36))
    draw.rectangle([ux + 120, uy - 10, ux + 142, uy], fill=(24, 28, 36))
    # caption strip at the bottom of the panel
    strip_h = 44
    draw.rectangle([x0, y1 - strip_h, x1, y1], fill=(16, 16, 18))
    cap = "THE STRAIT OF HORMUZ  \u2014  TANKERS ABLAZE AFTER U.S. STRIKES ON IRAN"
    draw.text((x0 + 20, y1 - strip_h + 11), cap, font=SANS_B(21), fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 48                      # side margin
    cw = W - 2 * mx              # content width

    # double border
    d.rectangle([20, 20, W - 21, H - 21], outline=INK, width=2)
    d.rectangle([28, 28, W - 29, H - 29], outline=INK, width=1)

    # ---- masthead ----
    y = 42
    kick = "THE WORLD IN ONE IMAGE"
    f_kick = SERIF_B(52)
    d.text(((W - d.textlength(kick, font=f_kick)) / 2, y), kick, font=f_kick, fill=INK)
    y += 68
    date = "TUESDAY  ·  17 NOVEMBER 2026"
    f_date = SANS_B(25)
    d.text(((W - d.textlength(date, font=f_date)) / 2, y), date, font=f_date, fill=RED)
    y += 38
    d.line([(mx, y), (W - mx, y)], fill=INK, width=3)
    d.line([(mx, y + 6), (W - mx, y + 6)], fill=INK, width=1)
    y += 18

    # ---- lead headline + deck ----
    lead = "U.S. STRIKES IRAN AS TANKERS BURN IN THE STRAIT OF HORMUZ"
    f_lead = SERIF_B(42)
    y = text_block(d, mx, y, wrap(d, lead, f_lead, cw), f_lead, INK, 52)
    y += 6
    deck = ("Warplanes hit missile sites on Qeshm Island after attacks on U.S. forces, "
            "and Oman evacuates 24 seafarers from a burning gas tanker.")
    f_deck = SERIF(24)
    y = text_block(d, mx, y, wrap(d, deck, f_deck, cw), f_deck, MUTED, 31)
    y += 12

    # ---- hero panel ----
    panel = (mx, y, W - mx, y + 250)
    draw_hero(d, panel)
    d.rectangle(panel, outline=INK, width=2)
    y = panel[3] + 14
    d.line([(mx, y), (W - mx, y)], fill=INK, width=2)
    y += 14

    # ---- four stories, two columns x two rows ----
    stories = [
        ("UKRAINE", "Kerch Bridge hit again as a span falls into the sea",
         "Kyiv\u2019s drones strike for a second day; Moscow answers with attacks on Kyiv\u2019s bridges."),
        ("ASIA", "Trump lands in Manila on his way to a three-way summit",
         "Quad talks open the trip; a first-ever meeting with Xi and Putin is set for Thursday in China."),
        ("HEALTH", "America loses its measles-free status",
         "The first loss since 2000, after a year of uninterrupted spread, officials confirm."),
        ("TECHNOLOGY", "Outages ripple across airports, banks and Big Tech",
         "Apple and Microsoft falter, an NSA system goes dark; no cyberattack, officials say."),
    ]
    col_w = (cw - 32) // 2
    row_h = 140
    for i, (kicker, head, body) in enumerate(stories):
        col, row = i % 2, i // 2
        x = mx + col * (col_w + 32)
        yy = y + row * row_h
        d.text((x, yy), kicker, font=SANS_B(20), fill=RED)
        yy += 28
        yy = text_block(d, x, yy, wrap(d, head, SERIF_B(27), col_w),
                        SERIF_B(27), INK, 30)
        yy = text_block(d, x, yy + 2, wrap(d, body, SANS(19), col_w),
                        SANS(19), MUTED, 23)
    y += 2 * row_h + 4

    # ---- also line + footer ----
    also = "ALSO:  Nvidia spy scandal  ·  Gaza winter emergency  ·  Japan scrambles jets"
    d.text((mx, y), also, font=SANS_B(17), fill=INK)
    y += 24
    d.line([(mx, y), (W - mx, y)], fill=INK, width=1)
    foot = "SUMMED UP FROM TUESDAY\u2019S REPORTING  ·  17 NOVEMBER 2026"
    f_foot = SANS_B(17)
    d.text(((W - d.textlength(foot, font=f_foot)) / 2, y + 10), foot,
           font=f_foot, fill=MUTED)

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
