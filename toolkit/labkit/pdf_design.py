"""PDF design-system library (ReportLab).

Fonts, palettes, page templates and hyperlinks that business folders can reuse.

    from labkit.pdf_design import Theme, PDFBuilder
    b = PDFBuilder("out.pdf", Theme.named("sage"), title="My Planner")
    b.cover("Weekly Planner", "Undated - Letter")
    b.lined_page("Notes"); b.checklist_page("Tasks", ["a", "b"])
    b.save()
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Iterable, Sequence

from reportlab.lib.colors import Color, HexColor
from reportlab.lib.pagesizes import A4, A5, LETTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as rl_canvas

PAGE_SIZES = {"letter": LETTER, "a4": A4, "a5": A5}

# ---- fonts -----------------------------------------------------------------
# Only fonts we may legally embed are listed (DejaVu: free licence; Liberation: SIL OFL).
# Check the licence of any font you add before selling a product that embeds it.
FONT_CANDIDATES = {
    "sans": [
        ("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
         "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    ],
    "serif": [
        ("/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
         "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"),
    ],
}
_registered: dict[str, tuple[str, str]] = {}


def register_font_family(name: str, regular_path: str, bold_path: str) -> tuple[str, str]:
    """Register your own TTF family (e.g. a Google Font you downloaded). Returns (regular, bold) names."""
    reg, bold = f"{name}", f"{name}-Bold"
    pdfmetrics.registerFont(TTFont(reg, regular_path))
    pdfmetrics.registerFont(TTFont(bold, bold_path))
    pdfmetrics.registerFontFamily(reg, normal=reg, bold=bold)
    _registered[name] = (reg, bold)
    return reg, bold


def get_fonts(kind: str = "sans") -> tuple[str, str]:
    """Return (regular, bold) font names; falls back to built-in Helvetica/Times if no TTF found."""
    if kind in _registered:
        return _registered[kind]
    for reg_p, bold_p in FONT_CANDIDATES.get(kind, []):
        if os.path.exists(reg_p) and os.path.exists(bold_p):
            return register_font_family(f"lab-{kind}", reg_p, bold_p)
    fallback = ("Helvetica", "Helvetica-Bold") if kind == "sans" else ("Times-Roman", "Times-Bold")
    _registered[kind] = fallback
    return fallback


# ---- palettes --------------------------------------------------------------
@dataclass(frozen=True)
class Palette:
    name: str
    bg: str
    ink: str
    primary: str
    accent: str
    muted: str
    line: str


PALETTES = {
    "sage": Palette("sage", "#FAF8F3", "#2B2F2A", "#6B8F71", "#D9A96F", "#8A8F87", "#D8DCD3"),
    "ocean": Palette("ocean", "#F6FAFC", "#16293B", "#2F6F9F", "#F2A65A", "#7A8A99", "#D3E0EA"),
    "blush": Palette("blush", "#FFF9F7", "#3A2A2E", "#C98B93", "#8FB3A5", "#9A8A8D", "#EBD9DC"),
    "mono": Palette("mono", "#FFFFFF", "#111111", "#333333", "#999999", "#777777", "#DDDDDD"),
    "midnight": Palette("midnight", "#1B2030", "#EEF1F7", "#7FA6F5", "#F5C97F", "#9AA3B8", "#343C52"),
}


def luminance(hex_color: str) -> float:
    c = HexColor(hex_color)
    def f(v):
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(c.red) + 0.7152 * f(c.green) + 0.0722 * f(c.blue)


def contrast_ratio(a: str, b: str) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


@dataclass
class Theme:
    palette: Palette
    font_kind: str = "sans"
    heading_kind: str = "serif"
    margin: float = 48.0
    page_size: tuple = LETTER

    @classmethod
    def named(cls, name: str, page: str = "letter", **kw) -> "Theme":
        return cls(PALETTES[name], page_size=PAGE_SIZES[page.lower()], **kw)

    def check_contrast(self, minimum: float = 4.5) -> dict[str, float]:
        """WCAG-style contrast of ink and muted text on the background (for accessible products)."""
        p = self.palette
        return {"ink": contrast_ratio(p.ink, p.bg), "muted": contrast_ratio(p.muted, p.bg)}


# ---- builder ---------------------------------------------------------------
class PDFBuilder:
    def __init__(self, path: str, theme: Theme, title: str = "", author: str = "", footer: str = ""):
        self.theme, self.path, self.footer_text = theme, path, footer
        self.c = rl_canvas.Canvas(path, pagesize=theme.page_size)
        self.c.setTitle(title or os.path.basename(path))
        if author:
            self.c.setAuthor(author)
        self.W, self.H = theme.page_size
        self.body, self.bold = get_fonts(theme.font_kind)
        self.head, self.head_bold = get_fonts(theme.heading_kind)
        self.pages = 0
        self._bookmarks: list[tuple[str, str]] = []

    # -- primitives
    def _bg(self):
        p = self.theme.palette
        self.c.setFillColor(HexColor(p.bg))
        self.c.rect(0, 0, self.W, self.H, stroke=0, fill=1)

    def new_page(self, heading: str | None = None, bookmark: str | None = None) -> float:
        """Start a page with background, header, footer. Returns y where content may start."""
        if self.pages:
            self.c.showPage()
        self.pages += 1
        self._bg()
        p, m = self.theme.palette, self.theme.margin
        y = self.H - m
        if bookmark or heading:
            key = f"p{self.pages}"
            self.c.bookmarkPage(key)
            self.c.addOutlineEntry(bookmark or heading, key, level=0)
            self._bookmarks.append((bookmark or heading, key))
        if heading:
            self.c.setFillColor(HexColor(p.ink))
            self.c.setFont(self.head_bold, 24)
            self.c.drawString(m, y - 20, heading)
            self.c.setStrokeColor(HexColor(p.primary))
            self.c.setLineWidth(2)
            self.c.line(m, y - 30, m + 60, y - 30)
            y -= 52
        self._footer()
        return y

    def _footer(self):
        p, m = self.theme.palette, self.theme.margin
        self.c.setFillColor(HexColor(p.muted))
        self.c.setFont(self.body, 8)
        if self.footer_text:
            self.c.drawString(m, m / 2, self.footer_text)
        self.c.drawRightString(self.W - m, m / 2, str(self.pages))

    def text(self, x, y, s, size=11, color=None, bold=False, align="left"):
        self.c.setFillColor(HexColor(color or self.theme.palette.ink))
        self.c.setFont(self.bold if bold else self.body, size)
        {"left": self.c.drawString, "center": self.c.drawCentredString, "right": self.c.drawRightString}[align](x, y, s)

    def wrap(self, s: str, width: float, size=11, bold=False) -> list[str]:
        font = self.bold if bold else self.body
        words, lines, cur = s.split(), [], ""
        for w in words:
            t = f"{cur} {w}".strip()
            if pdfmetrics.stringWidth(t, font, size) <= width:
                cur = t
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    def paragraph(self, x, y, s, width, size=11, leading=None, color=None) -> float:
        leading = leading or size * 1.45
        for ln in self.wrap(s, width, size):
            self.text(x, y, ln, size, color)
            y -= leading
        return y

    # -- hyperlinks
    def link(self, x, y, s, url, size=11):
        """Draw underlined, clickable external link text at baseline (x, y)."""
        col = self.theme.palette.primary
        self.text(x, y, s, size, col)
        w = pdfmetrics.stringWidth(s, self.body, size)
        self.c.setStrokeColor(HexColor(col))
        self.c.setLineWidth(0.6)
        self.c.line(x, y - 1.5, x + w, y - 1.5)
        self.c.linkURL(url, (x, y - 3, x + w, y + size), relative=0)
        return w

    def internal_link(self, x, y, s, bookmark_key, size=11):
        w = pdfmetrics.stringWidth(s, self.body, size)
        self.text(x, y, s, size, self.theme.palette.primary)
        self.c.linkRect("", bookmark_key, (x, y - 3, x + w, y + size), relative=0)
        return w

    def button(self, x, y, w, h, label, url=None, bookmark_key=None):
        p = self.theme.palette
        self.c.setFillColor(HexColor(p.primary))
        self.c.roundRect(x, y, w, h, h / 2.5, stroke=0, fill=1)
        self.text(x + w / 2, y + h / 2 - 4, label, 11, "#FFFFFF", True, "center")
        if url:
            self.c.linkURL(url, (x, y, x + w, y + h), relative=0)
        elif bookmark_key:
            self.c.linkRect("", bookmark_key, (x, y, x + w, y + h), relative=0)

    # -- templates
    def cover(self, title: str, subtitle: str = "", tagline: str = ""):
        p = self.theme.palette
        self.new_page(bookmark="Cover")
        self.c.setFillColor(HexColor(p.primary))
        self.c.rect(0, self.H * 0.38, self.W, self.H * 0.30, stroke=0, fill=1)
        self.c.setFillColor(HexColor(p.accent))
        self.c.rect(0, self.H * 0.38 - 8, self.W, 8, stroke=0, fill=1)
        lines = self.wrap(title, self.W - 2 * self.theme.margin - 20, 36, True) or [title]
        y = self.H * 0.53 + 18 * (len(lines) - 1)
        self.c.setFillColor(HexColor("#FFFFFF"))
        self.c.setFont(self.head_bold, 36)
        for ln in lines:
            self.c.drawCentredString(self.W / 2, y, ln)
            y -= 44
        if subtitle:
            self.text(self.W / 2, self.H * 0.30, subtitle, 14, p.ink, align="center")
        if tagline:
            self.text(self.W / 2, self.H * 0.26, tagline, 10, p.muted, align="center")

    def toc_page(self, entries: Sequence[tuple[str, str]] | None = None, heading="Contents"):
        """Table of contents with clickable internal links. Pages must already be known: pass entries
        [(label, bookmark_key)] or call after building (see add_toc_later)."""
        y = self.new_page(heading, bookmark=heading)
        for label, key in entries or self._bookmarks:
            self.internal_link(self.theme.margin, y, label, key, 13)
            y -= 24

    def lined_page(self, heading="Notes", spacing=26):
        y = self.new_page(heading)
        p, m = self.theme.palette, self.theme.margin
        self.c.setStrokeColor(HexColor(p.line))
        self.c.setLineWidth(0.6)
        while y > m + 20:
            self.c.line(m, y, self.W - m, y)
            y -= spacing

    def grid_page(self, heading="Grid", step=18, dots=True):
        y = self.new_page(heading)
        p, m = self.theme.palette, self.theme.margin
        self.c.setFillColor(HexColor(p.line))
        self.c.setStrokeColor(HexColor(p.line))
        yy = y
        while yy > m + 10:
            x = m
            while x <= self.W - m + 0.1:
                if dots:
                    self.c.circle(x, yy, 0.8, stroke=0, fill=1)
                x += step
            if not dots:
                self.c.line(m, yy, self.W - m, yy)
            yy -= step
        if not dots:
            x = m
            while x <= self.W - m + 0.1:
                self.c.line(x, y, x, yy + step)
                x += step

    def checklist_page(self, heading: str, items: Iterable[str] = (), rows: int = 20):
        y = self.new_page(heading)
        p, m = self.theme.palette, self.theme.margin
        items = list(items)
        for i in range(max(rows, len(items))):
            self.c.setStrokeColor(HexColor(p.primary))
            self.c.setLineWidth(1)
            self.c.roundRect(m, y - 12, 14, 14, 3, stroke=1, fill=0)
            if i < len(items):
                self.text(m + 24, y - 8, items[i], 12)
            self.c.setStrokeColor(HexColor(p.line))
            self.c.setLineWidth(0.5)
            self.c.line(m + 24, y - 14, self.W - m, y - 14)
            y -= 30
            if y < m + 20:
                break

    def weekly_page(self, heading="Week of ____", days=("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")):
        y = self.new_page(heading)
        p, m = self.theme.palette, self.theme.margin
        n = len(days)
        h = (y - m - 10) / n
        for i, d in enumerate(days):
            top = y - i * h
            self.c.setStrokeColor(HexColor(p.line))
            self.c.rect(m, top - h, self.W - 2 * m, h, stroke=1, fill=0)
            self.c.setFillColor(HexColor(p.primary))
            self.c.rect(m, top - h, 52, h, stroke=0, fill=1)
            self.text(m + 26, top - h / 2 - 4, d, 12, "#FFFFFF", True, "center")

    def table_page(self, heading: str, columns: Sequence[str], rows: int = 18, widths: Sequence[float] | None = None):
        y = self.new_page(heading)
        p, m = self.theme.palette, self.theme.margin
        total = self.W - 2 * m
        widths = widths or [total / len(columns)] * len(columns)
        self.c.setFillColor(HexColor(p.primary))
        self.c.rect(m, y - 22, total, 22, stroke=0, fill=1)
        x = m
        for col, w in zip(columns, widths):
            self.text(x + 6, y - 15, col, 10, "#FFFFFF", True)
            x += w
        y -= 22
        for r in range(rows):
            if y - 24 < m + 20:
                break
            self.c.setStrokeColor(HexColor(p.line))
            x = m
            for w in widths:
                self.c.rect(x, y - 24, w, 24, stroke=1, fill=0)
                x += w
            y -= 24

    def license_page(self, shop: str, terms: Sequence[str], url: str | None = None):
        y = self.new_page("Terms of Use", bookmark="Terms of Use")
        m = self.theme.margin
        for t in terms:
            y = self.paragraph(m, y, "- " + t, self.W - 2 * m) - 4
        if url:
            self.link(m, y - 10, f"More from {shop}", url, 12)

    def save(self) -> str:
        self.c.save()
        return self.path
