"""news-image-20261125 v3: The Daily Globe — 49 verified stories of Wed 25 Nov 2026.
Fresh render, stdlib-only entrypoint copies entry.png to /output. Layout 1024x1024:
giant date masthead, 6-number stat strip, 3 detailed heroes, 10 medium panels,
dot-matrix world map with numbered pins, 36-item ALSO list, DATE CHECK band, footer.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 241, 222)
INK = (26, 26, 26)
RED = (176, 30, 30)
NAVY = (31, 58, 95)
GREY = (110, 110, 105)
SEA = (220, 232, 234)
LAND = (122, 106, 69)
WHITE = (255, 255, 255)
CARD = (255, 253, 246)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
OVERFLOW = []


def font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except Exception:
        return ImageFont.load_default()


F_TITLE = font("DejaVuSans-Bold.ttf", 50)
F_SUB = font("DejaVuSans-Bold.ttf", 12)
F_STRIP = font("DejaVuSans-Bold.ttf", 10)
F_STATNUM = font("DejaVuSans-Bold.ttf", 32)
F_STATLBL = font("DejaVuSans.ttf", 10)
F_KICK = font("DejaVuSans-Bold.ttf", 10)
F_HEAD = font("DejaVuSans-Bold.ttf", 16)
F_DECK = font("DejaVuSans.ttf", 11)
F_SRC = font("DejaVuSans-Bold.ttf", 9)
F_MEDKICK = font("DejaVuSans-Bold.ttf", 9)
F_MEDHEAD = font("DejaVuSans-Bold.ttf", 12)
F_MEDDECK = font("DejaVuSans.ttf", 10)
F_MAPT = font("DejaVuSans-Bold.ttf", 14)
F_MAPL = font("DejaVuSans.ttf", 10)
F_ALSOH = font("DejaVuSans-Bold.ttf", 12)
F_ALSO = font("DejaVuSans.ttf", 10)
F_ALSON = font("DejaVuSans-Bold.ttf", 10)
F_DC = font("DejaVuSans-Bold.ttf", 11)
F_FOOT = font("DejaVuSans.ttf", 10)
F_PIN = font("DejaVuSans-Bold.ttf", 10)


def wrap(f, text, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if f.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def check(label, lines, max_lines, f, max_w):
    for ln in lines:
        if f.getlength(ln) > max_w:
            OVERFLOW.append(label + ": line too wide: " + ln)
    if len(lines) > max_lines:
        OVERFLOW.append(label + ": %d lines, max %d" % (len(lines), max_lines))


def draw_lines(d, lines, x, y, f, fill, lh):
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


STATS = [
    ("1st", "first Pakistani astronaut to visit Tiangong"),
    ("490,334", "Russian soldiers dead, BBC finds"),
    ("£2,166", "Ofgem energy cap from January, +26%"),
    ("8:30", "US PCE + GDP due 8:30 a.m. ET"),
    ("3.8%", "Australia trimmed-mean inflation"),
    ("9,500 lb", "lead azide detonated in Iowa"),
]

HEROES = [
    {"num": 1, "kicker": "JIUQUAN • SPACE",
     "head": "Pakistan's first astronaut reaches orbit aboard Shenzhou-24",
     "deck": "Muhammad Zeeshan Ali lifts off — the first foreigner to visit China's Tiangong station.",
     "src": "REUTERS", "art": "rocket"},
    {"num": 3, "kicker": "WASHINGTON • ECONOMY",
     "head": "US inflation and growth data due at 8:30 a.m. ET",
     "deck": "October PCE and the second Q3 GDP reading land today — the last big numbers before the Fed meets.",
     "src": "BEA • REUTERS", "art": "chart"},
    {"num": 10, "kicker": "LONDON • ENERGY",
     "head": "Ofgem lifts energy cap 26% to £2,166 from January",
     "deck": "Households face bills £443 higher from January as the regulator sets the new cap.",
     "src": "REUTERS", "art": "house"},
]

MEDIUM = [
    {"num": 2, "kicker": "IOWA • SAFETY",
     "head": "9,500 lb of lead azide detonated in Iowa",
     "deck": "Controlled blast disposes of the seized explosive.", "icon": "burst"},
    {"num": 4, "kicker": "WASHINGTON • TRADE",
     "head": "US set to unveil new global tariffs",
     "deck": "Tariff findings on 16 partners expected today.", "icon": "ship"},
    {"num": 5, "kicker": "SYDNEY • ECONOMY",
     "head": "Australia inflation hotter than expected",
     "deck": "Trimmed mean 3.8% in October; rate-cut bets fade.", "icon": "coin"},
    {"num": 6, "kicker": "KYIV • WAR",
     "head": "490,334 Russian soldiers dead, BBC finds",
     "deck": "Leaked records put the toll far above official counts.", "icon": "candle"},
    {"num": 7, "kicker": "LOS ANGELES • LAW",
     "head": "Thomas Markle indicted by grand jury",
     "deck": "Meghan's father charged; FBI arrested him.", "icon": "gavel"},
    {"num": 8, "kicker": "SYDNEY • JUSTICE",
     "head": "Lamarre guilty of double murder",
     "deck": "Jury convicts Beau Lamarre over the 2024 killings.", "icon": "court"},
    {"num": 9, "kicker": "BERLIN • ECONOMY",
     "head": "Germany's Q3 GDP grows 0.1%, cut from 0.2%",
     "deck": "Destatis: final reading revised down from 0.2%.", "icon": "factory"},
    {"num": 11, "kicker": "QUITO • DIPLOMACY",
     "head": "US pauses military operations with Ecuador",
     "deck": "Joint operations paused, the NYT reports.", "icon": "flag"},
    {"num": 12, "kicker": "NEW YORK • MARKETS",
     "head": "Gold slips ahead of US inflation data",
     "deck": "Traders await the PCE reading due today.", "icon": "gold"},
    {"num": 13, "kicker": "MIDDLE EAST • ENERGY",
     "head": "Oil falls as glut fears beat Middle East disruption",
     "deck": "Crude slips despite regional tensions.", "icon": "drop"},
]

ALSO = [
    (14, "SEOUL", "Asian stocks plunge; Korea down 5.3%"),
    (15, "MUMBAI", "Indian stocks open higher on Wednesday"),
    (16, "LONDON", "Bank of England's Bailey faces MPs today"),
    (17, "WASHINGTON", "Durable goods, home sales, jobless"),
    (18, "NEW YORK", "Storms threaten Thanksgiving travel"),
    (19, "WASHINGTON", "Nvidia export deadline ends today"),
    (20, "BEIJING", "China's Chen Jining probed in graft inquiry"),
    (21, "WASHINGTON", "Attorney general dodges Nvidia probe"),
    (22, "FORT HOOD", "Fort Hood gunman seeks firing-squad delay"),
    (23, "SANTA CLARA", "Nvidia board in focus as Huang returns"),
    (24, "WASHINGTON", "Pentagon hires firm to audit base schools"),
    (25, "TENNESSEE", "Tennessee paper's new owner: Al Gore"),
    (26, "GLOBAL", "Tech outages pile up as AI raises the stakes"),
    (27, "NEW YORK", "Polly Anderson, senior AP editor, dies"),
    (28, "WASHINGTON", "Trump pardons turkeys Freedom, Feathers"),
    (29, "WASHINGTON", "Melania Trump welcomes Christmas tree"),
    (30, "SPACE", "Hera spacecraft returns to asteroid Didymos"),
    (31, "LONDON", "Citi UK chief risk officer resigns"),
    (32, "CARACAS", "Citi weighs return to Venezuela"),
    (33, "TOKYO", "Starbucks picks banks for Japan business sale"),
    (34, "CONGO", "DR Congo plane missing; rebels claim downing"),
    (35, "NIGERIA", "Nigerian king, 92, suspended for abuse claims"),
    (36, "GAZA", "Israeli strike kills Hamas security chief in Gaza"),
    (37, "DAMASCUS", "Landmine victims surge in Syria after war"),
    (38, "TAIPEI", "China-linked AI smeared Taiwan candidates"),
    (39, "DAKAR", "Senegal reinstated as 2025 Africa champs"),
    (40, "LONDON", "Two arrested over burglary at royals' home"),
    (41, "HONIARA", "Solomon Islands ends China pact for Australia"),
    (42, "WASHINGTON", "Omar home search records unsealed"),
    (43, "JOHANNESBURG", "Zimbabwean jailed for Ukraine fight bid"),
    (44, "BRUSSELS", "NATO chief vows space defence"),
    (45, "NEW DELHI", "The high cost of eating in India"),
    (46, "YAOUNDE", "Shot at 15: a life wrecked by conflict"),
    (47, "MADRID", "Clashing visions mirror a divided Spain"),
    (48, "PYONGYANG", "North Koreans jailed for being Christian"),
    (49, "KYIV", "Kyiv defends Libya strikes; Zelenskyy confirms hit"),
]

DATECHECK = [
    "Huawei verdict (24 Nov)",
    "Dow 50,000 / Nvidia -6% (24 Nov)",
    "CIA breach (24 Nov)",
    "Nepal quake (24 Nov)",
]

REGION_LINE = ("49 STORIES • ALL VERIFIED TODAY • AMERICAS 19 • EUROPE 9 • "
               "ASIA-PACIFIC 8 • AFRICA 5 • MIDDLE EAST 3 • OCEANIA 3 • GLOBAL 2")


def draw_top_strip(d):
    d.text((12, 5), "THE WORLD IN ONE DAY", font=F_STRIP, fill=INK)
    d.text((12 + 560, 5), "DAY 329 OF 2026", font=F_STRIP, fill=RED)
    brand = "THE DAILY GLOBE"
    d.text((W - 12 - F_STRIP.getlength(brand), 5), brand, font=F_STRIP, fill=INK)
    d.line([(12, 22), (W - 12, 22)], fill=RED, width=2)


def draw_masthead(d):
    title = "Wednesday 25 November 2026"
    tw = F_TITLE.getlength(title)
    d.text(((W - tw) / 2, 26), title, font=F_TITLE, fill=INK)
    sub = REGION_LINE
    sw = F_SUB.getlength(sub)
    d.text(((W - sw) / 2, 88), sub, font=F_SUB, fill=INK)
    d.line([(12, 112), (W - 12, 112)], fill=INK, width=2)


def draw_stats(d, y0, h):
    n = len(STATS)
    cw = (W - 24) / n
    for i, (num, lbl) in enumerate(STATS):
        x = 12 + i * cw
        d.line([(x, y0 + 8), (x, y0 + h - 8)], fill=(200, 190, 160), width=1)
        nw = F_STATNUM.getlength(num)
        d.text((x + (cw - nw) / 2, y0 + 8), num, font=F_STATNUM, fill=RED)
        lines = wrap(F_STATLBL, lbl, cw - 10)
        check("stat " + num, lines, 2, F_STATLBL, cw - 10)
        ly = y0 + 46
        for ln in lines[:2]:
            lw = F_STATLBL.getlength(ln)
            d.text((x + (cw - lw) / 2, ly), ln, font=F_STATLBL, fill=INK)
            ly += 13
    d.line([(12, y0 + h - 1), (W - 12, y0 + h - 1)], fill=INK, width=1)


def draw_rocket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 54))
    for sx, sy, r in [(20, 12, 1), (60, 26, 1), (110, 8, 2), (160, 30, 1),
                      (210, 14, 1), (260, 34, 2), (300, 10, 1), (90, 44, 1),
                      (180, 52, 1), (240, 48, 1)]:
        d.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r], fill=WHITE)
    cx = x + w // 2
    d.polygon([(cx - 26, y + h), (cx - 26, y + h - 22), (cx + 26, y + h - 22),
               (cx + 26, y + h)], fill=(120, 120, 120))
    d.polygon([(cx - 14, y + 18), (cx, y + 2), (cx + 14, y + 18)], fill=RED)
    d.rectangle([cx - 14, y + 18, cx + 14, y + 62], fill=WHITE)
    d.ellipse([cx - 6, y + 30, cx + 6, y + 42], fill=(90, 160, 220))
    d.rectangle([cx - 14, y + 62, cx + 14, y + 68], fill=RED)
    d.polygon([(cx - 8, y + 68), (cx, y + h - 24), (cx + 8, y + 68)],
              fill=(255, 150, 40))
    d.ellipse([cx - 34, y + h - 26, cx - 8, y + h - 6], fill=(200, 200, 200))
    d.ellipse([cx + 8, y + h - 26, cx + 34, y + h - 6], fill=(200, 200, 200))


def draw_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 238, 240))
    base = y + h - 14
    bars = [(0.35, (150, 150, 150)), (0.6, (70, 110, 170)), (0.9, (31, 58, 95))]
    bw = 46
    gap = (w - 3 * bw) / 4
    for i, (frac, col) in enumerate(bars):
        bx = x + gap + i * (bw + gap)
        bh = (h - 30) * frac
        d.rectangle([bx, base - bh, bx + bw, base], fill=col)
    d.line([(x + 10, base), (x + w - 10, base)], fill=INK, width=2)
    d.text((x + w - 52, y + 6), "%", font=font("DejaVuSans-Bold.ttf", 34),
           fill=RED)


def draw_house(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 232))
    hx, hy, hw, hh = x + 60, y + 42, 200, 52
    d.polygon([(hx - 14, hy), (hx + hw // 2, hy - 30), (hx + hw + 14, hy)],
              fill=(150, 60, 50))
    d.rectangle([hx, hy, hx + hw, hy + hh], fill=(232, 214, 170))
    d.rectangle([hx + 84, hy + 26, hx + 116, hy + hh], fill=(90, 60, 40))
    d.polygon([(x + 218, y + 8), (x + 190, y + 48), (x + 208, y + 48),
               (x + 192, y + 82), (x + 232, y + 34), (x + 212, y + 34),
               (x + 238, y + 8)], fill=(255, 200, 0))
    d.text((x + 14, y + h - 26), "£", font=font("DejaVuSans-Bold.ttf", 22),
           fill=RED)


def draw_hero(d, hx, hy, hw, hh, hero):
    d.rectangle([hx, hy, hx + hw, hy + hh], fill=CARD, outline=(180, 170, 140))
    art_h = 96
    art = hero["art"]
    if art == "rocket":
        draw_rocket(d, hx + 1, hy + 1, hw - 2, art_h)
    elif art == "chart":
        draw_chart(d, hx + 1, hy + 1, hw - 2, art_h)
    else:
        draw_house(d, hx + 1, hy + 1, hw - 2, art_h)
    n = str(hero["num"])
    d.ellipse([hx + hw - 32, hy + 6, hx + hw - 8, hy + 30], fill=RED)
    nw = F_PIN.getlength(n)
    d.text((hx + hw - 20 - nw / 2, hy + 10), n, font=F_PIN, fill=WHITE)
    ty = hy + art_h + 8
    d.text((hx + 10, ty), hero["kicker"], font=F_KICK, fill=NAVY)
    ty += 14
    lines = wrap(F_HEAD, hero["head"], hw - 20)
    check("hero head " + n, lines, 2, F_HEAD, hw - 20)
    ty = draw_lines(d, lines[:2], hx + 10, ty, F_HEAD, INK, 19)
    ty += 3
    dlines = wrap(F_DECK, hero["deck"], hw - 20)
    check("hero deck " + n, dlines, 2, F_DECK, hw - 20)
    ty = draw_lines(d, dlines[:2], hx + 10, ty, F_DECK, INK, 14)
    d.text((hx + 10, hy + hh - 16), hero["src"], font=F_SRC, fill=RED)
    d.text((hx + hw - 10 - F_SRC.getlength("REPORTED TODAY"), hy + hh - 16),
           "REPORTED TODAY", font=F_SRC, fill=RED)


def draw_icon(d, x, y, s, kind):
    c = (31, 58, 95)
    if kind == "burst":
        for ang in range(0, 360, 30):
            import math
            r1, r2 = s * 0.28, s * 0.5
            a = math.radians(ang)
            d.line([(x + s / 2, y + s / 2),
                    (x + s / 2 + r2 * math.cos(a), y + s / 2 + r2 * math.sin(a))],
                   fill=(200, 60, 40), width=3)
        d.ellipse([x + s * 0.3, y + s * 0.3, x + s * 0.7, y + s * 0.7],
                  fill=(255, 150, 40))
    elif kind == "ship":
        d.polygon([(x + 4, y + s - 8), (x + s - 4, y + s - 8),
                   (x + s - 10, y + s - 2), (x + 10, y + s - 2)], fill=c)
        d.rectangle([x + s / 2 - 1, y + 4, x + s / 2 + 1, y + s - 10], fill=c)
        d.polygon([(x + s / 2 + 1, y + 5), (x + s - 6, y + s - 12),
                   (x + s / 2 + 1, y + s - 12)], fill=RED)
    elif kind == "coin":
        d.ellipse([x + 2, y + 2, x + s - 2, y + s - 2], fill=(210, 170, 60),
                  outline=(150, 110, 20), width=2)
        d.text((x + s / 2 - 4, y + s / 2 - 9), "$",
               font=font("DejaVuSans-Bold.ttf", 15), fill=WHITE)
    elif kind == "candle":
        d.rectangle([x + s / 2 - 3, y + 8, x + s / 2 + 3, y + s - 4], fill=WHITE,
                    outline=c)
        d.ellipse([x + s / 2 - 3, y + 1, x + s / 2 + 3, y + 8], fill=(255, 180, 40))
        d.rectangle([x + 2, y + s - 4, x + s - 2, y + s - 1], fill=c)
    elif kind == "gavel":
        d.rectangle([x + 4, y + 6, x + s - 4, y + 12], fill=c)
        d.rectangle([x + s / 2 - 2, y + 12, x + s / 2 + 2, y + s - 4], fill=c)
        d.rectangle([x + 4, y + s - 6, x + s - 4, y + s - 2], fill=c)
    elif kind == "court":
        for i in range(3):
            cx = x + 5 + i * 9
            d.rectangle([cx, y + 8, cx + 4, y + s - 6], fill=c)
        d.polygon([(x + 2, y + 8), (x + s / 2, y + 1), (x + s - 2, y + 8)],
                  fill=RED)
        d.rectangle([x + 2, y + s - 5, x + s - 2, y + s - 2], fill=c)
    elif kind == "factory":
        d.rectangle([x + 3, y + 12, x + s - 3, y + s - 3], fill=c)
        d.rectangle([x + 5, y + 4, x + 9, y + 13], fill=c)
        d.rectangle([x + 12, y + 7, x + 16, y + 13], fill=c)
        d.polygon([(x + 6, y + 15), (x + 12, y + 21), (x + 18, y + 15)],
                  fill=(255, 200, 0))
    elif kind == "flag":
        d.rectangle([x + 6, y + 3, x + 8, y + s - 3], fill=c)
        d.polygon([(x + 8, y + 3), (x + s - 3, y + 7), (x + 8, y + 11)],
                  fill=RED)
    elif kind == "gold":
        d.polygon([(x + 4, y + s - 8), (x + 10, y + s - 14),
                   (x + s - 10, y + s - 14), (x + s - 4, y + s - 8)],
                  fill=(210, 170, 60))
        d.polygon([(x + 8, y + s - 16), (x + 13, y + s - 21),
                   (x + s - 13, y + s - 21), (x + s - 8, y + s - 16)],
                  fill=(230, 190, 80))
    else:  # drop
        d.polygon([(x + s / 2, y + 2), (x + s - 4, y + s - 8),
                   (x + 4, y + s - 8)], fill=(40, 90, 140))
        d.ellipse([x + 4, y + s - 10, x + s - 4, y + s - 2], fill=(40, 90, 140))


def draw_medium(d, mx, my, mw, mh, m):
    d.rectangle([mx, my, mx + mw, my + mh], fill=CARD, outline=(180, 170, 140))
    draw_icon(d, mx + 8, my + 7, 24, m["icon"])
    d.text((mx + 38, my + 8), m["kicker"], font=F_MEDKICK, fill=NAVY)
    n = str(m["num"])
    d.ellipse([mx + mw - 26, my + 6, mx + mw - 6, my + 26], fill=RED)
    nw = F_PIN.getlength(n)
    d.text((mx + mw - 16 - nw / 2, my + 9), n, font=F_PIN, fill=WHITE)
    hy = my + 34
    lines = wrap(F_MEDHEAD, m["head"], mw - 16)
    check("medium head " + n, lines, 2, F_MEDHEAD, mw - 16)
    hy = draw_lines(d, lines[:2], mx + 8, hy, F_MEDHEAD, INK, 14)
    dlines = wrap(F_MEDDECK, m["deck"], mw - 16)
    check("medium deck " + n, dlines, 2, F_MEDDECK, mw - 16)
    draw_lines(d, dlines[:2], mx + 8, hy + 2, F_MEDDECK, INK, 12)


MAP_GRID = [
    "         #######      ###                                      ",
    "  #####   #########   ###             ###################      ",
    "  ####    ###########  ###           ######################### ",
    "      ###########     # ###          #######################  ",
    "     ###########      #######        ######################   ",
    "    ###########        ########       ####################    ",
    "    ##########          #######        #################  #   ",
    "    ##########          #######         ###########     ##    ",
    "    #########           #######  ####   #########             ",
    "    ######              ########  ####   ######               ",
    "     ####               ########   ###    ####                ",
    "      ###               #######    ###    ####                ",
    "       ###              #######        ####                   ",
    "            ####        ######         ###                    ",
    "            #####       #####          ######                 ",
    "            #####       #####           #######               ",
    "            #####       ####             ######               ",
    "             ####       ####              #####               ",
    "             ####       ####             ######               ",
    "             ###        ###            #######                ",
    "             ###        ###            #######                ",
    "             ###        ###             #####                 ",
    "             ##         ##              ####                  ",
    "             ##                                  ##          ",
    "             #                                   #           ",
    "             #                                               ",
]

PINS = [
    (1, 100.3, 41.0, None), (2, -93.5, 42.0, None),
    (3, -77.0, 38.9, None), (4, -63.0, 30.0, (298, 643)),
    (5, 151.2, -33.9, None), (6, 37.6, 55.8, None),
    (7, -118.2, 34.1, None), (8, 158.0, -28.0, (932, 723)),
    (9, 13.4, 52.5, None), (10, -0.1, 51.5, None),
    (11, -78.5, -0.2, None), (12, -66.0, 45.0, (306, 641)),
    (13, 46.7, 24.7, None),
]


def draw_map(d, y0, h):
    d.text((12, y0 + 2), "WHERE IT HAPPENED", font=F_MAPT, fill=INK)
    leg = "pins = story numbers"
    d.text((W - 12 - F_MAPL.getlength(leg), y0 + 6), leg, font=F_MAPL,
           fill=GREY)
    gy, gh = y0 + 24, h - 24
    d.rectangle([12, gy, W - 12, gy + gh], fill=SEA)
    rows, cols = len(MAP_GRID), 60
    cw, chh = 1000.0 / cols, gh / rows
    for r, row in enumerate(MAP_GRID):
        for cix, cell in enumerate(row.ljust(cols)):
            if cell == "#":
                x0 = 12 + cix * cw
                y0c = gy + r * chh
                d.rectangle([x0 + 0.6, y0c + 0.6, x0 + cw - 0.6,
                             y0c + chh - 0.6], fill=LAND)
                cx = 12 + (cix + 0.5) * cw
                cy = gy + (r + 0.5) * chh
                d.ellipse([cx - 1.3, cy - 1.3, cx + 1.3, cy + 1.3],
                          fill=(96, 82, 52))
    for num, lon, lat, leader_from in PINS:
        if leader_from:
            px = 12 + (lon + 180.0) / 360.0 * 1000.0
            py = gy + (78.0 - lat) / 131.0 * gh
            d.line([leader_from, (px, py)], fill=RED, width=1)
            d.ellipse([leader_from[0] - 2, leader_from[1] - 2,
                       leader_from[0] + 2, leader_from[1] + 2], fill=RED)
    for num, lon, lat, leader_from in PINS:
        px = 12 + (lon + 180.0) / 360.0 * 1000.0
        py = gy + (78.0 - lat) / 131.0 * gh
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
                  outline=WHITE, width=1)
        ns = str(num)
        nw = F_PIN.getlength(ns)
        d.text((px - nw / 2, py - 7), ns, font=F_PIN, fill=WHITE)


def draw_also(d, y0, h):
    d.text((12, y0 + 2), "ALSO ON WEDNESDAY 25 NOV — 36 MORE STORIES",
           font=F_ALSOH, fill=INK)
    d.line([(12, y0 + 20), (W - 12, y0 + 20)], fill=INK, width=1)
    col_w = (W - 24 - 2 * 12) / 3
    top = y0 + 28
    lh = 14
    for i, (num, place, head) in enumerate(ALSO):
        col = i // 12
        row = i % 12
        x = 12 + col * (col_w + 12)
        y = top + row * lh
        ns = "#" + str(num)
        d.text((x, y), ns, font=F_ALSON, fill=RED)
        rest = place + " — " + head
        if F_ALSO.getlength(rest) > col_w - F_ALSON.getlength(ns) - 6:
            OVERFLOW.append("also #%d too wide: %s" % (num, rest))
        d.text((x + F_ALSON.getlength(ns) + 5, y), rest, font=F_ALSO, fill=INK)


def draw_datecheck(d, y0, h):
    d.rectangle([12, y0, W - 12, y0 + h], fill=(176, 30, 30))
    parts = ["DATE CHECK — Left out as other days' news:"]
    parts.extend(DATECHECK)
    text = " • ".join(parts)
    tw = F_DC.getlength(text)
    if tw > W - 24:
        OVERFLOW.append("datecheck too wide: %d" % tw)
    d.text(((W - tw) / 2, y0 + (h - 13) / 2), text, font=F_DC, fill=WHITE)


def draw_footer(d, y0, h):
    line1 = ("Every story here happened or was first reported on Wednesday 25 "
             "November 2026. Disputed claims are attributed to the outlet "
             "that reported them.")
    d.text((12, y0 + 4), line1, font=F_FOOT, fill=INK)
    left = "Sources: AP • Reuters • AFP • BBC • BEA • NYT • Destatis • ABS • Xinhua"
    d.text((12, y0 + 22), left, font=F_FOOT, fill=INK)
    right = "THE DAILY GLOBE • WEDNESDAY 25 NOVEMBER 2026 • 49 STORIES"
    d.text((W - 12 - F_FOOT.getlength(right), y0 + 22), right, font=F_FOOT,
           fill=INK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_top_strip(d)
    draw_masthead(d)
    draw_stats(d, 114, 78)
    hw = (W - 24 - 2 * 8) / 3
    for i, hero in enumerate(HEROES):
        draw_hero(d, 12 + i * (hw + 8), 192, hw, 206, hero)
    mw = (W - 24 - 4 * 6) / 5
    for i, m in enumerate(MEDIUM):
        r, c = divmod(i, 5)
        draw_medium(d, 12 + c * (mw + 6), 398 + r * 93, mw, 87, m)
    draw_map(d, 578, 170)
    draw_also(d, 748, 196)
    draw_datecheck(d, 944, 36)
    draw_footer(d, 980, 44)
    img.save("entry.png", "PNG")
    if OVERFLOW:
        print("OVERFLOW:")
        for o in OVERFLOW:
            print(" - " + o)
    else:
        print("OVERFLOW: none")


if __name__ == "__main__":
    main()
