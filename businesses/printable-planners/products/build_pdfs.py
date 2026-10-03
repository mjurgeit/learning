"""Generates the Shiftwise design-system PDFs (original work, reportlab).
Run: python3 build_pdfs.py  -> writes PDFs into ./pdf/
"""
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdf")
os.makedirs(OUT, exist_ok=True)

# ---------- design system: "Shiftwise" ----------
INK = "#12343B"      # deep teal ink (text, headers)
SAND = "#F7F3EC"     # warm paper background
LINE = "#CFC8BC"     # hairlines
SAGE = "#7FB7A4"     # secondary / fills
MIST = "#E3EFEA"     # light sage fill
CORAL = "#E4572E"    # single accent (active tab, key marks)
GREY = "#6B7B7E"     # secondary text
F, FB = "Helvetica", "Helvetica-Bold"
MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"]
DAYS = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

def col(c, fill=None, stroke=None):
    if fill: c.setFillColor(fill)
    if stroke: c.setStrokeColor(stroke)

def txt(c, x, y, s, size=10, font=F, color=INK, align="l"):
    c.setFont(font, size); c.setFillColor(color)
    {"l": c.drawString, "c": c.drawCentredString, "r": c.drawRightString}[align](x, y, s)

def rrect(c, x, y, w, h, r=6, fill=None, stroke=None, lw=0.8):
    if fill: c.setFillColor(fill)
    if stroke: c.setStrokeColor(stroke)
    c.setLineWidth(lw)
    c.roundRect(x, y, w, h, r, fill=1 if fill else 0, stroke=1 if stroke else 0)

def hline(c, x1, x2, y, color=LINE, lw=0.6):
    c.setStrokeColor(color); c.setLineWidth(lw); c.line(x1, y, x2, y)

def bg(c, W, H):
    c.setFillColor(SAND); c.rect(0, 0, W, H, fill=1, stroke=0)

# =====================================================================
# 1) HYPERLINKED DIGITAL PLANNER (landscape, iPad 11" proportions)
# =====================================================================
W, H = 1194, 834
TABW = 92
TABS = [("Home","home"),("Calendar","cal"),("Weeks","wk"),("Shifts","sh"),("Brain","br"),("Track","tr"),("Notes","nt")]

def dest(c, name, title=None, outline_level=0):
    c.bookmarkPage(name)
    if title: c.addOutlineEntry(title, name, level=outline_level, closed=True)

def link(c, x, y, w, h, name):
    c.linkRect("", name, (x, y, x + w, y + h), relative=0, thickness=0)

def chrome(c, title, subtitle, active, back=None):
    """Page frame: background, header, right-hand hyperlinked tabs."""
    bg(c, W, H)
    c.setFillColor(INK); c.rect(0, H - 74, W - TABW, 74, fill=1, stroke=0)
    txt(c, 36, H - 46, title, 26, FB, SAND)
    txt(c, 36, H - 63, subtitle, 10, F, SAGE)
    txt(c, W - TABW - 28, 12, "SHIFTWISE", 8, FB, GREY, "r")
    # tabs
    th = 62; gap = 8; y0 = H - 100
    for i, (lab, key) in enumerate(TABS):
        y = y0 - i * (th + gap)
        on = key == active
        rrect(c, W - TABW + 6, y - th, TABW - 6, th, 10, fill=CORAL if on else INK)
        txt(c, W - TABW + 6 + (TABW - 6) / 2, y - th / 2 - 3, lab, 11, FB, SAND, "c")
        link(c, W - TABW, y - th, TABW, th, key)
    if back:
        rrect(c, W - TABW - 150, H - 62, 112, 22, 11, stroke=SAGE)
        txt(c, W - TABW - 94, H - 55, "< " + back[0], 9, FB, SAGE, "c")
        link(c, W - TABW - 150, H - 62, 112, 22, back[1])

def page_end(c): c.showPage()

BODY_L, BODY_R, BODY_T, BODY_B = 36, W - TABW - 28, H - 96, 30

def grid(c, x, y_top, w, h, cols, rows, head=None, shade_head=True):
    cw, rh = w / cols, h / rows
    for r in range(rows + 1): hline(c, x, x + w, y_top - r * rh)
    for k in range(cols + 1):
        c.setStrokeColor(LINE); c.setLineWidth(0.6); c.line(x + k * cw, y_top, x + k * cw, y_top - h)
    return cw, rh

