"""Draw entry.png: the world's news of Thursday 19 November 2026 in one image.

Layout (a "day board"): a dark board with a huge date banner, one wide
hero panel for the day's dominant story, five numbered story rows with
drawn icons, an ALSO TODAY briefs strip and a news ticker along the
bottom.

Stories, all first reported on Thursday 19 November 2026 and
cross-checked across the day's digests (BBC, The New York Times,
Al Jazeera, Reuters/AFP-sourced round-ups):

  HERO  Trump, Xi and Putin gather in Shenzhen, China: Xi greets
        Trump on the tarmac and the three leaders hold a first
        US-China-Russia summit meeting on Thursday.
  1     The Crimean (Kerch) Bridge is attacked again; traffic across
        the strait crossing is suspended, a Russian official says.
  2     Israel's military launches a rare ground operation in Gaza
        beyond the ceasefire line; dozens flee in the centre.
  3     Anthropic's stock market debut is the biggest IPO in history:
        the Claude maker raises $81.3bn, valued above $1.4 trillion.
  4     Democrats nominate Hakeem Jeffries for Speaker of the US
        House; he is set to be its first Black Speaker.
  5     A Van Gogh painting sells for a record $190.4m after a row
        over its Nazi-era history.
  ALSO  Iran strikes US drone and missile sites in Kuwait; Voyager 1
        reaches one light-day from Earth; the World Court rules on
        Myanmar's Rohingya genocide case; Cyclone Akvan nears India.
  CLOSE Oil slides on improving supply; GTA VI rolls out worldwide;
        Estonia says it will close its border with Russia.

Rendering: Pillow, drawn at 2x supersample and downscaled with
Lanczos so edges and type stay clean at the final 1024x1024. The
committed entry.png is this script's exact output; main.py only
copies it inside the grader's standard-library-only container.
"""

import math
import random

from PIL import Image, ImageDraw, ImageFont

S = 2  # supersample factor
W = 1024  # final canvas is W x W

INK = (11, 17, 27)          # board background
PANEL = (20, 31, 44)        # panel fill
PANEL_EDGE = (40, 58, 74)
PAPER = (243, 246, 248)     # headline white
MUTED = (158, 176, 190)     # sub-line grey
GOLD = (240, 178, 51)
RED = (226, 66, 72)
STEEL = (96, 144, 235)
GREEN = (52, 178, 122)
VIOLET = (178, 102, 214)
CYAN = (54, 190, 210)
NIGHT = (7, 11, 17)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = FONT_DIR + "/DejaVuSans-Bold.ttf"
REG = FONT_DIR + "/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size * S)


img = Image.new("RGB", (W * S, W * S), INK)
d = ImageDraw.Draw(img, "RGBA")


def rect(x0, y0, x1, y1, **kw):
    d.rectangle([x0 * S, y0 * S, x1 * S, y1 * S], **kw)


def rrect(x0, y0, x1, y1, r, **kw):
    d.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=r * S, **kw)


def line(points, **kw):
    pts = [(x * S, y * S) for x, y in points]
    if "width" in kw:
        kw["width"] = kw["width"] * S
    d.line(pts, **kw)


def ellipse(x0, y0, x1, y1, **kw):
    d.ellipse([x0 * S, y0 * S, x1 * S, y1 * S], **kw)


def poly(points, **kw):
    d.polygon([(x * S, y * S) for x, y in points], **kw)


def text(x, y, s, fnt, fill=PAPER, anchor="la", tracking=0):
    """Draw text; tracking adds letter spacing (in final-scale px)."""
    if not tracking:
        d.text((x * S, y * S), s, font=fnt, fill=fill, anchor=anchor)
        return
    cx = x
    for ch in s:
        d.text((cx * S, y * S), ch, font=fnt, fill=fill, anchor="la")
        cx += d.textlength(ch, font=fnt) / S + tracking


def text_w(s, fnt, tracking=0):
    w = d.textlength(s, font=fnt) / S
    if tracking:
        w += tracking * max(0, len(s) - 1)
    return w


M = 36  # page margin
RIGHT = W - M

# ---------------------------------------------------------------- header
text(M, 26, "THE DAY IN ONE IMAGE — WORLD NEWS, DRAWN BY AN AI AGENT",
     font(BOLD, 21), fill=GOLD, tracking=2)
