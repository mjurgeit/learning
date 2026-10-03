# Skills, tools and responsibilities

## Skills needed
1. **Product design/layout**: grid, type hierarchy, colour tokens. Here done in code (Python `reportlab`) so product variants are cheap. Free alternatives: Figma/Canva/Affinity (hyperlinks need export-to-PDF with internal links; Canva supports page links but is clunky for 90+ pages).
2. **Etsy SEO**: keyword research (Etsy autocomplete, eRank/Marmalead/EverBee free tiers; RankHero pages for rough volume), title/tag writing, thumbnail CTR.
3. **Mockups/photography**: render PDF pages to PNG (PyMuPDF) and place on iPad/desk scenes. Free: Canva, Figma, Photopea. Needs properly licensed or self-made scene images.
4. **Pinterest marketing**: pin graphics, board SEO, scheduling (free native scheduler, Tailwind paid).
5. **Basic compliance**: Etsy Creativity Standards, AI disclosure, tax basics for digital sales.
6. **Testing**: opening the PDF in GoodNotes, Notability, Noteshelf, Xodo; printing at 100% on A4 and Letter.

## Tools and costs
| Tool | Use | Cost |
|---|---|---|
| Python 3 + reportlab | generate PDFs (`products/build_pdfs.py`) | free |
| PyMuPDF | render previews, check links | free |
| Etsy | marketplace | $0.20/listing + fees (see plan.md) |
| Canva / Figma free | mockups, pin graphics | free |
| GoodNotes / Notability | link testing | free tier or paid (check current price) |
| eRank / Marmalead / EverBee | keyword data | free tier; paid ~$6-30/mo [estimate] |
| Pinterest business | traffic | free |
| Payhip | own store/email | free plan with transaction fee, check current |

## Claude can do
- Write/extend the generator code, make new products and size variants, check links and page counts.
- Write listing copy, tags, descriptions, FAQs, pin text, A/B title variants; keyword brainstorming and clustering.
- Produce mockup images from the PDFs and pin graphics (via code), analyse exported Etsy stats CSVs, plan the calendar.
## Human must do
- Create the Etsy seller account, ID/bank/tax verification, shop name/policies, payouts. Etsy has no public API for creating digital listings that fits this workflow, so listings, file uploads, and images are uploaded by hand (or via the Etsy open API only if the owner registers an app; not assumed).
- Test on a real iPad with GoodNotes; print-test on paper; sign off that claims are true.
- Final Etsy "Creativity Standards" attestations/AI disclosure fields.
- Reply to customers, handle refunds, register for taxes as required locally.
- Check trademark/shop-name availability.

## Learning path (about 4 weeks, part-time)
1. Week 1: Etsy Seller Handbook basics, fee/tax overview, run keyword research on 28 terms.
2. Week 2: open `build_pdfs.py`, change a colour token and one page; regenerate; test links on iPad.
3. Week 3: thumbnail/mockup craft; first Pinterest pins.
4. Week 4: read your Etsy stats (visits, CTR, conversion); decide keep/kill per the plan.