def build_digital():
    c = canvas.Canvas(os.path.join(OUT, "Shiftwise_Digital_Shift_Planner_Hyperlinked_iPad.pdf"), pagesize=(W, H))
    c.setTitle("Shiftwise Digital Shift Planner (Hyperlinked, Undated)")
    c.setAuthor("Shiftwise"); c.setSubject("Undated hyperlinked planner for nurses and shift workers")

    # --- cover
    dest(c, "cover", "Cover")
    bg(c, W, H); c.setFillColor(INK); c.rect(0, 0, 430, H, fill=1, stroke=0)
    c.setFillColor(CORAL); c.circle(215, 520, 70, fill=1, stroke=0)
    c.setFillColor(SAND); c.circle(245, 535, 62, fill=1, stroke=0)  # crescent moon motif
    txt(c, 215, 330, "SHIFTWISE", 30, FB, SAND, "c")
    txt(c, 215, 308, "planner for the rotating week", 11, F, SAGE, "c")
    txt(c, 500, 560, "Digital", 56, FB, INK); txt(c, 500, 500, "Shift Planner", 56, FB, INK)
    txt(c, 502, 462, "Undated  |  Hyperlinked  |  GoodNotes, Notability, Noteshelf", 13, F, GREY)
    items = ["12-hour shift brain sheets", "Rotation & shift calendar", "Sleep, energy & recovery trackers", "Overtime, pay & licence trackers"]
    for i, s in enumerate(items):
        c.setFillColor(CORAL); c.circle(512, 400 - i * 30 + 4, 4, fill=1, stroke=0); txt(c, 530, 400 - i * 30, s, 14)
    rrect(c, 500, 220, 190, 44, 22, fill=INK); txt(c, 595, 237, "Tap to open", 14, FB, SAND, "c"); link(c, 500, 220, 190, 44, "home")

    # --- home
    page_end(c); dest(c, "home", "Home")
    chrome(c, "Home", "Tap any tile. Turn OFF writing mode (pencil) to use links.", "home", ("Cover", "cover"))
    tiles = [("Calendar","12 monthly spreads + year view","cal"),("Weeks","26 weekly shift spreads","wk"),
             ("Shifts","31 shift logs (day & night)","sh"),("Brain Sheets","12-hr patient / task sheets","br"),
             ("Trackers","Sleep, energy, pay, licence, swaps","tr"),("Notes","Dot grid + lined pages","nt")]
    tw, th = 300, 190
    for i, (a, b, k) in enumerate(tiles):
        x = BODY_L + (i % 3) * (tw + 24); y = BODY_T - 20 - (i // 3) * (th + 28) - th
        rrect(c, x, y, tw, th, 16, fill="#FFFFFF", stroke=LINE)
        c.setFillColor(MIST if i % 2 == 0 else "#FBE3DA"); c.roundRect(x + 18, y + th - 62, 44, 44, 10, fill=1, stroke=0)
        txt(c, x + 24, y + th - 100, a, 24, FB); txt(c, x + 24, y + th - 124, b, 11, F, GREY)
        txt(c, x + 24, y + 22, "Open >", 11, FB, CORAL); link(c, x, y, tw, th, k)
    txt(c, BODY_L, 52, "Tip: duplicate any page in your app to add more. Shifts, brain sheets and trackers are all undated.", 10, F, GREY)

    # --- calendar section: year overview
    page_end(c); dest(c, "cal", "Calendar")
    chrome(c, "Year at a Glance", "Tap a month to open it.", "cal")
    cw, ch = 250, 170
    for i, m in enumerate(MONTHS):
        x = BODY_L + (i % 4) * (cw + 20); y = BODY_T - 10 - (i // 4) * (ch + 22) - ch
        rrect(c, x, y, cw, ch, 12, fill="#FFFFFF", stroke=LINE)
        txt(c, x + 16, y + ch - 30, m, 17, FB)
        # mini grid
        for r in range(5):
            for k in range(7):
                c.setFillColor(LINE); c.circle(x + 22 + k * 33, y + ch - 62 - r * 20, 2, fill=1, stroke=0)
        link(c, x, y, cw, ch, f"m{i+1}")
    # monthly pages
    for i, m in enumerate(MONTHS):
        page_end(c); dest(c, f"m{i+1}", m, 1)
        chrome(c, m, "Write dates in the first row, mark shifts with D / N / OFF.", "cal", ("Year", "cal"))
        gx, gw = BODY_L, BODY_R - BODY_L; gt = BODY_T - 28; gh = gt - 150
        cwid = gw / 7; rh = gh / 6
        c.setFillColor(MIST); c.rect(gx, gt, gw, 24, fill=1, stroke=0)
        for k, d in enumerate(DAYS): txt(c, gx + k * cwid + cwid / 2, gt + 8, d, 11, FB, INK, "c")
        grid(c, gx, gt, gw, gh, 7, 6)
        for r in range(6):
            for k in range(7):
                rrect(c, gx + k * cwid + cwid - 40, gt - r * rh - 22, 30, 14, 4, stroke=LINE, lw=0.5)
        # weeks links
        txt(c, gx, 118, "Jump to weeks:", 10, FB, GREY)
        for w in range(2):
            wn = i * 2 + w + 1
            rrect(c, gx + 100 + w * 118, 108, 106, 22, 11, fill=INK); txt(c, gx + 153 + w * 118, 115, f"Week {wn}", 9, FB, SAND, "c")
            link(c, gx + 100 + w * 118, 108, 106, 22, f"w{wn}")
        txt(c, gx, 78, "Month focus", 11, FB); hline(c, gx + 78, gx + 480, 78); hline(c, gx, gx + 480, 52)
        txt(c, gx + 540, 78, "Notes", 11, FB); hline(c, gx + 580, BODY_R, 78); hline(c, gx + 540, BODY_R, 52)
    # weekly index
    page_end(c); dest(c, "wk", "Weeks")
    chrome(c, "Weekly Spreads", "26 undated weeks. Tap a number.", "wk")
    for n in range(26):
        x = BODY_L + (n % 7) * 138; y = BODY_T - 20 - (n // 7) * 120 - 92
        rrect(c, x, y, 124, 92, 14, fill="#FFFFFF", stroke=LINE)
        txt(c, x + 62, y + 40, str(n + 1), 30, FB, INK, "c"); txt(c, x + 62, y + 18, "WEEK", 9, FB, GREY, "c")
        link(c, x, y, 124, 92, f"w{n+1}")
    for n in range(26):
        page_end(c); dest(c, f"w{n+1}", f"Week {n+1}", 1)
        chrome(c, f"Week {n+1}", "Week of ____ / ____ / ______", "wk", ("Weeks", "wk"))
        # prev / next
        if n > 0: rrect(c, BODY_L, 20, 90, 24, 12, stroke=SAGE); txt(c, BODY_L + 45, 28, "< Prev", 10, FB, SAGE, "c"); link(c, BODY_L, 20, 90, 24, f"w{n}")
        if n < 25: rrect(c, BODY_L + 100, 20, 90, 24, 12, stroke=SAGE); txt(c, BODY_L + 145, 28, "Next >", 10, FB, SAGE, "c"); link(c, BODY_L + 100, 20, 90, 24, f"w{n+2}")
        gx, gw = BODY_L, BODY_R - BODY_L; top = BODY_T - 8
        cwid = gw / 7; bh = 330
        for k, d in enumerate(DAYS):
            x = gx + k * cwid
            rrect(c, x + 3, top - 28, cwid - 6, 26, 8, fill=INK); txt(c, x + cwid / 2, top - 20, d.upper(), 11, FB, SAND, "c")
            rrect(c, x + 3, top - 28 - 44, cwid - 6, 40, 8, fill=MIST)
            txt(c, x + 12, top - 28 - 24, "SHIFT", 7, FB, GREY)
            for j, lab in enumerate(["D", "N", "OFF"]):
                cx = x + 46 + j * 28
                c.setStrokeColor(INK); c.setLineWidth(0.8); c.circle(cx, top - 28 - 24 + 3, 9, fill=0, stroke=1); txt(c, cx, top - 28 - 24, lab, 6 if lab=="OFF" else 8, FB, INK, "c")
            rrect(c, x + 3, top - 28 - 44 - bh - 4, cwid - 6, bh, 8, fill="#FFFFFF", stroke=LINE)
            for r in range(1, 12): hline(c, x + 10, x + cwid - 10, top - 76 - r * 26.5)
        yb = top - 76 - bh - 14
        for j, (lab, w_) in enumerate([("Top 3 priorities", 0.36), ("Home & life", 0.30), ("Self-care + notes", 0.30)]):
            bx = gx + sum([0.36, 0.30, 0.30][:j]) * gw + j * 6
            rrect(c, bx, 56, w_ * gw - 6, yb - 56, 10, fill="#FFFFFF", stroke=LINE)
            txt(c, bx + 12, yb - 20, lab, 11, FB)
            for r in range(1, 6): hline(c, bx + 12, bx + w_ * gw - 18, yb - 22 - r * 24)

    # shift log index + 31 pages
    page_end(c); dest(c, "sh", "Shift Logs")
    chrome(c, "Shift Logs", "31 daily shift pages. Tap a number.", "sh")
    for n in range(31):
        x = BODY_L + (n % 8) * 118; y = BODY_T - 20 - (n // 8) * 108 - 86
        rrect(c, x, y, 106, 86, 14, fill="#FFFFFF", stroke=LINE); txt(c, x + 53, y + 34, str(n + 1), 28, FB, INK, "c")
        link(c, x, y, 106, 86, f"s{n+1}")
    HOURS_D = ["7a","8a","9a","10a","11a","12p","1p","2p","3p","4p","5p","6p"]
    HOURS_N = ["7p","8p","9p","10p","11p","12a","1a","2a","3a","4a","5a","6a"]
    for n in range(31):
        page_end(c); dest(c, f"s{n+1}", f"Shift {n+1}", 1)
        chrome(c, f"Shift Log {n+1}", "Date ____ / ____ / ______     Day [  ]   Night [  ]   Hours ______", "sh", ("Shifts", "sh"))
        gx = BODY_L; top = BODY_T - 6; colw = 300
        rrect(c, gx, top - 24, colw, 22, 8, fill=INK); txt(c, gx + 12, top - 17, "HOUR BY HOUR (use the 12 that match your shift)", 8, FB, SAND)
        for j in range(12):
            y = top - 28 - (j + 1) * 46
            rrect(c, gx, y, colw, 44, 6, fill="#FFFFFF", stroke=LINE)
            txt(c, gx + 8, y + 17, HOURS_D[j] if n % 2 == 0 else HOURS_N[j], 10, FB, CORAL)
            hline(c, gx + 44, gx + colw - 10, y + 14)
        x2 = gx + colw + 18; w2 = BODY_R - x2
        def box(y, h, lab, rows=0):
            rrect(c, x2, y, w2, h, 10, fill="#FFFFFF", stroke=LINE); txt(c, x2 + 12, y + h - 18, lab, 11, FB)
            for r in range(1, rows + 1): hline(c, x2 + 12, x2 + w2 - 12, y + h - 20 - r * 24)
        box(top - 178, 176, "Must-do before handoff", 5)
        box(top - 374, 186, "Tasks / follow-ups  (tick when done)", 5)
        box(top - 566, 184 - 0, "Shift notes (no patient identifiers)", 5)
        # check boxes
        for r in range(1, 6):
            c.setStrokeColor(INK); c.rect(x2 + 14, top - 374 + 186 - 20 - r * 24 + 3, 10, 10, fill=0, stroke=1)
        # energy
        txt(c, x2 + 12, 40, "Energy", 10, FB); 
        for k in range(5): c.setStrokeColor(INK); c.circle(x2 + 70 + k * 26, 44, 9, fill=0, stroke=1); txt(c, x2 + 70 + k * 26, 41, str(k + 1), 8, FB, INK, "c")
        txt(c, x2 + 240, 40, "Water", 10, FB)
        for k in range(8): c.setStrokeColor(SAGE); c.setLineWidth(1.2); c.circle(x2 + 290 + k * 22, 44, 7, fill=0, stroke=1)

    # brain sheets index + 10 pages
    page_end(c); dest(c, "br", "Brain Sheets")
    chrome(c, "Brain Sheets", "Patient / task sheets, 4 per page. Use initials or room codes only.", "br")
    for n in range(10):
        x = BODY_L + (n % 5) * 160; y = BODY_T - 20 - (n // 5) * 130 - 100
        rrect(c, x, y, 146, 100, 14, fill="#FFFFFF", stroke=LINE); txt(c, x + 73, y + 42, str(n + 1), 30, FB, INK, "c")
        link(c, x, y, 146, 100, f"b{n+1}")
    for n in range(10):
        page_end(c); dest(c, f"b{n+1}", f"Brain sheet {n+1}", 1)
        chrome(c, f"Brain Sheet {n+1}", "Never write names, DOB or MRN. Follow your facility's privacy rules.", "br", ("Brain", "br"))
        bw = (BODY_R - BODY_L - 16) / 2; bh = (BODY_T - 24 - 36 - 16) / 2
        for q in range(4):
            x = BODY_L + (q % 2) * (bw + 16); y = BODY_T - 8 - (q // 2) * (bh + 16) - bh
            rrect(c, x, y, bw, bh, 12, fill="#FFFFFF", stroke=LINE)
            c.setFillColor(INK); c.roundRect(x, y + bh - 30, bw, 30, 12, fill=1, stroke=0); c.rect(x, y + bh - 30, bw, 14, fill=1, stroke=0)
            txt(c, x + 12, y + bh - 20, "Room / code ______   Age ___   Code status ______", 9, FB, SAND)
            labs = ["Why here / dx", "Meds due (times)", "Labs & vitals to watch", "To do / follow up", "Handoff: Situation - Background - Assessment - Recommendation"]
            sec = (bh - 30) / len(labs)
            for j, lab in enumerate(labs):
                yy = y + bh - 30 - j * sec
                txt(c, x + 10, yy - 14, lab, 8, FB, CORAL if j == 4 else GREY); hline(c, x + 10, x + bw - 10, yy - 28 if j < 4 else yy - 30)
                hline(c, x + 10, x + bw - 10, yy - sec, LINE, 0.4)

    # trackers index
    page_end(c); dest(c, "tr", "Trackers")
    chrome(c, "Trackers", "Tap a tracker.", "tr")
    trk = [("Sleep & Recovery","30-day log","t1"),("Energy & Mood","month grid","t2"),("Overtime & Pay","hours + extra shifts","t3"),
           ("Licence & CE","renewals, hours, dates","t4"),("Shift Swaps","owed / swapped","t5"),("Goals","3-month reset","t6")]
    for i, (a, b, k) in enumerate(trk):
        x = BODY_L + (i % 3) * 324; y = BODY_T - 20 - (i // 3) * 170 - 140
        rrect(c, x, y, 300, 140, 16, fill="#FFFFFF", stroke=LINE); txt(c, x + 22, y + 82, a, 20, FB); txt(c, x + 22, y + 58, b, 11, F, GREY)
        txt(c, x + 22, y + 22, "Open >", 11, FB, CORAL); link(c, x, y, 300, 140, k)
    def tracker_page(key, title, sub, headers, rows=31, widths=None):
        page_end(c); dest(c, key, title, 1)
        chrome(c, title, sub, "tr", ("Trackers", "tr"))
        gx, gw = BODY_L, BODY_R - BODY_L; top = BODY_T - 8
        n = len(headers); widths = widths or [1] * n; tot = sum(widths); rh = (top - 40 - 36) / rows
        c.setFillColor(INK); c.rect(gx, top - 30, gw, 30, fill=1, stroke=0)
        xs = [gx]
        for w_ in widths: xs.append(xs[-1] + gw * w_ / tot)
        for k, hd in enumerate(headers): txt(c, xs[k] + 8, top - 20, hd, 9, FB, SAND)
        for r in range(rows):
            y = top - 30 - (r + 1) * rh
            if r % 2 == 0: c.setFillColor("#FFFFFF"); c.rect(gx, y, gw, rh, fill=1, stroke=0)
            hline(c, gx, gx + gw, y, LINE, 0.4)
            if key != "t3" or True: txt(c, xs[0] + 8, y + rh / 2 - 3, str(r + 1) if rows == 31 else "", 8, F, GREY)
        for k in range(1, n): c.setStrokeColor(LINE); c.setLineWidth(0.4); c.line(xs[k], top - 30, xs[k], top - 30 - rows * rh)
    tracker_page("t1", "Sleep & Recovery", "Day, hours slept, quality 1-5, caffeine cut-off, wind-down done?", ["Day","Bedtime","Wake","Hours","Quality 1-5","Last caffeine","Blackout / mask","Notes"], 31, [0.6,1,1,0.8,1,1.2,1.2,3])
    tracker_page("t2", "Energy & Mood", "Rate each day 1-5. Spot patterns across your rotation.", ["Day","Shift D/N/Off","Energy","Mood","Movement","Meal quality","Water","Win of the day"], 31, [0.6,1.1,0.9,0.9,1,1.1,0.8,3])
    tracker_page("t3", "Overtime & Pay", "Track extra hours, differentials and pay period totals.", ["#","Date","Shift","Hrs worked","OT hrs","Diff %","Gross est.","Notes"], 20, [0.5,1,1,1,1,1,1.2,3])
    tracker_page("t4", "Licence & CE", "Renewals, CE hours and certification dates.", ["#","Item","Number / ID","Issued","Expires","CE hrs needed","CE hrs done","Reminder set"], 16, [0.5,2,1.5,1,1,1,1,1])
    tracker_page("t5", "Shift Swaps", "Who owes whom a shift.", ["#","Date","With","I took / I gave","Owed back by","Done"], 20, [0.5,1,1.5,1.5,1.2,0.8])
    # goals
    page_end(c); dest(c, "t6", "Goals", 1)
    chrome(c, "3-Month Reset", "Pick three goals. Small steps beat big promises.", "tr", ("Trackers", "tr"))
    for i in range(3):
        x = BODY_L + i * 330; y = 60
        rrect(c, x, y, 310, BODY_T - 60 - 10, 14, fill="#FFFFFF", stroke=LINE)
        txt(c, x + 18, BODY_T - 40, f"Goal {i+1}", 18, FB, CORAL)
        for r in range(1, 20): hline(c, x + 18, x + 292, BODY_T - 46 - r * 28)
    # notes
    page_end(c); dest(c, "nt", "Notes")
    chrome(c, "Notes", "Choose a page style. Duplicate pages in your app.", "nt")
    for i, (a, k) in enumerate([("Dot grid", "n1"), ("Lined", "n2"), ("Blank + header", "n3")]):
        x = BODY_L + i * 330; y = BODY_T - 20 - 200
        rrect(c, x, y, 300, 200, 16, fill="#FFFFFF", stroke=LINE); txt(c, x + 22, y + 100, a, 22, FB); txt(c, x + 22, y + 24, "Open >", 11, FB, CORAL); link(c, x, y, 300, 200, k)
    for k, style in [("n1", "dot"), ("n2", "line"), ("n3", "blank")]:
        page_end(c); dest(c, k, {"n1": "Dot grid", "n2": "Lined notes", "n3": "Blank notes"}[k], 1)
        chrome(c, {"n1": "Dot Grid", "n2": "Lined Notes", "n3": "Notes"}[k], "Duplicate this page as needed.", "nt", ("Notes", "nt"))
        if style == "dot":
            for xi in range(BODY_L + 6, int(BODY_R), 24):
                for yi in range(BODY_B + 6, int(BODY_T) - 6, 24): c.setFillColor(LINE); c.circle(xi, yi, 1.1, fill=1, stroke=0)
        elif style == "line":
            for yi in range(BODY_B + 10, int(BODY_T) - 10, 28): hline(c, BODY_L, BODY_R, yi)
        else:
            hline(c, BODY_L, BODY_R, BODY_T - 20, INK, 1)
    c.showPage(); c.save()

# =====================================================================
# 2) PRINTABLE PACKS (A4 + US Letter) -- portrait, proportional layout
# =====================================================================
def pkg_page(c, W_, H_, title, sub, n, total, brand):
    bg(c, W_, H_)
    m = W_ * 0.07
    c.setFillColor(INK); c.rect(0, H_ - 62, W_, 62, fill=1, stroke=0)
    txt(c, m, H_ - 38, title, 20, FB, SAND); txt(c, m, H_ - 53, sub, 8.5, F, SAGE)
    txt(c, W_ - m, H_ - 38, brand, 9, FB, SAGE, "r")
    c.setFillColor(CORAL); c.rect(0, H_ - 66, W_ * 0.18, 4, fill=1, stroke=0)
    txt(c, W_ / 2, 20, f"{n} / {total}", 8, F, GREY, "c")
    return m

def build_shift_pack(name, size):
    W_, H_ = size
    path = os.path.join(OUT, f"Shiftwise_Printable_Shift_Planner_Pack_{name}.pdf")
    c = canvas.Canvas(path, pagesize=size); c.setTitle(f"Shiftwise Printable Shift Planner Pack ({name})"); c.setAuthor("Shiftwise")
    T = 8; B = "SHIFTWISE"
    # 1 cover / how to
    bg(c, W_, H_); c.setFillColor(INK); c.rect(0, H_ * 0.45, W_, H_ * 0.55, fill=1, stroke=0)
    c.setFillColor(CORAL); c.circle(W_ * 0.72, H_ * 0.8, 46, fill=1, stroke=0); c.setFillColor(INK); c.circle(W_ * 0.72 + 18, H_ * 0.8 + 8, 42, fill=1, stroke=0)
    txt(c, W_ * 0.08, H_ * 0.78, "Shift Planner", 40, FB, SAND); txt(c, W_ * 0.08, H_ * 0.78 - 44, "Printable Pack", 40, FB, SAND)
    txt(c, W_ * 0.08, H_ * 0.78 - 72, f"For nurses & rotating-shift workers  |  {name.replace('_',' ')} size  |  8 pages", 11, F, SAGE)
    y = H_ * 0.38; txt(c, W_ * 0.08, y, "How to use", 16, FB)
    for i, s in enumerate(["Print at 100% / Actual size (turn off 'fit to page').", f"Paper: {name.replace(chr(95),chr(32))}. Use the other file for the other size.",
                           "Print as many copies as you like for your own use.", "Tip: punch holes and keep it in a clipboard or A5/half-letter binder.",
                           "Do not write patient names, DOB or MRN. Follow your employer's privacy rules.",
                           "This planner is an organiser, not a clinical reference."]):
        c.setFillColor(CORAL); c.circle(W_ * 0.085, y - 28 - i * 22 + 3, 2.5, fill=1, stroke=0); txt(c, W_ * 0.1, y - 28 - i * 22, s, 10.5)
    txt(c, W_ * 0.08, 40, "Personal use only. No resale or redistribution of the files.", 8.5, F, GREY)
    # 2 brain sheet
    c.showPage(); m = pkg_page(c, W_, H_, "12-Hour Shift Brain Sheet", "Date ____/____/______    Unit ________    Day [ ]  Night [ ]", 2, T, B)
    top = H_ - 86; colw = (W_ - 2 * m - 14) / 2
    rrect(c, m, top - 18, W_ - 2 * m, 18, 5, fill=MIST); txt(c, m + 8, top - 13, "Top 3 priorities:  1 ______________________   2 ______________________   3 ______________________", 8, FB)
    hrs = ["7","8","9","10","11","12","1","2","3","4","5","6"]
    rowh = (top - 30 - 120) / 12
    for side in range(2):
        x = m + side * (colw + 14)
        c.setFillColor(INK); c.rect(x, top - 40, colw, 18, fill=1, stroke=0); txt(c, x + 6, top - 34, "7 AM - 7 PM" if side == 0 else "7 PM - 7 AM", 8.5, FB, SAND)
        for j in range(12):
            y = top - 40 - (j + 1) * rowh
            rrect(c, x, y, colw, rowh, 0, fill="#FFFFFF" if j % 2 == 0 else None, stroke=LINE, lw=0.4)
            txt(c, x + 5, y + rowh / 2 - 3, hrs[j] + (" a" if (side == 0 and j < 5) or (side == 1 and j >= 5) else " p"), 8.5, FB, CORAL)
    yb = top - 40 - 12 * rowh - 10
    for k, lab in enumerate(["Breaks / meals", "Must-do before handoff", "Notes"]):
        bw = (W_ - 2 * m - 20) / 3; x = m + k * (bw + 10)
        rrect(c, x, 40, bw, yb - 40, 8, fill="#FFFFFF", stroke=LINE); txt(c, x + 8, yb - 16, lab, 9, FB)
        for r in range(1, int((yb - 50) / 20)): hline(c, x + 8, x + bw - 8, yb - 18 - r * 20)
    # 3 patient / task brain sheet
    c.showPage(); m = pkg_page(c, W_, H_, "Patient & Task Brain Sheet", "Use room codes or initials only. No names, DOB or MRN.", 3, T, B)
    top = H_ - 82; bw = (W_ - 2 * m - 12) / 2; bh = (top - 36 - 12) / 2
    for q in range(4):
        x = m + (q % 2) * (bw + 12); y = top - (q // 2) * (bh + 12) - bh
        rrect(c, x, y, bw, bh, 8, fill="#FFFFFF", stroke=LINE)
        c.setFillColor(INK); c.roundRect(x, y + bh - 22, bw, 22, 8, fill=1, stroke=0); c.rect(x, y + bh - 22, bw, 10, fill=1, stroke=0)
        txt(c, x + 8, y + bh - 15, "Room / code ______  Age ___  Code status ______", 7.5, FB, SAND)
        labs = ["Why here / dx", "Meds due (times)", "Labs & vitals to watch", "To do / follow up", "Handoff (S-B-A-R)"]
        sec = (bh - 22) / 5
        for j, lab in enumerate(labs):
            yy = y + bh - 22 - j * sec; txt(c, x + 7, yy - 11, lab, 7, FB, CORAL if j == 4 else GREY); hline(c, x + 7, x + bw - 7, yy - 24, LINE, .4); hline(c, x + 7, x + bw - 7, yy - sec, LINE, .4)
    # 4 weekly schedule + rotation
    c.showPage(); m = pkg_page(c, W_, H_, "Weekly Shift Planner", "Week of ____/____/______", 4, T, B)
    top = H_ - 84; cw = (W_ - 2 * m) / 7
    for k, d in enumerate(DAYS):
        x = m + k * cw; rrect(c, x + 1.5, top - 20, cw - 3, 20, 5, fill=INK); txt(c, x + cw / 2, top - 14, d.upper(), 8.5, FB, SAND, "c")
        rrect(c, x + 1.5, top - 48, cw - 3, 26, 5, fill=MIST)
        for j, lab in enumerate(["D", "N", "OFF"]):
            cx = x + cw * (0.2 + j * 0.3); c.setStrokeColor(INK); c.setLineWidth(.7); c.circle(cx, top - 35, 6.5, fill=0, stroke=1); txt(c, cx, top - 37.5, lab, 4.8 if lab == "OFF" else 6.5, FB, INK, "c")
        bh = (top - 52) * 0.5; rrect(c, x + 1.5, top - 52 - bh, cw - 3, bh, 5, fill="#FFFFFF", stroke=LINE)
        for r in range(1, int(bh / 22)): hline(c, x + 6, x + cw - 6, top - 52 - r * 22)
    y2 = top - 52 - (top - 52) * 0.5 - 14
    txt(c, m, y2 - 4, "4-week rotation map", 11, FB)
    rh = 26; ytop = y2 - 14
    for r in range(5):
        y = ytop - r * rh; 
        if r == 0:
            for k, d in enumerate(DAYS): txt(c, m + 56 + (k + .5) * ((W_ - 2 * m - 56) / 7), y - 14, d, 8, FB, GREY, "c")
        else:
            txt(c, m, y - 14, f"Week {r}", 8.5, FB)
            for k in range(7): rrect(c, m + 56 + k * ((W_ - 2 * m - 56) / 7) + 2, y - rh + 4, (W_ - 2 * m - 56) / 7 - 4, rh - 6, 5, fill="#FFFFFF", stroke=LINE, lw=.5)
    yb = ytop - 5 * rh - 14
    rrect(c, m, 40, W_ - 2 * m, yb - 40, 8, fill="#FFFFFF", stroke=LINE); txt(c, m + 8, yb - 16, "Week notes & non-negotiables (sleep, family, appointments)", 9, FB)
    for r in range(1, int((yb - 50) / 20)): hline(c, m + 8, W_ - m - 8, yb - 20 - r * 20)
    # 5 sleep & recovery month
    c.showPage(); m = pkg_page(c, W_, H_, "Sleep & Recovery Tracker", "Month ____________   Spot patterns across days and nights", 5, T, B)
    top = H_ - 82; hd = ["Day", "Shift", "Bed", "Wake", "Hrs", "Quality 1-5", "Caffeine cut-off", "Notes"]; wd = [.5, .7, .8, .8, .6, 1, 1.2, 3]
    xs = [m]; 
    for w_ in wd: xs.append(xs[-1] + (W_ - 2 * m) * w_ / sum(wd))
    c.setFillColor(INK); c.rect(m, top - 22, W_ - 2 * m, 22, fill=1, stroke=0)
    for k, h_ in enumerate(hd): txt(c, xs[k] + 5, top - 15, h_, 7.5, FB, SAND)
    rh = (top - 22 - 150) / 31
    for r in range(31):
        y = top - 22 - (r + 1) * rh
        if r % 2 == 0: c.setFillColor("#FFFFFF"); c.rect(m, y, W_ - 2 * m, rh, fill=1, stroke=0)
        hline(c, m, W_ - m, y, LINE, .35); txt(c, xs[0] + 5, y + rh / 2 - 2.5, str(r + 1), 7, F, GREY)
    for k in range(1, len(hd)): c.setStrokeColor(LINE); c.setLineWidth(.35); c.line(xs[k], top - 22, xs[k], top - 22 - 31 * rh)
    yb = top - 22 - 31 * rh - 12
    rrect(c, m, 40, W_ - 2 * m, yb - 40, 8, fill=MIST); txt(c, m + 8, yb - 16, "What helped me sleep this month:", 9, FB)
    for r in range(1, 4): hline(c, m + 8, W_ - m - 8, yb - 16 - r * 20, SAGE)
    # 6 energy / self-care
    c.showPage(); m = pkg_page(c, W_, H_, "Self-Care & Energy Check-in", "Tick it, don't track it perfectly.", 6, T, B)
    top = H_ - 84; items = ["Water (8 circles)", "Real meal", "Moved my body", "Daylight / outside", "Screen-free wind-down", "Talked to a friend"]
    cw2 = (W_ - 2 * m - 130) / 7
    for k, d in enumerate(DAYS): txt(c, m + 130 + (k + .5) * cw2, top - 10, d, 8.5, FB, INK, "c")
    for i, it in enumerate(items):
        y = top - 24 - (i + 1) * 34; rrect(c, m, y, W_ - 2 * m, 30, 7, fill="#FFFFFF", stroke=LINE, lw=.5); txt(c, m + 8, y + 11, it, 9, FB)
        for k in range(7): c.setStrokeColor(SAGE); c.setLineWidth(1.1); c.circle(m + 130 + (k + .5) * cw2, y + 15, 8, fill=0, stroke=1)
    y = top - 24 - 7 * 34 - 10
    txt(c, m, y, "Energy this week (colour in)", 10, FB)
    for k in range(7):
        x = m + 130 + k * cw2 + 4
        for L in range(5): c.setStrokeColor(INK); c.setLineWidth(.6); c.rect(x, y - 14 - (L + 1) * 16, cw2 - 8, 14, fill=0, stroke=1)
        txt(c, m + 100, y - 14 - (k < 5) * 0, "", 1)
    txt(c, m, y - 14 - 16, "High", 7.5, F, GREY); txt(c, m, y - 14 - 5 * 16 + 4, "Low", 7.5, F, GREY)
    yb = y - 14 - 5 * 16 - 16
    rrect(c, m, 40, W_ - 2 * m, yb - 40, 8, fill=MIST); txt(c, m + 8, yb - 16, "One thing I'm proud of this week:", 9, FB)
    for r in range(1, int((yb - 50) / 22)): hline(c, m + 8, W_ - m - 8, yb - 18 - r * 22, SAGE)
    # 7 pay / overtime / licence
    c.showPage(); m = pkg_page(c, W_, H_, "Overtime, Pay & Licence Log", "Know your hours. Never miss a renewal.", 7, T, B)
    top = H_ - 82; hd = ["Date", "Shift", "Hrs", "OT hrs", "Diff %", "Notes"]; wd = [1, 1, .7, .8, .8, 3]
    xs = [m]
    for w_ in wd: xs.append(xs[-1] + (W_ - 2 * m) * w_ / sum(wd))
    c.setFillColor(INK); c.rect(m, top - 20, W_ - 2 * m, 20, fill=1, stroke=0)
    for k, h_ in enumerate(hd): txt(c, xs[k] + 5, top - 14, h_, 7.5, FB, SAND)
    rh = 19
    for r in range(15):
        y = top - 20 - (r + 1) * rh
        if r % 2 == 0: c.setFillColor("#FFFFFF"); c.rect(m, y, W_ - 2 * m, rh, fill=1, stroke=0)
        hline(c, m, W_ - m, y, LINE, .35)
    yb = top - 20 - 15 * rh - 18
    txt(c, m, yb, "Licence & certification tracker", 11, FB)
    hd2 = ["Item", "ID / number", "Expires", "CE needed", "CE done"]; wd2 = [2, 1.6, 1, 1, 1]; xs2 = [m]
    for w_ in wd2: xs2.append(xs2[-1] + (W_ - 2 * m) * w_ / sum(wd2))
    c.setFillColor(MIST); c.rect(m, yb - 26, W_ - 2 * m, 20, fill=1, stroke=0)
    for k, h_ in enumerate(hd2): txt(c, xs2[k] + 5, yb - 20, h_, 7.5, FB)
    for r in range(7): hline(c, m, W_ - m, yb - 26 - (r + 1) * 21, LINE, .35)
    # 8 notes
    c.showPage(); m = pkg_page(c, W_, H_, "Notes & Brain Dump", "Lined on top, dotted below.", 8, T, B)
    top = H_ - 86; split = H_ * 0.48
    for yy in range(int(split), int(top), 22): hline(c, m, W_ - m, yy)
    for xi in range(int(m), int(W_ - m), 18):
        for yi in range(40, int(split) - 10, 18): c.setFillColor(LINE); c.circle(xi, yi, 1, fill=1, stroke=0)
    c.showPage(); c.save()
    return path

# =====================================================================
# 3) PET CARE PACK (A4 + US Letter) -- second-niche sample, same design system
# =====================================================================
def build_pet_pack(name, size):
    W_, H_ = size
    path = os.path.join(OUT, f"Shiftwise_Pet_Care_Binder_Pack_{name}.pdf")
    c = canvas.Canvas(path, pagesize=size); c.setTitle(f"Pet Care Binder Pack ({name})"); c.setAuthor("Shiftwise")
    T = 6; B = "SHIFTWISE PETS"
    bg(c, W_, H_); c.setFillColor(SAGE); c.rect(0, H_ * 0.5, W_, H_ * 0.5, fill=1, stroke=0)
    c.setFillColor(INK)
    for dx, dy, r in [(0, 0, 26), (-48, 34, 14), (-16, 62, 14), (22, 62, 14), (54, 34, 14)]: c.circle(W_ * 0.72 + dx, H_ * 0.76 + dy, r, fill=1, stroke=0)  # paw motif
    txt(c, W_ * 0.08, H_ * 0.76, "Pet Care", 42, FB, INK); txt(c, W_ * 0.08, H_ * 0.76 - 46, "Binder Pack", 42, FB, INK)
    txt(c, W_ * 0.08, H_ * 0.76 - 74, f"Dogs, cats & small pets  |  {name.replace('_',' ')}  |  6 pages", 11, F, INK)
    y = H_ * 0.4; txt(c, W_ * 0.08, y, "How to use", 16, FB)
    for i, s in enumerate(["Print at 100% / Actual size.", "One set per pet. Keep with your vet records.", "Not a substitute for veterinary advice.", "Personal use only."]):
        c.setFillColor(CORAL); c.circle(W_ * 0.085, y - 28 - i * 22 + 3, 2.5, fill=1, stroke=0); txt(c, W_ * 0.1, y - 28 - i * 22, s, 10.5)
    def table(top, title, hd, wd, rows, rh=24):
        txt(c, m, top, title, 11, FB); top -= 8
        xs = [m]
        for w_ in wd: xs.append(xs[-1] + (W_ - 2 * m) * w_ / sum(wd))
        c.setFillColor(INK); c.rect(m, top - 20, W_ - 2 * m, 20, fill=1, stroke=0)
        for k, h_ in enumerate(hd): txt(c, xs[k] + 5, top - 14, h_, 7.5, FB, SAND)
        for r in range(rows):
            y = top - 20 - (r + 1) * rh
            if r % 2 == 0: c.setFillColor("#FFFFFF"); c.rect(m, y, W_ - 2 * m, rh, fill=1, stroke=0)
            hline(c, m, W_ - m, y, LINE, .4)
        for k in range(1, len(hd)): c.setStrokeColor(LINE); c.setLineWidth(.4); c.line(xs[k], top - 20, xs[k], top - 20 - rows * rh)
        return top - 20 - rows * rh - 20
    c.showPage(); m = pkg_page(c, W_, H_, "Pet Profile", "Everything a sitter or vet needs on one page", 2, T, B)
    top = H_ - 92
    fields = ["Name", "Species / breed", "Birthday / age", "Colour & markings", "Microchip #", "Vet clinic & phone", "Emergency vet (24h)", "Insurance & policy #", "Allergies", "Medical conditions"]
    for i, f in enumerate(fields):
        y = top - i * 34; txt(c, m, y, f, 8.5, FB, GREY); hline(c, m + 130, W_ - m, y - 3, INK, .6)
    y = top - 10 * 34 - 6; rrect(c, m, 50, W_ * 0.35, y - 50, 10, fill="#FFFFFF", stroke=LINE); txt(c, m + 10, y - 16, "Photo", 9, FB, GREY)
    rrect(c, m + W_ * 0.35 + 12, 50, W_ - 2 * m - W_ * 0.35 - 12, y - 50, 10, fill=MIST); txt(c, m + W_ * 0.35 + 22, y - 16, "Quirks, fears & favourite things", 9, FB)
    for r in range(1, int((y - 60) / 22)): hline(c, m + W_ * 0.35 + 22, W_ - m - 10, y - 20 - r * 22, SAGE)
    c.showPage(); m = pkg_page(c, W_, H_, "Vaccines & Vet Visits", "Dates, due dates and what was done", 3, T, B)
    y = table(H_ - 90, "Vaccinations & preventatives", ["Item", "Date given", "Next due", "Vet / lot #"], [2, 1, 1, 1.5], 9)
    table(y, "Vet visit log", ["Date", "Reason", "Findings / advice", "Cost"], [1, 1.6, 3, .8], 9)
    c.showPage(); m = pkg_page(c, W_, H_, "Medication & Supplements", "Dose, timing and tick-off for the week", 4, T, B)
    y = table(H_ - 90, "Current medications", ["Name", "Dose", "How often", "Start", "End"], [2, 1, 1.4, 1, 1], 7)
    top = y; txt(c, m, top, "Weekly dose check", 11, FB); cw = (W_ - 2 * m - 110) / 7
    for k, d in enumerate(DAYS): txt(c, m + 110 + (k + .5) * cw, top - 16, d, 8, FB, GREY, "c")
    for i in range(6):
        yy = top - 26 - (i + 1) * 30; hline(c, m, W_ - m, yy + 4, LINE, .4)
        for k in range(7): c.setStrokeColor(SAGE); c.setLineWidth(1); c.circle(m + 110 + (k + .5) * cw, yy + 19, 7, fill=0, stroke=1)
    c.showPage(); m = pkg_page(c, W_, H_, "Feeding, Weight & Care", "Spot changes early", 5, T, B)
    y = table(H_ - 90, "Food & feeding plan", ["Meal", "Food / brand", "Amount", "Time"], [1, 2.5, 1, 1], 5)
    y = table(y, "Weight log", ["Date", "Weight", "Body score 1-9", "Notes"], [1, 1, 1.2, 3], 8)
    table(y, "Grooming, nails, teeth & flea/tick", ["Task", "Last done", "Next due", "Notes"], [2, 1, 1, 2], 5)
    c.showPage(); m = pkg_page(c, W_, H_, "Pet Sitter Instructions", "Hand this page over before you leave", 6, T, B)
    top = H_ - 92
    for i, f in enumerate(["Dates away", "Your contact number", "Backup contact", "Feeding times & amounts", "Walks / play routine", "Medication instructions", "House rules (sofa? treats?)", "Where things are (food, leads, litter)", "Do NOT feed / give", "Anything else"]):
        y = top - i * 36; txt(c, m, y, f, 8.5, FB, GREY); hline(c, m + 150, W_ - m, y - 3, INK, .6); hline(c, m, W_ - m, y - 18, LINE, .4)
    c.showPage(); c.save()
    return path

if __name__ == "__main__":
    build_digital()
    for nm, sz in [("A4", A4), ("US_Letter", letter)]:
        build_shift_pack(nm, sz); build_pet_pack(nm, sz)
    for f in sorted(os.listdir(OUT)): print(f, os.path.getsize(os.path.join(OUT, f)) // 1024, "KB")
