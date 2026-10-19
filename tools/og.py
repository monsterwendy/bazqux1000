#!/usr/bin/env python3
"""Regenerates the bazqux1000 OG/embed image (1200x630).
usage: python3 og.py --title "BAZQUX1000" --subtitle "edit audio metadata in browser" -o og.png
"""
import argparse, math
from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
BADGES = [  # label, bg, text
    ("MP3",  (80, 30, 30),  (180, 60, 60)),
    ("FLAC", (30, 60, 30),  (60, 140, 60)),
    ("M4A",  (30, 30, 80),  (60, 90, 180)),
    ("AAC",  (20, 20, 70),  (80, 110, 210)),
    ("ALAC", (50, 38, 5),   (200, 160, 40)),
    ("OGG",  (60, 30, 80),  (120, 60, 180)),
    ("OPUS", (30, 60, 70),  (60, 150, 160)),
]

def lerp(a, b, t): return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", default="BAZQUX1000")
    ap.add_argument("--subtitle", default="edit audio metadata in browser")
    ap.add_argument("-o", "--out", default="og.png")
    a = ap.parse_args()

    W, H = 1200, 630
    im = Image.new("RGB", (W, H), (10, 10, 10))
    d = ImageDraw.Draw(im)
    for x in range(0, W, 40): d.line([(x, 0), (x, H)], fill=(20, 20, 20))
    for y in range(0, H, 40): d.line([(0, y), (W, y)], fill=(20, 20, 20))

    # waveform: 13px bars every 20px, two sin^2 lobes around y=220
    cy = 220
    for x in range(4, W, 20):
        c = x + 6
        h = 7
        if 30 <= c <= 545: h += 88 * math.sin(math.pi * (c - 30) / 515) ** 2
        if 545 <= c <= 1080: h += 110 * math.sin(math.pi * (c - 545) / 535) ** 2
        col = lerp((0, 200, 180), (20, 255, 80), c / W)
        d.rectangle([x, cy - h, x + 12, cy + h], fill=col)

    title_font = ImageFont.truetype(FONT, 72)
    sub_font = ImageFont.truetype(FONT, 22)
    badge_font = ImageFont.truetype(FONT, 20)
    d.text((62, 395), a.title, font=title_font, fill=(255, 255, 255))
    d.text((62, 482), a.subtitle, font=sub_font, fill=(100, 100, 100))

    x = 62
    for label, bg, fg in BADGES:
        tw = d.textlength(label, font=badge_font)
        w = int(tw + 20)
        d.rectangle([x, 525, x + w, 557], fill=bg)
        d.text((x + 10, 529), label, font=badge_font, fill=fg)
        x += w + 9
    im.save(a.out)
    print("wrote", a.out)

if __name__ == "__main__":
    main()
