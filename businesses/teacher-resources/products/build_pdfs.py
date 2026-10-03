"""Generates original Grade 3 fractions printables (all art is vector, drawn in code; no third-party clipart/fonts).
Run: python3 build_pdfs.py   -> writes PDFs next to this script."""
import random, os
from fractions import Fraction
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import simpleSplit
from reportlab.lib.colors import HexColor, black, white

W, H = letter
M = 48
OUT = os.path.dirname(os.path.abspath(__file__))
INK = HexColor("#222222"); ACC = HexColor("#2F6F8F"); SHADE = HexColor("#BBD6E4"); GREY = HexColor("#888888")
BRAND = "Fraction Fluency | Grade 3"
DENS = [2, 3, 4, 6, 8]

def wrap(c, text, x, y, width, font="Helvetica", size=11, lead=None):
    lead = lead or size + 3
    c.setFont(font, size)
    for ln in simpleSplit(text, font, size, width):
        c.drawString(x, y, ln); y -= lead
    return y

def header(c, title, std, key=False, plain=False):
    c.setFillColor(ACC); c.rect(0, H - 62, W, 62, stroke=0, fill=1)
    c.setFillColor(white); c.setFont("Helvetica-Bold", 20)
    c.drawString(M, H - 38, title + ("  - ANSWER KEY" if key and not plain else ""))
    c.setFont("Helvetica", 9); c.drawString(M, H - 54, std)
    c.setFillColor(INK)
    if not key and not plain:
        c.setFont("Helvetica", 11); c.drawString(M, H - 84, "Name: ______________________________"); c.drawRightString(W - M, H - 84, "Date: ______________")
    c.setFont("Helvetica", 8); c.setFillColor(GREY)
    c.drawCentredString(W / 2, 24, BRAND + "  |  Original work. Single-classroom license.  |  page %d" % c.getPageNumber())
    c.setFillColor(INK)

def bar(c, x, y, w, h, n, k, show=True):
    """fraction bar with n equal parts, first k shaded"""
    c.setLineWidth(1.2); c.setStrokeColor(INK)
    pw = w / n
    for i in range(n):
        c.setFillColor(SHADE if (i < k and show) else white)
        c.rect(x + i * pw, y, pw, h, stroke=1, fill=1)
    c.setFillColor(INK)

def numline(c, x, y, w, n, point=None, label_ends=True):
    c.setLineWidth(1.5); c.setStrokeColor(INK); c.line(x, y, x + w, y)
    for i in range(n + 1):
        tx = x + w * i / n; c.line(tx, y - 6 if i in (0, n) else y - 4, tx, y + (6 if i in (0, n) else 4))
    c.setFont("Helvetica-Bold", 11)
    if label_ends: c.drawCentredString(x, y - 20, "0"); c.drawCentredString(x + w, y - 20, "1")
    if point is not None:
        px = x + w * point / n; c.setFillColor(HexColor("#C0392B")); c.circle(px, y, 5, stroke=0, fill=1); c.setFillColor(INK)

def frac_text(c, x, y, a, b, size=14):
    """stacked fraction centered at x; y is baseline of the line"""
    c.setFont("Helvetica-Bold", size)
    c.drawCentredString(x, y + 4, str(a)); c.drawCentredString(x, y - size + 1, str(b))
    tw = max(c.stringWidth(str(a), "Helvetica-Bold", size), c.stringWidth(str(b), "Helvetica-Bold", size)) + 6
    c.setLineWidth(1); c.line(x - tw / 2, y + 1, x + tw / 2, y + 1)

def blank_frac(c, x, y, size=14):
    c.setLineWidth(1); c.line(x - 14, y + 1, x + 14, y + 1)
    c.rect(x - 11, y + 5, 22, 18, stroke=1, fill=0); c.rect(x - 11, y - 22, 22, 18, stroke=1, fill=0)