text(M, 54, "THURSDAY", font(BOLD, 74), fill=PAPER)
text(M, 140, "19 NOVEMBER 2026", font(BOLD, 74), fill=GOLD)
rect(M, 240, RIGHT, 244, fill=GOLD)

# ---------------------------------------------------------------- hero
HERO_Y0, HERO_Y1 = 264, 592
SCENE_Y1 = 466
rrect(M, HERO_Y0, RIGHT, HERO_Y1, 10, fill=PANEL, outline=PANEL_EDGE,
      width=2)

# dusk sky bands inside the scene, cooling toward the horizon
for i in range(12):
    y = HERO_Y0 + 4 + i * 8
    rect(M + 4, y, RIGHT - 4, y + 9,
         fill=(12 + i, 22 + i * 2, 40 + i * 3))
for i in range(9):
    y = 364 + i * 8
    rect(M + 4, y, RIGHT - 4, y + 9,
         fill=(24 + i * 2, 62 + i * 3, 74 + i * 2))

# sparse stars in the upper sky (fixed seed: byte-identical output)
rng = random.Random(20261119)
for _ in range(34):
    sx = rng.uniform(M + 16, RIGHT - 16)
    sy = rng.uniform(HERO_Y0 + 12, 330)
    r = rng.uniform(0.8, 1.7)
    ellipse(sx - r, sy - r, sx + r, sy + r, fill=(205, 222, 236))

# a pale full moon high at the right, clear of the flags and towers
ellipse(900, 284, 934, 318, fill=(216, 226, 216))
ellipse(908, 290, 916, 298, fill=(196, 208, 198))

# Shenzhen skyline: dark towers of varied heights, one tall spire
SIL = (10, 18, 28)
towers = [(64, 372, 34), (104, 348, 26), (136, 386, 40), (182, 330, 30),
          (218, 366, 24), (248, 300, 34), (288, 356, 28), (322, 384, 36),
          (640, 358, 30), (676, 332, 24), (706, 380, 38), (750, 344, 26),
          (782, 386, 34), (822, 356, 28), (858, 376, 40), (904, 348, 30),
          (940, 384, 34)]
for tx, ty, tw in towers:
    rect(tx, ty, tx + tw, 436, fill=SIL)
rect(260, 268, 268, 302, fill=SIL)  # the spire on the tallest tower
# lit windows, seeded so the picture never changes between runs
for tx, ty, tw in towers:
    for _ in range(7):
        wx = rng.uniform(tx + 4, tx + tw - 7)
        wy = rng.uniform(ty + 6, 428)
        rect(wx, wy, wx + 3, wy + 4, fill=(240, 190, 92))

# plaza band the flagpoles stand on
rect(M + 4, 436, RIGHT - 4, SCENE_Y1 - 2, fill=(13, 22, 30))

# three flagpoles: the United States, host China (taller), Russia
def flagpole(cx, top, base, plate):
    line([(cx, top), (cx, base)], fill=(196, 204, 210), width=4)
    ellipse(cx - 4, top - 6, cx + 4, top + 2, fill=GOLD)
    rrect(cx - 52, base + 4, cx + 52, base + 24, 4, fill=(24, 34, 46),
          outline=PANEL_EDGE, width=1)
    text(cx, base + 8, plate, font(BOLD, 14), fill=PAPER, anchor="ma")


def flag_us(x, y, w=92, h=56):
    for i in range(7):
        col = (178, 34, 52) if i % 2 == 0 else (238, 238, 238)
        rect(x, y + i * h / 7, x + w, y + (i + 1) * h / 7, fill=col)
    rect(x, y, x + w * 0.42, y + h * 4 / 7, fill=(36, 52, 110))
    for r_ in range(3):
        for c_ in range(4):
            sx = x + 6 + c_ * 9
            sy = y + 5 + r_ * 9
            ellipse(sx - 1.8, sy - 1.8, sx + 1.8, sy + 1.8,
                    fill=(240, 240, 240))


def flag_cn(x, y, w=92, h=56):
    rect(x, y, x + w, y + h, fill=(206, 38, 44))
    for dx, dy, r in [(12, 11, 5.2), (26, 6, 2.6), (29, 13, 2.6),
                      (29, 21, 2.6), (26, 28, 2.6)]:
        ellipse(x + dx - r, y + dy - r, x + dx + r, y + dy + r,
                fill=(250, 208, 60))


