"""Paint entry.png - the world news of Thursday 19 November 2026, in one image.

The board: a dark slate with a big date masthead, a wide hero panel
for the day's biggest story, five numbered story rows with small
drawn icons, an ALSO TODAY strip of briefs and a closing ticker.

The stories were all first reported on Thursday 19 November 2026 and
cross-checked across the day's digests (BBC, The New York Times,
Al Jazeera and Reuters/AFP-sourced round-ups):

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
  CLOSE Oil slides on improving supply; GTA VI rolls out worldwide.

Pillow paints at twice size and a Lanczos downscale keeps the type
crisp at 1024x1024. The committed entry.png is this script's exact
output; main.py only copies it inside the grader's container, which
installs nothing and has no Pillow.
"""

import math
import random

from PIL import Image, ImageDraw, ImageFont

SS = 2        # supersample factor
SIZE = 1024   # final canvas is SIZE x SIZE


def _rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


PAL = {name: _rgb(h) for name, h in {
    "board": "0B111B", "panel": "141F2C", "edge": "283A4A",
    "paper": "F3F6F8", "muted": "9EB0BE", "gold": "F0B233",
    "red": "E24248", "steel": "6090EB", "green": "34B27A",
    "violet": "B266D6", "cyan": "36BED2", "night": "070B11",
}.items()}

FONT_AT = "/usr/share/fonts/truetype/dejavu/"
_font_cache = {}


def F(bold, px):
    key = (bold, px)
    if key not in _font_cache:
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
        _font_cache[key] = ImageFont.truetype(FONT_AT + name, px * SS)
    return _font_cache[key]


canvas = Image.new("RGB", (SIZE * SS, SIZE * SS), PAL["board"])
dr = ImageDraw.Draw(canvas, "RGBA")


def _sc(box):
    return [v * SS for v in box]


def box(x0, y0, x1, y1, **kw):
    dr.rectangle(_sc([x0, y0, x1, y1]), **kw)


def rbox(x0, y0, x1, y1, rad, **kw):
    dr.rounded_rectangle(_sc([x0, y0, x1, y1]), radius=rad * SS, **kw)


def seg(points, **kw):
    if "width" in kw:
        kw["width"] = kw["width"] * SS
    dr.line([(x * SS, y * SS) for x, y in points], **kw)


def oval(x0, y0, x1, y1, **kw):
    dr.ellipse(_sc([x0, y0, x1, y1]), **kw)


def shape(points, **kw):
    dr.polygon([(x * SS, y * SS) for x, y in points], **kw)


def put(x, y, s, fnt, fill=None, anchor="la", tracking=0):
    fill = PAL["paper"] if fill is None else fill
    if tracking == 0:
        dr.text((x * SS, y * SS), s, font=fnt, fill=fill, anchor=anchor)
        return
    cx = x
    for ch in s:
        dr.text((cx * SS, y * SS), ch, font=fnt, fill=fill, anchor="la")
        cx += dr.textlength(ch, font=fnt) / SS + tracking


def width_of(s, fnt, tracking=0):
    w = dr.textlength(s, font=fnt) / SS
    return w + (tracking * max(0, len(s) - 1) if tracking else 0)


EDGE_L = 36
EDGE_R = SIZE - EDGE_L


def masthead():
    put(EDGE_L, 26, "THE DAY IN ONE IMAGE — WORLD NEWS, DRAWN BY AN AI AGENT",
        F(True, 21), fill=PAL["gold"], tracking=2)
    put(EDGE_L, 54, "THURSDAY", F(True, 74))
    put(EDGE_L, 140, "19 NOVEMBER 2026", F(True, 74), fill=PAL["gold"])
    box(EDGE_L, 240, EDGE_R, 244, fill=PAL["gold"])


HERO_TOP, HERO_BOT = 264, 592
SCENE_BOT = 466


