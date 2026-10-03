"""Listing-image generator (Pillow).

Produces 2000x2000 JPG/PNG images in the style that converts for digital products:
cover (thumbnail), stack, framed-on-wall, included-card, and feature badges.
Etsy photo guidance [blog-claim, multiple sources]: >=2000px shortest side, up to 10 images, sRGB JPG.
"""
from __future__ import annotations

import os
import random
from typing import Sequence

from PIL import Image, ImageDraw, ImageFilter, ImageFont

SIZE = (2000, 2000)
FONT_FILES = {
    "bold": ["/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
    "regular": ["/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"],
    "serif": ["/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"],
}
THEMES = {
    "sage": {"bg": "#EEF1EA", "ink": "#2B2F2A", "primary": "#6B8F71", "accent": "#D9A96F", "card": "#FFFFFF"},
    "ocean": {"bg": "#E8F1F7", "ink": "#16293B", "primary": "#2F6F9F", "accent": "#F2A65A", "card": "#FFFFFF"},
    "blush": {"bg": "#FBEFEF", "ink": "#3A2A2E", "primary": "#C98B93", "accent": "#8FB3A5", "card": "#FFFFFF"},
    "midnight": {"bg": "#1B2030", "ink": "#EEF1F7", "primary": "#7FA6F5", "accent": "#F5C97F", "card": "#262D44"},
}


def font(kind: str, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for p in FONT_FILES[kind]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def wrap_text(draw: ImageDraw.ImageDraw, text: str, fnt, max_w: int) -> list[str]:
    lines, cur = [], ""
    for w in text.split():
        t = f"{cur} {w}".strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_text(draw, text, kind, max_w, max_h, start=160, min_size=40, spacing=1.15):
    """Largest font size whose wrapped text fits the box. Returns (font, lines)."""
    size = start
    while size >= min_size:
        f = font(kind, size)
        lines = wrap_text(draw, text, f, max_w)
        if len(lines) * size * spacing <= max_h and all(draw.textlength(l, font=f) <= max_w for l in lines):
            return f, lines
        size -= 4
    f = font(kind, min_size)
    return f, wrap_text(draw, text, f, max_w)


def placeholder_page(w=850, h=1100, theme="sage", label="Page preview", seed=1) -> Image.Image:
    """Generic page image (used when you have no real preview): header bar + lines + boxes."""
    t = THEMES[theme]
    rnd = random.Random(seed)
    img = Image.new("RGB", (w, h), t["card"])
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, 140], fill=t["primary"])
    d.text((50, 45), label, font=font("bold", 54), fill="#FFFFFF")
    y = 200
    while y < h - 80:
        d.rounded_rectangle([50, y, 80, y + 30], 6, outline=t["primary"], width=4)
        d.line([110, y + 32, w - 60, y + 32], fill=t["accent"], width=3)
        y += 70 + rnd.randint(0, 6)
    return img


def _shadow(base: Image.Image, box, radius=30, offset=(0, 18), opacity=90):
    sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle([box[0] + offset[0], box[1] + offset[1], box[2] + offset[0], box[3] + offset[1]],
                                 fill=(0, 0, 0, opacity))
    sh = sh.filter(ImageFilter.GaussianBlur(radius))
    base.alpha_composite(sh)


def _paste_page(canvas: Image.Image, page: Image.Image, center, width, angle=0.0):
    ratio = width / page.width
    p = page.convert("RGBA").resize((width, int(page.height * ratio)), Image.LANCZOS)
    pad = 40
    layer = Image.new("RGBA", (p.width + 2 * pad, p.height + 2 * pad), (0, 0, 0, 0))
    _shadow(layer, [pad, pad, pad + p.width, pad + p.height], 24, (0, 14), 80)
    layer.alpha_composite(p, (pad, pad))
    if angle:
        layer = layer.rotate(angle, resample=Image.BICUBIC, expand=True)
    canvas.alpha_composite(layer, (int(center[0] - layer.width / 2), int(center[1] - layer.height / 2)))


def _base(theme: str) -> tuple[Image.Image, dict]:
    t = THEMES[theme]
    return Image.new("RGBA", SIZE, t["bg"]), t


def cover_mockup(pages: Sequence[Image.Image], headline: str, subline: str = "", badges: Sequence[str] = (),
                 theme: str = "sage") -> Image.Image:
    """Thumbnail: big headline on top, fanned page stack below, badge row (e.g. 'INSTANT DOWNLOAD')."""
    img, t = _base(theme)
    d = ImageDraw.Draw(img)
    f, lines = fit_text(d, headline.upper(), "bold", 1700, 380, start=190)
    y = 110
    for ln in lines:
        d.text((SIZE[0] / 2, y), ln, font=f, fill=t["ink"], anchor="mt")
        y += int(f.size * 1.15)
    if subline:
        sf, sl = fit_text(d, subline, "regular", 1600, 120, start=64)
        for ln in sl:
            d.text((SIZE[0] / 2, y + 10), ln, font=sf, fill=t["primary"], anchor="mt")
            y += int(sf.size * 1.2)
    n = max(1, min(len(pages), 3))
    angles = {1: [0], 2: [-6, 5], 3: [-9, 0, 9]}[n]
    xs = {1: [1000], 2: [760, 1240], 3: [640, 1000, 1360]}[n]
    for i in range(n):
        _paste_page(img, pages[i], (xs[i], 1180 + (0 if i != 1 else -30)), 640 if n > 1 else 820, angles[i])
    bx = 90
    for b in badges:
        bf = font("bold", 50)
        w = int(d.textlength(b, font=bf)) + 80
        d.rounded_rectangle([bx, 1830, bx + w, 1940], 55, fill=t["primary"])
        d.text((bx + w / 2, 1885), b, font=bf, fill="#FFFFFF", anchor="mm")
        bx += w + 30
    return img.convert("RGB")