# ---------------- content generators (seeded, answers computed) ----------------
def gen_name(rng, n=6):
    out = []; seen = set()
    while len(out) < n:
        d = rng.choice(DENS); k = rng.randint(1, d)
        if (d, k) not in seen: seen.add((d, k)); out.append((d, k))
    return out

def gen_shade(rng, n=6):
    return gen_name(rng, n)

def gen_numline(rng, n=5):
    out = []; seen = set()
    while len(out) < n:
        d = rng.choice(DENS); k = rng.randint(1, d - 1)
        if (d, k) not in seen: seen.add((d, k)); out.append((d, k))
    return out

EQ = [((1, 2), (2, 4)), ((1, 2), (3, 6)), ((1, 2), (4, 8)), ((1, 3), (2, 6)), ((2, 3), (4, 6)), ((1, 4), (2, 8)), ((3, 4), (6, 8)), ((2, 4), (4, 8)), ((2, 6), (1, 3)), ((4, 8), (1, 2)), ((6, 8), (3, 4)), ((3, 6), (2, 4))]
def gen_eq(rng, n=8):
    return rng.sample(EQ, n)   # (a/b) = ?/d ; missing numerator = second numerator

def gen_compare(rng, n=8):
    out = []
    while len(out) < n:
        if rng.random() < .5:
            d = rng.choice(DENS); a, b = rng.randint(1, d), rng.randint(1, d)
            if a == b: continue
            p = ((a, d), (b, d))
        else:
            nu = rng.randint(1, 4); d1, d2 = rng.sample(DENS, 2)
            if nu > min(d1, d2): continue
            p = ((nu, d1), (nu, d2))
        if p not in out: out.append(p)
    return out
def cmp_sym(p):
    a, b = Fraction(*p[0]), Fraction(*p[1]); return ">" if a > b else "<" if a < b else "="

WORDS = [
 ("A pizza is cut into {d} equal slices. Mia eats {k} slices. What fraction of the pizza did Mia eat?", lambda d, k: (k, d)),
 ("A ribbon is cut into {d} equal pieces. Omar uses {k} pieces for a gift. What fraction of the ribbon did Omar use?", lambda d, k: (k, d)),
 ("A garden has {d} equal sections. Planted with tomatoes: {k} sections. What fraction of the garden has tomatoes?", lambda d, k: (k, d)),
 ("A chocolate bar has {d} equal pieces. Lena has {k} pieces left. What fraction of the bar is left?", lambda d, k: (k, d)),
 ("A fence has {d} equal panels. Painters finish {k} panels. What fraction of the fence is painted?", lambda d, k: (k, d)),
 ("A paper strip is folded into {d} equal parts. Jin colors {k} parts green. What fraction is green?", lambda d, k: (k, d)),
]
def gen_words(rng, n=5):
    items = rng.sample(WORDS, n); out = []
    for t, f in items:
        d = rng.choice(DENS[1:]); k = rng.randint(2, d - 1); out.append((t.format(d=d, k=k), f(d, k)))
    return out

# ---------------- worksheet pack ----------------
def ws_name(c, key):
    rng = random.Random(101); items = gen_name(rng)
    header(c, "Name the Fraction", "CCSS 3.NF.A.1  |  TEKS 3.3A (verify current TEKS numbering)", key)
    y = H - 130
    if not key: wrap(c, "Directions: Each bar is split into equal parts. Write the fraction that is shaded.", M, y + 14, W - 2 * M)
    for i, (d, k) in enumerate(items):
        yy = y - 40 - i * 95
        c.setFont("Helvetica-Bold", 13); c.drawString(M, yy + 8, "%d." % (i + 1))
        bar(c, M + 30, yy, 260, 36, d, k)
        c.setFont("Helvetica", 11); c.drawString(M + 320, yy + 10, "Fraction shaded:")
        if key: frac_text(c, M + 440, yy + 20, k, d, 16)
        else: blank_frac(c, M + 440, yy + 12)