def hero():
    rbox(EDGE_L, HERO_TOP, EDGE_R, HERO_BOT, 10,
         fill=PAL["panel"], outline=PAL["edge"], width=2)
    # dusk sky: two stacks of bands cooling toward the horizon
    for i in range(12):
        y = HERO_TOP + 4 + i * 8
        box(EDGE_L + 4, y, EDGE_R - 4, y + 9,
            fill=(12 + i, 22 + i * 2, 40 + i * 3))
    for i in range(9):
        y = 364 + i * 8
        box(EDGE_L + 4, y, EDGE_R - 4, y + 9,
            fill=(24 + i * 2, 62 + i * 3, 74 + i * 2))
    # sparse stars (seeded: the picture is byte-identical every run)
    rng = random.Random(20261119)
    for _ in range(34):
        sx = rng.uniform(EDGE_L + 16, EDGE_R - 16)
        sy = rng.uniform(HERO_TOP + 12, 330)
        r = rng.uniform(0.8, 1.7)
        oval(sx - r, sy - r, sx + r, sy + r, fill=(205, 222, 236))
    # a pale full moon high at the right, clear of flags and towers
    oval(900, 284, 934, 318, fill=(216, 226, 216))
    oval(908, 290, 916, 298, fill=(196, 208, 198))
    # Shenzhen skyline silhouettes with lit windows, one tall spire
    sil = (10, 18, 28)
    towers = [(64, 372, 34), (104, 348, 26), (136, 386, 40),
              (182, 330, 30), (218, 366, 24), (248, 300, 34),
              (288, 356, 28), (322, 384, 36), (640, 358, 30),
              (676, 332, 24), (706, 380, 38), (750, 344, 26),
              (782, 386, 34), (822, 356, 28), (858, 376, 40),
              (904, 348, 30), (940, 384, 34)]
    for tx, ty, tw in towers:
        box(tx, ty, tx + tw, 436, fill=sil)
    box(260, 268, 268, 302, fill=sil)
    for tx, ty, tw in towers:
        for _ in range(7):
            wx = rng.uniform(tx + 4, tx + tw - 7)
            wy = rng.uniform(ty + 6, 428)
            box(wx, wy, wx + 3, wy + 4, fill=(240, 190, 92))
    # plaza band the flagpoles stand on
    box(EDGE_L + 4, 436, EDGE_R - 4, SCENE_BOT - 2, fill=(13, 22, 30))

    def pole(cx, top, base, plate):
        seg([(cx, top), (cx, base)], fill=(196, 204, 210), width=4)
        oval(cx - 4, top - 6, cx + 4, top + 2, fill=PAL["gold"])
        rbox(cx - 52, base + 4, cx + 52, base + 24, 4,
             fill=(24, 34, 46), outline=PAL["edge"], width=1)
        put(cx, base + 8, plate, F(True, 14), anchor="ma")

    def flag_us(x, y, w=92, h=56):
        stripes = [(178, 34, 52), (238, 238, 238)]
        for i in range(7):
            box(x, y + i * h / 7, x + w, y + (i + 1) * h / 7,
                fill=stripes[i % 2])
        box(x, y, x + w * 0.42, y + h * 4 / 7, fill=(36, 52, 110))
        for r_ in range(3):
            for c_ in range(4):
                sx, sy = x + 6 + c_ * 9, y + 5 + r_ * 9
                oval(sx - 1.8, sy - 1.8, sx + 1.8, sy + 1.8,
                     fill=(240, 240, 240))

    def flag_cn(x, y, w=92, h=56):
        box(x, y, x + w, y + h, fill=(206, 38, 44))
        for dx, dy, r in [(12, 11, 5.2), (26, 6, 2.6), (29, 13, 2.6),
                          (29, 21, 2.6), (26, 28, 2.6)]:
            oval(x + dx - r, y + dy - r, x + dx + r, y + dy + r,
                 fill=(250, 208, 60))

    def flag_ru(x, y, w=92, h=56):
        thirds = [(238, 238, 238), (30, 70, 160), (200, 40, 48)]
        for i, col in enumerate(thirds):
            box(x, y + i * h / 3, x + w, y + (i + 1) * h / 3, fill=col)

    pole(238, 306, 428, "TRUMP")
    flag_us(242, 306)
    pole(512, 292, 428, "XI JINPING")
    flag_cn(516, 292)
    pole(786, 306, 428, "PUTIN")
    flag_ru(790, 306)

    # tag chip over the scene's top-left corner
    rbox(EDGE_L + 18, HERO_TOP + 14, EDGE_L + 216, HERO_TOP + 42, 6,
         fill=PAL["red"])
    put(EDGE_L + 31, HERO_TOP + 19, "SHENZHEN · SUMMIT", F(True, 17))
    # caption band under the scene
    box(EDGE_L + 3, SCENE_BOT, EDGE_R - 3, HERO_BOT - 3, fill=(8, 13, 20))
    put(EDGE_L + 22, SCENE_BOT + 14,
        "THREE PRESIDENTS, ONE TABLE IN SHENZHEN", F(True, 30))
    put(EDGE_L + 22, SCENE_BOT + 56,
        "Trump, Xi and Putin meet face to face — a first US-China-Russia "
        "summit", F(False, 19), fill=PAL["muted"])
    put(EDGE_L + 22, SCENE_BOT + 82,
        "Xi greets Trump on the tarmac as the leaders gather in China",
        F(False, 19), fill=PAL["muted"])


