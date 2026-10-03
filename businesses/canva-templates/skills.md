# Skills, tools and division of labor

## 1. Skills needed
| Skill | Level needed | Free way to learn | Notes |
|---|---|---|---|
| Canva design (layouts, grids, brand kit, template links, Bulk Create) | Intermediate | Canva Design School (free); YouTube "Canva template link Etsy" tutorials | Core production skill; ~15 h to be fluent |
| Etsy SEO (titles, tags, attributes, photos) | Basic-intermediate | Etsy Seller Handbook (free); eRank free tier | Biggest lever on traffic |
| Product photography/mockups | Basic | Canva mockup apps, scripts in products/generate_assets.py | Real screenshots of pages beat fake devices |
| Copywriting for realtors | Basic | Claude drafts; owner edits | Must avoid legal claims |
| Real estate domain sanity-check | Basic | Talk to 1-2 agents; read NAR/state association pages | Critical for credibility; verify state specifics |
| Pinterest marketing | Basic | Pinterest Academy (free) | 3-5 pins/day schedule |
| Bookkeeping/taxes for a small shop | Basic | Spreadsheet; consult tax pro | Digital sales tax / VAT: Etsy collects in many places, verify |

## 2. Tools (free option / paid option)
| Need | Free | Paid (est.) |
|---|---|---|
| Design | Canva Free (template links work) | Canva Pro ~$15/mo [estimate]: Bulk Create, resize, brand kit, premium elements |
| Marketplace | Etsy ($0.20/listing + $15 setup [blog-claim]) | Etsy Ads (optional) |
| Own storefront | Payhip Free (5% fee) | Plus $29/mo 2% [blog-claim] |
| SEO research | Etsy autocomplete, eRank free (limited), Google Trends | Marmalead/eRank Pro ~$6-20/mo [estimate] |
| Mockups | Python script (Pillow/reportlab) in this folder; Canva | Placeit ~$15/mo |
| Pinterest | Business account free; manual scheduling | Tailwind ~$15/mo |
| Email list | Payhip built-in or MailerLite free | n/a |
| Tracking | Etsy stats + results.md | n/a |

## 3. What Claude can do vs what the human must do
**Claude can:** research/verify keywords from public sources; write all listing copy, FAQs, speaker notes, captions; write page-by-page template specs; generate PDFs/PNG mockups via script; build CSVs for Canva Bulk Create; draft Pinterest pin titles/descriptions; track results; propose price/title tests from stats the owner pastes in.
**Claude cannot / human must:**
1. Create Etsy, Payhip, Canva, Pinterest accounts; ID verification, bank/payout setup, tax forms (W-9 etc.).
2. Build the actual Canva files (no Canva file export or API write by script) and create template links; test with a second account.
3. Upload listings and photos (Etsy has no write access for us here), set category/attributes, answer Etsy's "who made it / AI" questions truthfully.
4. Run Etsy autocomplete/eRank manually (etsy.com, canva.com and rankhero.com were blocked from the research sandbox).
5. Respond to buyer messages, handle disputes/refunds policy.
6. Real-estate legal reasonableness check: have an agent or broker skim templates for state compliance.
7. Pay any fees; monitor Etsy policy changes.

## 4. Learning path (about 3 weeks, 6-8 h/week)
1. Week 1: Canva Design School basics; make 1 free practice template; read Etsy Seller Handbook (digital products, Creativity Standards); do keyword autocomplete from plan.md section 5.
2. Week 2: Build Product 8 (entry) end-to-end: template link, delivery PDF (generate_assets.py), listing from listings.md; publish.
3. Week 3: Build Product 1; mockups with real screenshots; start Pinterest board "Real Estate Marketing" and pin 5/day.
4. Ongoing: weekly 30-min stats review; update titles/tags after 30 days of data.

## 5. Delivery file checklist
- Delivery PDF: run `python3 products/generate_assets.py` after editing LINK in the script (one PDF per product; clone function for several links).
- Etsy file limits: 5 files per listing, 20 MB each [blog-claim, verify in Etsy help].
- Backup: duplicate masters in Canva; keep a text file of every template link.
