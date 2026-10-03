from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
D = "/usr/share/fonts/truetype/liberation/"
for n, f in [("Sans","LiberationSans-Regular"),("Sans-B","LiberationSans-Bold"),
             ("Serif","LiberationSerif-Regular"),("Serif-B","LiberationSerif-Bold"),
             ("Serif-I","LiberationSerif-Italic"),("Mono-B","LiberationMono-Bold")]:
    pdfmetrics.registerFont(TTFont(n, D+f+".ttf"))
IN = 72.0
def margins(pageno, inside, outside):
    """KDP: page 1 is a right-hand (recto) page -> odd pages have gutter on the left."""
    return (inside, outside) if pageno % 2 == 1 else (outside, inside)