def ws_shade(c, key):
    rng = random.Random(102); items = gen_shade(rng)
    header(c, "Shade the Fraction", "CCSS 3.NF.A.1  |  TEKS 3.3A", key)
    y = H - 130
    if not key: wrap(c, "Directions: Shade the bar to show the fraction.", M, y + 14, W - 2 * M)
    for i, (d, k) in enumerate(items):
        yy = y - 40 - i * 95
        c.setFont("Helvetica-Bold", 13); c.drawString(M, yy + 8, "%d." % (i + 1))
        frac_text(c, M + 50, yy + 22, k, d, 16)
        bar(c, M + 100, yy, 260, 36, d, k, show=key)
def ws_numline(c, key):
    rng = random.Random(103); items = gen_numline(rng)
    header(c, "Fractions on a Number Line", "CCSS 3.NF.A.2  |  TEKS 3.3B", key)
    y = H - 130
    if not key: wrap(c, "Directions: The distance from 0 to 1 is split into equal parts. Write the fraction named by the red dot.", M, y + 14, W - 2 * M)
    for i, (d, k) in enumerate(items):
        yy = y - 60 - i * 115
        c.setFont("Helvetica-Bold", 13); c.drawString(M, yy + 8, "%d." % (i + 1))
        numline(c, M + 40, yy, 300, d, k)
        c.setFont("Helvetica", 11); c.drawString(M + 370, yy + 6, "Dot is at:")
        if key: frac_text(c, M + 450, yy + 14, k, d, 16)
        else: blank_frac(c, M + 450, yy + 8)
def ws_eq(c, key):
    rng = random.Random(104); items = gen_eq(rng)
    header(c, "Equivalent Fractions", "CCSS 3.NF.A.3b  |  TEKS 3.3F", key)
    y = H - 130
    if not key: wrap(c, "Directions: Use the bars to help. Write the missing numerator so the fractions are equal.", M, y + 14, W - 2 * M)
    for i, ((a, b), (a2, b2)) in enumerate(items):
        yy = y - 44 - i * 72
        c.setFont("Helvetica-Bold", 13); c.drawString(M, yy + 8, "%d." % (i + 1))
        frac_text(c, M + 45, yy + 20, a, b, 15); c.setFont("Helvetica-Bold", 16); c.drawString(M + 65, yy + 8, "=")
        if key: frac_text(c, M + 100, yy + 20, a2, b2, 15)
        else:
            c.setLineWidth(1); c.line(M + 88, yy + 20, M + 112, yy + 20)
            c.rect(M + 90, yy + 24, 22, 17, stroke=1, fill=0); c.setFont("Helvetica-Bold", 15); c.drawCentredString(M + 100, yy + 4, str(b2))
        bar(c, M + 160, yy + 22, 150, 20, b, a); bar(c, M + 160, yy - 2, 150, 20, b2, a2 if key else 0)
def ws_compare(c, key):
    rng = random.Random(105); items = gen_compare(rng)
    header(c, "Compare the Fractions", "CCSS 3.NF.A.3d  |  TEKS 3.3H", key)
    y = H - 130
    if not key: wrap(c, "Directions: Write <, >, or = in each circle. Draw bars or a number line if you need help.", M, y + 14, W - 2 * M)
    for i, (p, q) in enumerate(items):
        yy = y - 44 - i * 72
        c.setFont("Helvetica-Bold", 13); c.drawString(M, yy + 8, "%d." % (i + 1))
        frac_text(c, M + 80, yy + 20, *p, 16); c.setLineWidth(1.2); c.circle(M + 150, yy + 12, 15, stroke=1, fill=0)
        if key: c.setFont("Helvetica-Bold", 18); c.drawCentredString(M + 150, yy + 6, cmp_sym((p, q)))
        frac_text(c, M + 220, yy + 20, *q, 16)
