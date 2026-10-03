"""Generates scriptable assets for the Keyline Studio real-estate Canva shop.
Run: python3 generate_assets.py   (needs reportlab, pillow)
Outputs into ./assets/. All designs are original."""
import os
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(OUT, exist_ok=True)
TEAL, SAND, BRASS, INK, SAGE, WHITE = "#14424A", "#F3EBDD", "#B8893B", "#1C2528", "#8FA89B", "#FFFFFF"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
F = lambda p, s: ImageFont.truetype(p, s)

def center(d, text, y, font, fill, w):
    tw = d.textlength(text, font=font)
    d.text(((w - tw) / 2, y), text, font=font, fill=fill)

def slide(w, h, title, sub, bg, fg, accent):
    im = Image.new("RGB", (w, h), bg)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w, 14], fill=accent)
    d.line([int(w*.1), int(h*.52), int(w*.9), int(h*.52)], fill=accent, width=3)
    center(d, title, int(h*.30), F(SERIF_B, int(w*.075)), fg, w)
    center(d, sub, int(h*.58), F(SANS, int(w*.04)), fg, w)
    d.rectangle([int(w*.07), int(h*.9), int(w*.93), int(h*.9)+6], fill=accent)
    return im

def cover_mockup(fname, headline, bullets, price_badge):
    W = 2000
    im = Image.new("RGB", (W, W), SAND)
    d = ImageDraw.Draw(im)
    center(d, headline, 90, F(SERIF_B, 92), TEAL, W)
    d.line([600, 230, 1400, 230], fill=BRASS, width=5)
    # three slide thumbnails (landscape 16:9) staggered
    specs = [("Welcome", "Your home-buying roadmap", TEAL, WHITE, BRASS),
             ("How I Get Paid", "Plain-English compensation", SAND, TEAL, BRASS),
             ("Your Next 30 Days", "Step-by-step timeline", SAGE, INK, WHITE)]
    pos = [(110, 330), (1000, 420), (560, 900)]
    for (t, s, bg, fg, ac), (x, y) in zip(specs, pos):
        sl = slide(880, 495, t, s, bg, fg, ac)
        d.rectangle([x+14, y+14, x+894, y+509], fill="#CFC6B4")
        im.paste(sl, (x, y))
    # bullets
    y = 1560
    for b in bullets:
        d.ellipse([220, y+14, 244, y+38], fill=BRASS)
        d.text((270, y), b, font=F(SANS_B, 52), fill=INK)
        y += 90
    d.ellipse([1500, 1160, 1900, 1560], fill=TEAL)
    center_x = 1700
    pf = F(SERIF_B, 90)
    tw = d.textlength(price_badge, font=pf)
    d.text((center_x - tw/2, 1320), price_badge, font=pf, fill=WHITE)
    tw = d.textlength("EDITABLE IN CANVA", font=F(SANS_B, 26))
    d.text((center_x - tw/2, 1250), "EDITABLE IN CANVA", font=F(SANS_B, 26), fill=SAND)
    im.save(os.path.join(OUT, fname))

def palette_png():
    sw = [("Deep Teal", TEAL), ("Warm Sand", SAND), ("Brass", BRASS), ("Ink", INK), ("Sage", SAGE), ("White", WHITE)]
    im = Image.new("RGB", (1800, 600), WHITE); d = ImageDraw.Draw(im)
    for i, (n, c) in enumerate(sw):
        x = i * 300
        d.rectangle([x, 0, x+300, 450], fill=c)
        d.text((x+20, 470), n, font=F(SANS_B, 32), fill=INK)
        d.text((x+20, 520), c.upper(), font=F(SANS, 30), fill=INK)
    im.save(os.path.join(OUT, "brand_palette.png"))

def carousel_samples():
    items = [("Pre-approval first", "Why it comes before touring", TEAL, WHITE, BRASS),
             ("What is a buyer agreement?", "In plain English", SAND, TEAL, BRASS),
             ("Closing costs 101", "Where the money goes", SAGE, INK, WHITE)]
    for i, (t, s, bg, fg, ac) in enumerate(items, 1):
        slide(1080, 1350, t, s, bg, fg, ac).save(os.path.join(OUT, f"sample_carousel_{i}.png"))

def hc(c): return HexColor(c)