def ic_bridge(cx, cy, c):
    strokes = [((cx - 22, cy), (cx - 3, cy), 4),
               ((cx + 3, cy + 3), (cx + 22, cy + 13), 4),
               ((cx - 15, cy - 15), (cx - 15, cy + 8), 4),
               ((cx + 11, cy - 15), (cx + 11, cy + 8), 4),
               ((cx - 15, cy - 15), (cx - 21, cy - 1), 2),
               ((cx - 15, cy - 15), (cx - 4, cy - 1), 2),
               ((cx + 11, cy - 15), (cx + 4, cy + 1), 2)]
    for a, b, w in strokes:
        seg([a, b], fill=c, width=w)
    seg([(cx - 21, cy + 16), (cx - 7, cy + 16)], fill=PAL["cyan"], width=2)
    seg([(cx + 6, cy + 18), (cx + 21, cy + 18)], fill=PAL["cyan"], width=2)


def ic_arrow(cx, cy, c):
    gx = cx - 22
    while gx < cx + 20:
        seg([(gx, cy + 8), (gx + 5, cy + 8)], fill=PAL["muted"], width=3)
        gx += 9
    shape([(cx + 4, cy - 18), (cx + 20, cy - 4), (cx + 10, cy - 2),
           (cx + 10, cy + 12), (cx - 2, cy + 12), (cx - 2, cy - 2),
           (cx - 12, cy - 4)], fill=c)
    oval(cx - 19, cy + 13, cx - 13, cy + 19, fill=PAL["gold"])


def ic_chart(cx, cy, c):
    seg([(cx - 20, cy + 16), (cx + 21, cy + 16)], fill=c, width=3)
    for i, bh in enumerate((11, 19, 28)):
        bx = cx - 17 + i * 14
        box(bx, cy + 15 - bh, bx + 9, cy + 15, fill=c)
    seg([(cx - 18, cy - 6), (cx - 4, cy - 12), (cx + 8, cy - 8),
         (cx + 19, cy - 17)], fill=PAL["gold"], width=3)
    shape([(cx + 19, cy - 17), (cx + 11, cy - 16), (cx + 18, cy - 9)],
          fill=PAL["gold"])


def ic_gavel(cx, cy, c):
    shape([(cx - 16, cy - 14), (cx - 6, cy - 20), (cx + 2, cy - 10),
           (cx - 8, cy - 4)], fill=c)
    box(cx - 19, cy - 12, cx - 13, cy - 6, fill=c)
    box(cx - 1, cy - 16, cx + 5, cy - 10, fill=c)
    seg([(cx - 8, cy - 8), (cx + 12, cy + 12)], fill=c, width=5)
    seg([(cx - 20, cy + 2), (cx - 15, cy + 5)], fill=PAL["gold"], width=3)
    seg([(cx - 17, cy - 6), (cx - 11, cy - 4)], fill=PAL["gold"], width=3)
    box(cx - 12, cy + 15, cx + 14, cy + 19, fill=c)