def ws_words(c, key):
    rng = random.Random(106); items = gen_words(rng)
    header(c, "Fraction Word Problems", "CCSS 3.NF.A.1  |  TEKS 3.3A", key)
    y = H - 130
    for i, (t, (a, b)) in enumerate(items):
        yy = y - i * 118
        c.setFont("Helvetica-Bold", 12); c.drawString(M, yy, "%d." % (i + 1))
        wrap(c, t, M + 22, yy, W - 2 * M - 30, size=12, lead=16)
        c.setFont("Helvetica", 11); c.drawString(M + 22, yy - 62, "Answer:")
        if key: frac_text(c, M + 90, yy - 54, a, b, 15)
        else:
            c.rect(M + 80, yy - 72, 60, 40, stroke=1, fill=0)
            c.setFont("Helvetica", 9); c.drawString(M + 160, yy - 62, "Draw a picture to show your thinking:"); c.rect(M + 160, yy - 100, 250, 30, stroke=1, fill=0)

def cover(c, title, subtitle, bullets):
    c.setFillColor(ACC); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(white); c.setFont("Helvetica-Bold", 38)
    yy = H - 200
    for ln in simpleSplit(title, "Helvetica-Bold", 38, W - 2 * M - 40): c.drawString(M + 20, yy, ln); yy -= 46
    c.setFont("Helvetica", 16); yy -= 10
    for ln in simpleSplit(subtitle, "Helvetica", 16, W - 2 * M - 40): c.drawString(M + 20, yy, ln); yy -= 22
    yy -= 20
    for b in bullets:
        c.setFont("Helvetica-Bold", 14); c.drawString(M + 20, yy, "+  " + b); yy -= 26
    for i, (d, k) in enumerate([(2, 1), (4, 3), (6, 4), (8, 5)]):
        bar(c, M + 20, 120 + i * 34, 300, 26, d, k)
    c.setFillColor(white); c.setFont("Helvetica", 11); c.drawString(M + 20, 70, "Print & go  |  Black-and-white friendly  |  Answer key included")
    c.showPage()

def terms(c):
    header(c, "Terms of Use & Thank You", BRAND, True, plain=True)
    y = H - 120
    for t in ["Thank you for your purchase! This resource is licensed for ONE teacher's classroom use (print copies for your own students).",
              "Please do not share, resell, or post this file online (including class websites or shared drives open to the public). Colleagues can buy their own license at a discount through the shop.",
              "All artwork in this file is original vector drawing made for this product. No third-party clipart or fonts are embedded (standard PDF fonts only).",
              "Standards note: items are aligned to Common Core State Standards (CCSS.MATH.CONTENT.3.NF) and tagged with the Texas TEKS Grade 3 fraction numbering in use when this was written. TEKS were revised and renumbered by the Texas State Board of Education, so verify numbering against your district's current scope and sequence.",
              "Not affiliated with or endorsed by any state or the owners of the CCSS or TEKS."]:
        y = wrap(c, t, M, y, W - 2 * M, size=12, lead=17) - 12
    c.showPage()

def page(c, fn):
    fn(c, False); c.showPage()
def keypage(c, fn):
    fn(c, True); c.showPage()

WS = [ws_name, ws_shade, ws_numline, ws_eq, ws_compare, ws_words]
def build_worksheets(c, with_cover=True):
    if with_cover: cover(c, "Fractions Worksheet Pack", "Grade 3 | Unit fractions, number lines, equivalence, comparing | CCSS + TEKS tagged", ["6 print-and-go worksheets", "Full answer key", "No prep, ink-friendly"])
    for f in WS: page(c, f)
    for f in WS: keypage(c, f)

