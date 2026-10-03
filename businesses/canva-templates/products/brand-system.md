# Brand system: Keyline Studio (placeholder name; owner may rename)

Use identical styling across all products so bundles look like one family (and mockups stay consistent).

## Palette (also see assets/brand_palette.png)
| Role | Name | Hex |
|---|---|---|
| Primary | Deep Teal | #14424A |
| Background | Warm Sand | #F3EBDD |
| Accent | Brass | #B8893B |
| Text | Ink | #1C2528 |
| Secondary | Sage | #8FA89B |
| Light | White | #FFFFFF |
Contrast: Ink on Sand and White on Teal both exceed WCAG AA for body text. Brass is for lines/icons/large text only.
Alt colorways (sell as recolor listings later): "Blush & Plum" (#4A2545 / #F6E7E4 / #C98B6B), "Coastal Navy" (#0F2A43 / #EEF3F6 / #D9A441), "Sage Modern" (#2F4A3C / #F1F0E8 / #C27C4E).

## Fonts (all free in Canva, so buyers can edit without Pro)
- Headings: **Playfair Display** Bold/SemiBold (fallback Canva "Lora").
- Body: **Lato** Regular/Bold (fallback "Open Sans").
- Accent labels: Lato Bold, ALL CAPS, letter-spacing +100.

## Type scale (1920x1080 presentation)
H1 72 pt, H2 44 pt, body 24 pt, caption 16 pt. Social (1080x1350): H1 84 pt, body 38 pt.

## Layout rules
- 80 px safe margins on slides; 60 px on social. 12-column grid (Canva guides).
- Brass 4 px rule under every title. Footer: small "[Your Name] | [License #] | Equal Housing Opportunity" placeholder line on every client-facing page.
- Photos: use placeholder frames (Canva "frames") with Canva free photos, or gray boxes labelled "Your photo". Pro photos only if template is sold as link (it is).
- Icons: Canva free line icons, stroke Brass.

## Build workflow in Canva (applies to every product)
1. Create design at stated dimensions (Custom size) in a free or Pro account.
2. Set Brand Kit colors/fonts above. Build page 1, duplicate, vary.
3. Use text boxes with the sample copy from the spec; mark every fill-in as [BRACKETS] in a Brass highlight.
4. Group elements; name pages ("01 Welcome") via notes.
5. Share > Template link > "Anyone with the link can use as a template" (Share > More > Template link). Copy URL.
6. Test: open link in an incognito window logged into a second account; confirm Use-template works and no watermarks/Pro-locked items remain (crown icons are acceptable only because we deliver as a link; still prefer free elements to avoid friction).
7. Paste link into `assets/generate_assets.py` LINK constant, run script to produce the delivery PDF, upload as the Etsy digital file.
8. Keep a second copy of the design (duplicate) as a backup master.
