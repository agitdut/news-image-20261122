#!/usr/bin/env python3
"""Sunday, 22 November 2026 -- The Day in One Picture.

Draws a one-page newspaper front page (1024 x 1024 PNG) summing up the
world news of Sunday 22 November 2026: one lead story, three featured
stories, eighteen briefs from around the world, and a numbers strip.

Everything on the page comes from fixed strings and fixed geometry:
no clock, no randomness, no network, so two runs write byte-identical
files. Usage: python3 draw_news.py [output-dir]
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024
PAPER = (247, 242, 231)
INK = (28, 26, 23)
FADED = (105, 99, 88)
RULE = (198, 189, 170)
RED = (163, 31, 31)
WASH = (236, 228, 208)
LINE = (214, 205, 186)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


F_TITLE = font(SERIF, 46)
F_DATE = font(SANSB, 15)
F_KICK = font(SANSB, 13)
F_LEAD = font(SERIF, 38)
F_DECK = font(SANS, 16)
F_FEAT = font(SERIF, 18)
F_FDECK = font(SANS, 13)
F_BRIEF_HEAD = font(SANSB, 12)
F_BRIEF = font(SANS, 12)
F_SECT = font(SANSB, 14)
F_NUM = font(SERIF, 26)
F_NUMLAB = font(SANS, 11)
F_FOOT = font(SANS, 11)

MX = 30  # side margin
RX = W - MX


def wrap(draw, text, fnt, width, max_lines):
    """Greedy word wrap; returns at most max_lines lines."""
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
            if len(lines) == max_lines:
                return lines
    if cur and len(lines) < max_lines:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, gap=4):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + gap
    return y


def rule(draw, x0, y, x1, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


LEAD = {
    "kicker": "CYBERSECURITY  •  WASHINGTON",
    "headline": "FBI's criminal database hacked",
    "deck": (
        "The bureau investigates an apparent breach of its National Crime "
        "Information Center — the system holding fingerprints, wanted "
        "persons and missing-persons records. President Trump confirms "
        "the intrusion."
    ),
}

FEATURED = [
    {
        "kicker": "DIPLOMACY  •  SHENZHEN",
        "headline": "Trump, Xi and Putin issue joint peace declaration",
        "deck": (
            "The three leaders meet in China and promise a path to peace, "
            "but critics ask what was actually achieved — and Zelensky "
            "calls the summit “very unsuccessful” for Russia."
        ),
    },
    {
        "kicker": "CLIMATE  •  ANTALYA",
        "headline": "COP31 stalls in overtime over fossil fuels",
        "deck": (
            "Delegates scramble for a final text as talks run into a "
            "second day of overtime; a new draft deal aims to avert a "
            "collapse of the summit."
        ),
    },
    {
        "kicker": "SPORT  •  LAS VEGAS",
        "headline": "Verstappen wins a wild Las Vegas Grand Prix",
        "deck": (
            "Red Bull's Max Verstappen takes an extraordinary race of 34 "
            "lead changes, as the two Ferraris collide again."
        ),
    },
]

BRIEFS = [
    ("SINALOA", "“El Chapo Isidro” arrested in a shoot-out; 11 die in the raid, and the cartel boss's capture sparks deadly violence across the region."),
    ("BALTIC", "Drones strike a Russia-bound cargo ship in the Gulf of Finland; the vessel catches fire as regional tensions rise."),
    ("UKRAINE", "Russia hits Kryvyi Rih, Zelensky's home town; the president calls strikes on the Crimean Bridge a “fair response”."),
    ("SEOUL", "South Korea's education minister resigns over an exam-cheating scandal, after measures against AI-assisted cheating cause chaos."),
    ("ROME", "Paolo Bulgari, the Italian jeweller and businessman, dies aged 89, his family says."),
    ("INDONESIA", "Three killed and 36 missing after a fire at a confectionery factory."),
    ("NIGERIA", "At least 24 dead as a boat carrying mourners to a funeral overturns."),
    ("TECH", "Amazon nears a $7.5bn deal for Israeli AI startup Decart to boost its Trainium chips."),
    ("TECH", "IBM unveils “Nighthawk r3”, a 520-qubit quantum processor aimed at real workloads, not breaking RSA."),
    ("CALIFORNIA", "Miley Cyrus marries Maxx Morando in a California ceremony."),
    ("RIGHTS", "One in four women worldwide cannot refuse sex within marriage, the UN reports."),
    ("COPENHAGEN", "Denmark accuses Russia of plotting to assassinate a US-Ukrainian rapper."),
    ("LOS ANGELES", "A man is convicted of starting the Palisades fire."),
    ("CALIFORNIA", "Coastal communities on alert as the biggest waves in years hit the state."),
    ("YEMEN", "Houthis launch strikes on Saudi Arabia after a coalition “special operation” in Hodeida."),
    ("GULF", "Iran hits an industrial site in Bahrain; its foreign minister says reopening Hormuz is “not difficult” if the US accepts its conditions."),
    ("CRICKET", "India declares on 720 for 9 against New Zealand and takes a 352-run lead in Wellington."),
    ("NEW DELHI", "Nepal's PM Balendra Shah begins a two-day India visit as India and China hold fresh border talks."),
]

NUMBERS = [
    ("34", "lead changes in Las Vegas"),
    ("11", "killed in the Sinaloa raid"),
    ("24", "dead in the Nigeria boat disaster"),
    ("36", "missing in the Indonesia factory fire"),
    ("$7.5bn", "Amazon's Decart deal"),
    ("520", "qubits in IBM's Nighthawk r3"),
]


def draw_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead.
    y = 26
    title = "THE DAY IN ONE PICTURE"
    d.text(((W - d.textlength(title, font=F_TITLE)) / 2, y), title, font=F_TITLE, fill=INK)
    y += 58
    date = "SUNDAY, 22 NOVEMBER 2026  •  THE WORLD'S NEWS IN ONE IMAGE"
    d.text(((W - d.textlength(date, font=F_DATE)) / 2, y), date, font=F_DATE, fill=RED)
    y += 30
    rule(d, MX, y, RX, 3, INK)
    y += 8
    rule(d, MX, y, RX, 1)
    y += 16

    # Lead story in a tinted box.
    box_top = y
    d.rectangle([MX, box_top, RX, box_top + 160], fill=WASH, outline=RULE, width=1)
    lx = MX + 18
    ly = box_top + 12
    d.text((lx, ly), LEAD["kicker"], font=F_KICK, fill=RED)
    ly += 24
    ly = text_block(d, lx, ly, wrap(d, LEAD["headline"], F_LEAD, RX - MX - 36, 1), F_LEAD, gap=2)
    ly += 6
    text_block(d, lx, ly, wrap(d, LEAD["deck"], F_DECK, RX - MX - 36, 3), F_DECK, gap=2)
    y = box_top + 160 + 14

    # Three featured stories in a row.
    col_w = (RX - MX - 2 * 14) // 3
    for i, f in enumerate(FEATURED):
        x = MX + i * (col_w + 14)
        yy = y
        d.text((x, yy), f["kicker"], font=F_KICK, fill=RED)
        yy += 22
        yy = text_block(d, x, yy, wrap(d, f["headline"], F_FEAT, col_w, 3), F_FEAT, gap=1)
        yy += 2
        text_block(d, x, yy, wrap(d, f["deck"], F_FDECK, col_w, 4), F_FDECK, gap=1)
        if i < 2:
            d.line([(x + col_w + 7, y), (x + col_w + 7, y + 142)], fill=LINE, width=1)
    y += 158
    rule(d, MX, y, RX, 1)
    y += 12

    # Section header.
    d.text((MX, y), "MORE FROM AROUND THE WORLD", font=F_SECT, fill=INK)
    y += 26

    # Eighteen briefs: three columns, six rows.
    bcol_w = (RX - MX - 2 * 14) // 3
    row_h = 58
    for i, (place, body) in enumerate(BRIEFS):
        col = i % 3
        row = i // 3
        x = MX + col * (bcol_w + 14)
        yy = y + row * row_h
        head = place + " — "
        head_w = d.textlength(head, font=F_BRIEF_HEAD)
        d.text((x, yy), head, font=F_BRIEF_HEAD, fill=RED)
        first = wrap(d, body, F_BRIEF, bcol_w - head_w, 1)
        text_block(d, x + head_w, yy, first, F_BRIEF, gap=1)
        rest = body[len(first[0]):].strip() if first else body
        if rest:
            text_block(d, x, yy + 16, wrap(d, rest, F_BRIEF, bcol_w, 2), F_BRIEF, gap=1)
    y += 6 * row_h + 4
    rule(d, MX, y, RX, 1)
    y += 12

    # The day in numbers.
    d.text((MX, y), "THE DAY IN NUMBERS", font=F_SECT, fill=INK)
    y += 26
    ncol_w = (RX - MX) // 6
    for i, (num, lab) in enumerate(NUMBERS):
        x = MX + i * ncol_w
        d.text((x, y), num, font=F_NUM, fill=RED)
        lab_lines = wrap(d, lab, F_NUMLAB, ncol_w - 8, 2)
        yy = y + 34
        for ln in lab_lines:
            d.text((x, yy), ln, font=F_NUMLAB, fill=FADED)
            yy += 14
    y += 78
    rule(d, MX, y, RX, 3, INK)
    y += 10

    # Footer.
    foot = "Drawn from reporting published on Sunday 22 November 2026 — BBC, The Guardian, CNBC, Al Jazeera, France 24, Sky Sports."
    d.text((MX, y), foot, font=F_FOOT, fill=FADED)
    return img


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out_dir, exist_ok=True)
    img = draw_page()
    path = os.path.join(out_dir, "entry.png")
    img.save(path, "PNG")
    print(f"wrote {path} ({os.path.getsize(path)} bytes, {img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