# ---------------- task cards ----------------
def make_cards():
    rng = random.Random(201); cards = []
    for d, k in gen_name(rng, 6): cards.append(("bar", d, k, (k, d), "Write the fraction that is shaded."))
    for d, k in gen_numline(rng, 6): cards.append(("nl", d, k, (k, d), "Write the fraction shown by the dot."))
    for (a, b), (a2, b2) in rng.sample(EQ, 4): cards.append(("eq", (a, b), (a2, b2), a2, "Find the missing numerator:  %d/%d = ?/%d" % (a, b, b2)))
    for p, q in gen_compare(rng, 6): cards.append(("cmp", p, q, cmp_sym((p, q)), "Write <, > or = :   %d/%d  ?  %d/%d" % (p[0], p[1], q[0], q[1])))
    for n, d in [(3, 1), (2, 2), (4, 4), (6, 3)][:2]:
        pass
    cards.append(("txt", None, None, "1", "Write 4/4 as a whole number."))
    cards.append(("txt", None, None, "3/1", "Write the whole number 3 as a fraction with denominator 1."))
    return cards[:24]
ANS_TXT = lambda a: ("%d/%d" % a) if isinstance(a, tuple) else str(a)

def build_cards(c, with_cover=True):
    cards = make_cards()
    if with_cover: cover(c, "Fraction Task Cards", "24 cards | Grade 3 | CCSS 3.NF.A.1-3 + TEKS 3.3 tags | recording sheet + key", ["24 cut-and-go cards", "Student recording sheet", "Answer key"])
    cw, ch = (W - 2 * M) / 2, 158
    for pg in range(3):
        header(c, "Fraction Task Cards  (set %d of 3)" % (pg + 1), "Cut on the dotted lines. Students record answers on the recording sheet.", True, plain=True)
        c.setDash(3, 3)
        for i in range(8):
            idx = pg * 8 + i; col, row = i % 2, i // 2
            x = M + col * cw; y = H - 76 - (row + 1) * ch
            c.setStrokeColor(GREY); c.rect(x, y, cw, ch, stroke=1, fill=0)
        c.setDash()
        for i in range(8):
            idx = pg * 8 + i; kind, a, b, ans, prompt = cards[idx]
            col, row = i % 2, i // 2; x = M + col * cw; y = H - 76 - (row + 1) * ch
            c.setFillColor(ACC); c.circle(x + 20, y + ch - 20, 13, stroke=0, fill=1)
            c.setFillColor(white); c.setFont("Helvetica-Bold", 11); c.drawCentredString(x + 20, y + ch - 24, str(idx + 1)); c.setFillColor(INK)
            if kind == "bar": bar(c, x + 25, y + 70, cw - 50, 34, a, b)
            elif kind == "nl": numline(c, x + 30, y + 85, cw - 60, a, b)
            elif kind == "eq": bar(c, x + 25, y + 95, cw - 50, 16, a[1], a[0]); bar(c, x + 25, y + 72, cw - 50, 16, b[1], 0)
            elif kind == "cmp":
                frac_text(c, x + cw / 2 - 40, y + 85, *a, 16); c.setFont("Helvetica-Bold", 18); c.drawCentredString(x + cw / 2, y + 79, "?"); frac_text(c, x + cw / 2 + 40, y + 85, *b, 16)
            c.setFont("Helvetica", 10)
            yy = y + 48
            for ln in simpleSplit(prompt, "Helvetica", 10, cw - 30): c.drawString(x + 15, yy, ln); yy -= 13
        c.showPage()
    # recording sheet
    header(c, "Task Card Recording Sheet", "CCSS 3.NF.A.1 / A.2 / A.3  |  TEKS 3.3", False)
    for i in range(24):
        col, row = i // 12, i % 12; x = M + col * 260; y = H - 125 - row * 52
        c.setFont("Helvetica-Bold", 12); c.drawString(x, y, "%d." % (i + 1)); c.setLineWidth(.8); c.line(x + 28, y - 2, x + 200, y - 2)
    c.showPage()
    header(c, "Task Card Answer Key", "Cards 1-24", True)
    for i, cd in enumerate(cards):
        col, row = i // 12, i % 12; x = M + col * 260; y = H - 120 - row * 42
        c.setFont("Helvetica-Bold", 13); c.drawString(x, y, "%d.  %s" % (i + 1, ANS_TXT(cd[3])))
    c.showPage()