def open_house_signin_pdf():
    """A real, printable free lead-magnet: Open House Sign-In Sheet (original layout)."""
    c = canvas.Canvas(os.path.join(OUT, "free_open_house_sign_in.pdf"), pagesize=letter)
    W, H = letter
    c.setFillColor(hc(TEAL)); c.rect(0, H-110, W, 110, stroke=0, fill=1)
    c.setFillColor(hc(WHITE)); c.setFont("Times-Bold", 30); c.drawString(48, H-60, "Welcome to the Open House")
    c.setFont("Helvetica", 12); c.setFillColor(hc(SAND))
    c.drawString(48, H-86, "Property address: ______________________________   Date: ______________")
    c.setFillColor(hc(BRASS)); c.rect(0, H-118, W, 8, stroke=0, fill=1)
    cols = [("Name", 48, 150), ("Phone", 198, 110), ("Email", 308, 150), ("Working w/ agent?", 458, 70), ("Pre-approved?", 528, 40)]
    y = H-150
    c.setFillColor(hc(INK)); c.setFont("Helvetica-Bold", 9)
    for n, x, w in cols: c.drawString(x+2, y+4, n)
    c.setStrokeColor(hc(SAGE)); c.setLineWidth(.6)
    for r in range(17):
        yy = y - r*38 - 8
        c.line(48, yy, W-44, yy)
        if r % 2 == 0:
            c.setFillColor(hc(SAND)); c.rect(48, yy-30, W-92, 30, stroke=0, fill=1)
    c.setStrokeColor(hc(SAGE))
    for n, x, w in cols: c.line(x, y+14, x, y-17*38+0)
    c.setFillColor(hc(INK)); c.setFont("Helvetica-Oblique", 8)
    c.drawString(48, 34, "By signing, you agree to be contacted about this property. Template by Keyline Studio (sample).  Equal Housing Opportunity.")
    c.save()

def delivery_pdf():
    """The PDF Etsy sends the buyer: holds the Canva template link. Edit LINK before upload."""
    LINK = "https://www.canva.com/design/REPLACE_WITH_YOUR_TEMPLATE_LINK/use"
    c = canvas.Canvas(os.path.join(OUT, "delivery_template_access.pdf"), pagesize=letter)
    W, H = letter
    c.setFillColor(hc(SAND)); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(hc(TEAL)); c.rect(0, H-160, W, 160, stroke=0, fill=1)
    c.setFillColor(hc(WHITE)); c.setFont("Times-Bold", 32); c.drawCentredString(W/2, H-85, "Thank you for your purchase!")
    c.setFont("Helvetica", 14); c.drawCentredString(W/2, H-115, "Your editable Canva template is ready.")
    c.setFillColor(hc(BRASS)); c.roundRect(W/2-150, H-290, 300, 56, 10, stroke=0, fill=1)
    c.setFillColor(hc(WHITE)); c.setFont("Helvetica-Bold", 16); c.drawCentredString(W/2, H-268, "CLICK HERE TO OPEN YOUR TEMPLATE")
    c.linkURL(LINK, (W/2-150, H-290, W/2+150, H-234), relative=0)
    steps = ["1. Click the button above (you need a free Canva account; log in or sign up).",
             "2. Canva asks to 'Use template' - click it. A personal copy opens in your account.",
             "3. Replace the sample text, logo, colors, and photos with your own.",
             "4. Download as PDF (print) or PNG (social), or share a view link.",
             "5. Fonts used (Playfair Display, Lato) are included in Canva - nothing to install."]
    y = H-340; c.setFillColor(hc(INK)); c.setFont("Helvetica", 12)
    for s in steps: c.drawString(60, y, s); y -= 26
    c.setFont("Helvetica-Bold", 12); c.drawString(60, y-14, "License")
    c.setFont("Helvetica", 11)
    for i, s in enumerate(["For use by the purchaser in their own real estate business. You may not resell, share,",
                           "or redistribute the template or its link. Not legal advice; not a contract form.",
                           "Please verify disclosures, license number, and brokerage requirements for your state."]):
        c.drawString(60, y-34-i*17, s)
    c.setFont("Helvetica", 11); c.drawString(60, y-110, "Questions? Message us through Etsy. Reviews help a small shop a lot - thank you!")
    c.save()

if __name__ == "__main__":
    cover_mockup("mockup_cover_buyer_consultation.png", "Buyer Consultation Presentation",
                 ["16 editable Canva pages", "Plain-English commission talk track", "Fill-in blanks + brand colors"], "$24")
    cover_mockup("mockup_cover_listing_launch_bundle.png", "Listing Launch Bundle",
                 ["Listing presentation + open house kit", "36 Just Listed / Sold posts", "Free Canva account works"], "$39")
    palette_png(); carousel_samples(); open_house_signin_pdf(); delivery_pdf()
    print("done:", sorted(os.listdir(OUT)))