def ic_frame(cx, cy, c):
    rbox(cx - 20, cy - 18, cx + 20, cy + 18, 3, outline=c, width=4)
    for k in range(5):
        ang = k * 2.4
        sx = cx + 9 * math.cos(ang)
        sy = cy + 7 * math.sin(ang)
        oval(sx - 2.2, sy - 2.2, sx + 2.2, sy + 2.2, fill=PAL["gold"])
    dr.arc(_sc([cx - 13, cy - 11, cx + 13, cy + 11]),
           start=200, end=520, fill=PAL["cyan"], width=3 * SS)


STORIES = [
    ("1", "steel", ic_bridge, "UKRAINE · WAR",
     "CRIMEAN BRIDGE ATTACKED AGAIN",
     "Traffic halted after a new Ukrainian strike on the Kerch crossing"),
    ("2", "red", ic_arrow, "GAZA · WAR",
     "ISRAEL LAUNCHES RARE GROUND OP IN GAZA",
     "Tanks cross the ceasefire line; dozens flee their tents"),
    ("3", "green", ic_chart, "BUSINESS · AI",
     "ANTHROPIC IPO IS THE BIGGEST IN HISTORY",
     "The Claude maker raises $81.3bn, valued above $1.4 trillion"),
    ("4", "gold", ic_gavel, "UNITED STATES · POLITICS",
     "JEFFRIES SET TO BE FIRST BLACK SPEAKER",
     "Democrats nominate him to lead the US House"),
    ("5", "violet", ic_frame, "CULTURE · ART",
     "VAN GOGH SELLS FOR A RECORD $190.4M",
     "The record sale follows a row over the painting's Nazi-era past"),
]


def story_rows():
    y = 608
    for num, cname, icon, tag, head, sub in STORIES:
        col = PAL[cname]
        rbox(EDGE_L, y, EDGE_R, y + 56, 8,
             fill=PAL["panel"], outline=PAL["edge"], width=2)
        rbox(EDGE_L + 11, y + 10, EDGE_L + 47, y + 46, 6, fill=col)
        put(EDGE_L + 29, y + 15, num, F(True, 22),
            fill=PAL["night"], anchor="ma")
        icon(EDGE_L + 84, y + 28, col)
        tx = EDGE_L + 118
        put(tx, y + 6, head, F(True, 23))
        tag_f = F(True, 17)
        put(tx, y + 34, tag, tag_f, fill=col)
        put(tx + width_of(tag, tag_f) + 12, y + 34, "— " + sub,
            F(False, 17), fill=PAL["muted"])
        y += 62


def briefs_and_ticker():
    by = 926
    put(EDGE_L, by, "ALSO TODAY", F(True, 17), fill=PAL["gold"])
    put(EDGE_L + width_of("ALSO TODAY", F(True, 17)) + 14, by,
        "Iran strikes US bases in Kuwait · Voyager 1 one light-day "
        "from Earth", F(False, 17))
    put(EDGE_L, by + 24,
        "World court rules on Myanmar's genocide case · Cyclone Akvan "
        "nears India · EU plans a €45bn Ukraine loan",
        F(False, 17), fill=PAL["muted"])
    box(0, 980, SIZE, SIZE, fill=PAL["night"])
    put(EDGE_L, 989,
        "AT THE CLOSE · OIL SLIDES ON BETTER SUPPLY · GTA VI ROLLS "
        "OUT WORLDWIDE", F(True, 18), fill=PAL["gold"])


masthead()
hero()
story_rows()
briefs_and_ticker()

final = canvas.resize((SIZE, SIZE), Image.LANCZOS)
final.save("entry.png", optimize=True)
print("wrote entry.png", final.size)