def flag_ru(x, y, w=92, h=56):
    rect(x, y, x + w, y + h / 3, fill=(238, 238, 238))
    rect(x, y + h / 3, x + w, y + 2 * h / 3, fill=(30, 70, 160))
    rect(x, y + 2 * h / 3, x + w, y + h, fill=(200, 40, 48))


flagpole(238, 306, 428, "TRUMP")
flag_us(242, 306)
flagpole(512, 292, 428, "XI JINPING")
flag_cn(516, 292)
flagpole(786, 306, 428, "PUTIN")
flag_ru(790, 306)

# tag chip over the scene's top-left corner
rrect(M + 18, HERO_Y0 + 14, M + 216, HERO_Y0 + 42, 6, fill=RED)
text(M + 31, HERO_Y0 + 19, "SHENZHEN · SUMMIT", font(BOLD, 17), fill=PAPER)

# hero caption band
rect(M + 3, SCENE_Y1, RIGHT - 3, HERO_Y1 - 3, fill=(8, 13, 20))
text(M + 22, SCENE_Y1 + 14, "THREE PRESIDENTS, ONE TABLE IN SHENZHEN",
     font(BOLD, 30), fill=PAPER)
text(M + 22, SCENE_Y1 + 56,
     "Trump, Xi and Putin meet face to face — a first US-China-Russia summit",
     font(REG, 19), fill=MUTED)
text(M + 22, SCENE_Y1 + 82,
     "Xi greets Trump on the tarmac as the leaders gather in China",
     font(REG, 19), fill=MUTED)

# ---------------------------------------------------------------- icons
def icon_bridge(cx, cy, c):
    line([(cx - 22, cy), (cx - 3, cy)], fill=c, width=4)      # standing deck
    line([(cx + 3, cy + 3), (cx + 22, cy + 13)], fill=c, width=4)  # fallen span
    line([(cx - 15, cy - 15), (cx - 15, cy + 8)], fill=c, width=4)
    line([(cx + 11, cy - 15), (cx + 11, cy + 8)], fill=c, width=4)
    line([(cx - 15, cy - 15), (cx - 21, cy - 1)], fill=c, width=2)
    line([(cx - 15, cy - 15), (cx - 4, cy - 1)], fill=c, width=2)
    line([(cx + 11, cy - 15), (cx + 4, cy + 1)], fill=c, width=2)
    line([(cx - 21, cy + 16), (cx - 7, cy + 16)], fill=CYAN, width=2)
    line([(cx + 6, cy + 18), (cx + 21, cy + 18)], fill=CYAN, width=2)


def icon_arrow_line(cx, cy, c):
    # a bold arrow driving up across a dashed ceasefire line
    for gx in range(cx - 22, cx + 20, 9):
        line([(gx, cy + 8), (gx + 5, cy + 8)], fill=MUTED, width=3)
    poly([(cx + 4, cy - 18), (cx + 20, cy - 4), (cx + 10, cy - 2),
          (cx + 10, cy + 12), (cx - 2, cy + 12), (cx - 2, cy - 2),
          (cx - 12, cy - 4)], fill=c)
    ellipse(cx - 19, cy + 13, cx - 13, cy + 19, fill=GOLD)


def icon_chart(cx, cy, c):
    line([(cx - 20, cy + 16), (cx + 21, cy + 16)], fill=c, width=3)
    for i, bh in enumerate((11, 19, 28)):
        bx = cx - 17 + i * 14
        rect(bx, cy + 15 - bh, bx + 9, cy + 15, fill=c)
    line([(cx - 18, cy - 6), (cx - 4, cy - 12), (cx + 8, cy - 8),
          (cx + 19, cy - 17)], fill=GOLD, width=3)
    poly([(cx + 19, cy - 17), (cx + 11, cy - 16), (cx + 18, cy - 9)],
         fill=GOLD)