# ---------------- assessment ----------------
def build_assessment(c, with_cover=False):
    rng = random.Random(301)
    qs = []
    for d, k in gen_name(rng, 3): qs.append(("bar", d, k, "Write the fraction shaded.", (k, d), "3.NF.A.1"))
    for d, k in gen_numline(rng, 2): qs.append(("nl", d, k, "Write the fraction at the dot.", (k, d), "3.NF.A.2"))
    for (a, b), (a2, b2) in rng.sample(EQ, 2): qs.append(("eq", (a, b), (a2, b2), "%d/%d = ?/%d" % (a, b, b2), a2, "3.NF.A.3b"))
    for p, q in gen_compare(rng, 3): qs.append(("cmp", p, q, "Write <, > or =:  %d/%d  ?  %d/%d" % (p[0], p[1], q[0], q[1]), cmp_sym((p, q)), "3.NF.A.3d"))
    def sheet(c, key):
        header(c, "Fractions Check-Up (10 questions)", "CCSS 3.NF.A.1-3  |  15 minutes  |  Exit ticket / quiz", key)
        for i, (kind, a, b, prompt, ans, std) in enumerate(qs):
            col, row = i // 5, i % 5; x = M + col * 265; y = H - 130 - row * 125
            c.setFont("Helvetica-Bold", 12); c.drawString(x, y, "%d." % (i + 1))
            c.setFont("Helvetica", 10)
            for j, ln in enumerate(simpleSplit(prompt, "Helvetica", 10, 220)): c.drawString(x + 20, y - j * 12, ln)
            if kind == "bar": bar(c, x + 20, y - 50, 200, 26, a, b)
            if kind == "nl": numline(c, x + 25, y - 40, 190, a, b)
            if kind == "eq": bar(c, x + 20, y - 40, 200, 14, a[1], a[0]); bar(c, x + 20, y - 58, 200, 14, b[1], 0)
            if key:
                c.setFillColor(HexColor("#C0392B")); c.setFont("Helvetica-Bold", 12); c.drawString(x + 20, y - 85, "Answer: " + ANS_TXT(ans) + "   [" + std + "]"); c.setFillColor(INK)
            else:
                c.setFont("Helvetica", 10); c.drawString(x + 20, y - 85, "Answer: ____________")
    page(c, lambda c, k: sheet(c, False)); keypage(c, lambda c, k: sheet(c, True))

def make(name, fn, **kw):
    path = os.path.join(OUT, name); c = canvas.Canvas(path, pagesize=letter, title=name[:-4], author="Fraction Fluency")
    fn(c, **kw)
    if name.startswith("Bundle") or True: pass
    c.save(); print("wrote", path)

def build_bundle(c):
    cover(c, "Grade 3 Fractions Starter Bundle", "Worksheets + task cards + check-up | CCSS 3.NF + TEKS 3.3 tags | answer keys for everything", ["6 worksheets", "24 task cards + recording sheet", "10-question check-up", "All answer keys"])
    build_worksheets(c, False); build_cards(c, False); build_assessment(c); terms(c)

def build_free_sample(c):
    cover(c, "FREE Sample: Name the Fraction", "Try before you buy | Grade 3 | CCSS 3.NF.A.1", ["1 worksheet + answer key"])
    page(c, ws_name); keypage(c, ws_name)

if __name__ == "__main__":
    make("01_Fractions_Worksheet_Pack.pdf", lambda c: (build_worksheets(c), terms(c)))
    make("02_Fraction_Task_Cards.pdf", lambda c: (build_cards(c), terms(c)))
    make("03_Fractions_CheckUp_Assessment.pdf", lambda c: (cover(c, "Fractions Check-Up", "10 questions + key | Grade 3 | CCSS 3.NF.A.1-3", ["Quiz / exit ticket", "Answer key with standards"]), build_assessment(c), terms(c)))
    make("04_Grade3_Fractions_Starter_Bundle.pdf", build_bundle)
    make("00_FREE_Sample_Name_the_Fraction.pdf", build_free_sample)
