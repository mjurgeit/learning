# toolkit - reusable tooling for the Digital Business Lab

Python 3.11+, deps: `pillow`, `reportlab`, `pytest` (`pip install -r requirements.txt`).
All commands run from `/home/user/learning/toolkit`.

| Module | What it does |
|---|---|
| `labkit/pdf_design.py` | PDF design system: font registry (Liberation/DejaVu with Helvetica fallback, `register_font_family` for your own TTFs), 5 palettes + WCAG contrast check, `Theme`, `PDFBuilder` with templates (cover, TOC, lined, dot/grid, checklist, weekly, table, license page), external links, internal links, buttons, bookmarks/outline |
| `labkit/listing.py` | Etsy listing generator + validator from a JSON config: title <=140, 13 tags <=20 chars, no duplicates, allowed characters, stuffing/ALL-CAPS warnings, AI-disclosure block + check |
| `labkit/mockup.py` | Pillow listing images (2000x2000 JPG): cover/thumbnail, "what's included" card, framed-on-wall, how-it-works card; `build_set()` makes a 5-image gallery in one call |
| `labkit/revenue.py` | Fee tables (Etsy, Etsy Offsite Ads, Gumroad, Payhip, Stripe-direct, TPT) + conservative/base/optimistic scenario projector + ad break-even ROAS |

## Quick start
```bash
python -m pytest -q                                   # 18 tests
python examples/demo.py examples/demo_out             # PDF + listing + 5 mockups
python -m labkit.listing examples/budget_planner.json # title/tags/description + validation (exit 1 on errors)
python -m labkit.revenue compare --price 12           # net per sale on every platform
python -m labkit.revenue fees --platform etsy --price 9
python -m labkit.revenue scenario --platform etsy --price 9 --listings 20 --ads 30
```

## Using from a business folder
```python
import sys; sys.path.insert(0, "/home/user/learning/toolkit")
from labkit.pdf_design import Theme, PDFBuilder
b = PDFBuilder("planner.pdf", Theme.named("blush", "a4"), title="Planner", footer="MyShop")
b.cover("Daily Planner", "A4 - Printable"); y = b.new_page("Start here")
b.link(48, y, "Shop", "https://example.com"); b.checklist_page("Tasks"); b.save()
```
Listing config keys: `product, product_type, primary_keywords (priority order), extra_tags, attributes, hook, benefits, includes, how_to, faq [[q,a]], ai_used, shop_policy, title, tags` (explicit `title`/`tags` override generation but are still validated).

## Honest limits
- Fee rates are a snapshot (2026-10-03, from secondary sources; Etsy/Gumroad pages were not reachable by the research agent). Edit `PLATFORMS` in `revenue.py` when rates change. Scenario defaults are `[estimate]`, replace with measured shop data.
- Title/tag rules enforced as errors are Etsy's limits; "first 40 chars matter", stuffing and `& % :` rules are heuristic warnings only.
- Tag truncation drops trailing words from over-20-char phrases; review generated tags by hand.
- Mockups are generic vector-style compositions, not photo-realistic scenes. Feed real page renders (e.g. `pdftoppm -png`) via `pages=[Image,...]` for real previews.
- Fonts: bundled lookup uses system Liberation/DejaVu (free licences). Check licences before embedding any other font in a product you sell.
- No tax advice. See `research/02-playbook.md` section on taxes.