def framed_mockup(page: Image.Image, theme: str = "sage", caption: str = "") -> Image.Image:
    """Page in a frame on a wall above a simple sofa silhouette (for wall art / printables)."""
    img, t = _base(theme)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 1500, 2000, 2000], fill=t["accent"])  # floor
    d.rounded_rectangle([300, 1250, 1700, 1700], 90, fill=t["primary"])  # sofa
    d.rounded_rectangle([240, 1330, 400, 1700], 60, fill=t["primary"])
    d.rounded_rectangle([1600, 1330, 1760, 1700], 60, fill=t["primary"])
    fw = 640
    fh = int(fw * page.height / page.width)
    cx, cy = 1000, 700
    box = [cx - fw // 2 - 40, cy - fh // 2 - 40, cx + fw // 2 + 40, cy + fh // 2 + 40]
    _shadow(img, box, 30, (0, 25), 100)
    d = ImageDraw.Draw(img)
    d.rectangle(box, fill="#2B2B2B")
    d.rectangle([box[0] + 18, box[1] + 18, box[2] - 18, box[3] - 18], fill="#FFFFFF")
    img.alpha_composite(page.convert("RGBA").resize((fw, fh), Image.LANCZOS), (cx - fw // 2, cy - fh // 2))
    if caption:
        d = ImageDraw.Draw(img)
        d.text((1000, 1850), caption, font=font("bold", 56), fill=t["ink"], anchor="mm")
    return img.convert("RGB")


def included_card(title: str, items: Sequence[str], theme: str = "sage", footer: str = "") -> Image.Image:
    """'What's included' image: checklist card."""
    img, t = _base(theme)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([140, 140, 1860, 1860], 60, fill=t["card"])
    d.text((1000, 260), title.upper(), font=font("bold", 110), fill=t["primary"], anchor="mm")
    y = 440
    step = min(150, int(1250 / max(1, len(items))))
    fs = min(70, max(36, step - 50))
    f = font("regular", fs)
    for it in items:
        d.ellipse([260, y, 260 + fs, y + fs], fill=t["primary"])
        d.line([270, y + fs * .5, 260 + fs * .42, y + fs * .75, 250 + fs * .9, y + fs * .25], fill="#FFFFFF", width=8)
        for j, ln in enumerate(wrap_text(d, it, f, 1300)[:2]):
            d.text((260 + fs + 40, y + j * fs * 1.1), ln, font=f, fill=t["ink"])
        y += step
    if footer:
        d.text((1000, 1780), footer, font=font("bold", 54), fill=t["ink"], anchor="mm")
    return img.convert("RGB")


def info_card(headline: str, lines: Sequence[str], theme: str = "sage") -> Image.Image:
    """How-it-works / sizes / formats card with a big headline and numbered steps."""
    img, t = _base(theme)
    d = ImageDraw.Draw(img)
    f, hl = fit_text(d, headline.upper(), "bold", 1700, 300, start=150)
    y = 140
    for ln in hl:
        d.text((1000, y), ln, font=f, fill=t["ink"], anchor="mt")
        y += int(f.size * 1.15)
    y += 80
    step = min(260, int((1900 - y) / max(1, len(lines))))
    nf, tf = font("bold", 90), font("regular", 62)
    for i, ln in enumerate(lines, 1):
        d.ellipse([200, y, 330, y + 130], fill=t["primary"])
        d.text((265, y + 65), str(i), font=nf, fill="#FFFFFF", anchor="mm")
        for j, w in enumerate(wrap_text(d, ln, tf, 1300)[:2]):
            d.text((380, y + 10 + j * 70), w, font=tf, fill=t["ink"])
        y += step
    return img.convert("RGB")


def save_jpeg(img: Image.Image, path: str, quality: int = 90) -> str:
    """Save as sRGB JPEG. Mockups are ~2000px; Etsy guidance suggests keeping files small (<1MB is a blog-claim)."""
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    img.convert("RGB").save(path, "JPEG", quality=quality, optimize=True, dpi=(72, 72))
    return path


def build_set(out_dir: str, headline: str, subline: str, included: Sequence[str], steps: Sequence[str],
              pages: Sequence[Image.Image] | None = None, theme: str = "sage", badges=("INSTANT DOWNLOAD", "PRINTABLE PDF")) -> list[str]:
    """One call -> a 5-image listing gallery."""
    pages = list(pages or [placeholder_page(theme=theme, label=f"Page {i + 1}", seed=i) for i in range(3)])
    out = [
        save_jpeg(cover_mockup(pages, headline, subline, badges, theme), os.path.join(out_dir, "01-cover.jpg")),
        save_jpeg(included_card("What's included", included, theme), os.path.join(out_dir, "02-included.jpg")),
        save_jpeg(framed_mockup(pages[0], theme, "Looks great on your wall or desk"), os.path.join(out_dir, "03-room.jpg")),
        save_jpeg(info_card("How it works", steps, theme), os.path.join(out_dir, "04-how-it-works.jpg")),
        save_jpeg(cover_mockup(pages[:1], "Print at home or at a print shop", "US Letter and A4 included", (), theme),
                  os.path.join(out_dir, "05-print.jpg")),
    ]
    return out