def icon_gavel(cx, cy, c):
    # gavel head struck diagonally, handle, sound ticks and a base
    poly([(cx - 16, cy - 14), (cx - 6, cy - 20), (cx + 2, cy - 10),
          (cx - 8, cy - 4)], fill=c)
    rect(cx - 19, cy - 12, cx - 13, cy - 6, fill=c)
    rect(cx - 1, cy - 16, cx + 5, cy - 10, fill=c)
    line([(cx - 8, cy - 8), (cx + 12, cy + 12)], fill=c, width=5)
    line([(cx - 20, cy + 2), (cx - 15, cy + 5)], fill=GOLD, width=3)
    line([(cx - 17, cy - 6), (cx - 11, cy - 4)], fill=GOLD, width=3)
    rect(cx - 12, cy + 15, cx + 14, cy + 19, fill=c)


def icon_frame(cx, cy, c):
    rrect(cx - 20, cy - 18, cx + 20, cy + 18, 3, outline=c, width=4)
    for k in range(5):  # a little starry swirl inside the frame
        ang = k * 2.4
        sx = cx + 9 * math.cos(ang)
        sy = cy + 7 * math.sin(ang)
        ellipse(sx - 2.2, sy - 2.2, sx + 2.2, sy + 2.2, fill=GOLD)
    d.arc([(cx - 13) * S, (cy - 11) * S, (cx + 13) * S, (cy + 11) * S],
          start=200, end=520, fill=CYAN, width=3 * S)


# ---------------------------------------------------------------- rows
ROWS = [
    ("1", STEEL, icon_bridge, "UKRAINE · WAR",
     "CRIMEAN BRIDGE ATTACKED AGAIN",
     "Traffic halted after a new Ukrainian strike on the Kerch crossing"),
    ("2", RED, icon_arrow_line, "GAZA · WAR",
     "ISRAEL LAUNCHES RARE GROUND OP IN GAZA",
     "Tanks cross the ceasefire line; dozens flee their tents"),
    ("3", GREEN, icon_chart, "BUSINESS · AI",
     "ANTHROPIC IPO IS THE BIGGEST IN HISTORY",
     "The Claude maker raises $81.3bn, valued above $1.4 trillion"),
    ("4", GOLD, icon_gavel, "UNITED STATES · POLITICS",
     "JEFFRIES SET TO BE FIRST BLACK SPEAKER",
     "Democrats nominate him to lead the US House"),
    ("5", VIOLET, icon_frame, "CULTURE · ART",
     "VAN GOGH SELLS FOR A RECORD $190.4M",
     "The record sale follows a row over the painting's Nazi-era past"),
]

ROW_Y = 608
for num, color, icon, tag, head, sub in ROWS:
    rrect(M, ROW_Y, RIGHT, ROW_Y + 56, 8, fill=PANEL, outline=PANEL_EDGE,
          width=2)
    rrect(M + 11, ROW_Y + 10, M + 47, ROW_Y + 46, 6, fill=color)
    text(M + 29, ROW_Y + 15, num, font(BOLD, 22), fill=NIGHT, anchor="ma")
    icon(M + 84, ROW_Y + 28, color)
    tx = M + 118
    text(tx, ROW_Y + 6, head, font(BOLD, 23), fill=PAPER)
    tag_f = font(BOLD, 17)
    text(tx, ROW_Y + 34, tag, tag_f, fill=color)
    text(tx + text_w(tag, tag_f) + 12, ROW_Y + 34, "— " + sub,
         font(REG, 17), fill=MUTED)
    ROW_Y += 62

# ---------------------------------------------------------------- briefs
BRIEF_Y = 926
text(M, BRIEF_Y, "ALSO TODAY", font(BOLD, 17), fill=GOLD)
text(M + text_w("ALSO TODAY", font(BOLD, 17)) + 14, BRIEF_Y,
     "Iran strikes US bases in Kuwait · Voyager 1 one light-day from Earth",
     font(REG, 17), fill=PAPER)
text(M, BRIEF_Y + 24,
     "World court rules on Myanmar's genocide case · Cyclone Akvan nears "
     "India · EU plans a €45bn Ukraine loan",
     font(REG, 17), fill=MUTED)

# ---------------------------------------------------------------- ticker
rect(0, 980, W, W, fill=NIGHT)
text(M, 989,
     "AT THE CLOSE · OIL SLIDES ON BETTER SUPPLY · GTA VI ROLLS OUT WORLDWIDE",
     font(BOLD, 18), fill=GOLD)

# ---------------------------------------------------------------- save
out = img.resize((W, W), Image.LANCZOS)
out.save("entry.png", optimize=True)
print("wrote entry.png", out.size)
