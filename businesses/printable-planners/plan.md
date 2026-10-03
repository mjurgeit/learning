# Business plan: Shiftwise – planners for people whose week is not 9-to-5

Date: 2026-10-03. Platform: Etsy first (Payhip as second checkout later). Brand name "Shiftwise" is a working name: check Etsy shop-name availability and a USPTO/EUIPO trademark search before opening the shop.

Evidence legend: [verified] = read in a primary or directly searched source; [blog-claim] = seller/affiliate blog; [snippet] = number seen only in a web-search snippet (Etsy and several sites were blocked for direct fetching in this environment, so shop stats could not be opened and must be re-checked by the owner); [estimate] = our assumption.

## 1. Chosen niche and why

**Primary niche: nurses, nursing students and rotating-shift workers** (12-hour days/nights, rotating weeks). **Secondary niches (same design system, cheap to ship): pet-care binders and caregiver (elderly parent) binders.**

Why this and not generic planners:
- Generic terms are saturated. "digital planner" has ~27,100 avg monthly searches but 693,616 competing Etsy listings; "goodnotes" has 140,326 listings; "digital planner goodnotes" keyword difficulty 70/100 ([RankHero keyword pages](https://www.rankhero.com/keywords/digital-planner-goodnotes)) [estimate-tool data].
- Sellers' guides repeatedly name condition/work-pattern planners as under-served: "planners for shift workers whose weeks do not fit a nine-to-five grid", caregiver tools, and pet logs "still flying under the radar" ([Listify AI niche guide](https://www.listifyai.net/blog/low-competition-etsy-niches-digital-products)) [blog-claim]. Specificity converts better: "ADHD weekly planner printable A4" beats "weekly planner printable" ([same](https://www.listifyai.net/blog/low-competition-etsy-niches-digital-products)) [blog-claim].
- Nurse buyers demonstrably pay on Etsy: ScrubNotes shows 19,464 sales / 1,252 reviews; NurseInTheMaking 234.9K sales; a nurse seller claims $2M+ in three years from study guides (RNExplained) ([search result](https://www.etsy.com/shop/ScrubNotes), [snippet]; the $2M is a [blog-claim] and not verified). But those shops sell study guides/notes. Rotating-shift life-management (sleep, overtime, swaps, licence renewals) combined with a hyperlinked tablet planner appears thinly served in what I could see, which is the gap. **Caveat: I could not open Etsy search pages, so "thinly served" is a hypothesis; validate first (section 10, week 1).**
- ADHD planners are real demand but crowded: shops with ~2,400 / ~2,400 / ~1,000 sales and prices from $3.40 up (see teardown). We avoid head-on competition but can borrow the "executive function" angle as a tag, not a core.

## 2. Personas
1. **Maya, 24, nursing student/new grad RN.** iPad + GoodNotes, prints at home. Pain: clinical days, care plans, shifts, NCLEX prep, all in different places. Wants a brain sheet and a planner that matches her rotating schedule. Budget: $5-$15 one-off.
2. **Dev, 38, night-shift RN/paramedic/warehouse worker.** Pain: weeks that repeat in 4-6-week rotations, wrecked sleep, overtime and shift swaps to remember, licence/CE renewal dates. Wants a printable on a clipboard.
3. **Priya, 33, pet owner and sitter-hander** (secondary). Pain: vaccine dates and meds scattered; needs a one-page sitter sheet.
4. **Chris, 45, adult child caregiver** (secondary). Pain: meds, appointments, daily care log. Buyer is stressed and values clarity over decoration.

## 3. Product line: first 10 products

| # | Title (working) | Format | Price | Status |
|---|---|---|---|---|
| 1 | Digital Shift Planner for Nurses & Shift Workers, undated hyperlinked, iPad/GoodNotes | PDF, 96 pages, 923 links | $14.99 | **built** (`products/pdf/Shiftwise_Digital_Shift_Planner_Hyperlinked_iPad.pdf`) |
| 2 | Printable Shift Planner Pack, 12-hour brain sheets, A4 + US Letter | 2 PDFs x 8 pages | $7.99 | **built** |
| 3 | Pet Care Binder Pack, printable, A4 + US Letter | 2 PDFs x 6 pages | $6.99 | **built** |
| 4 | Nursing Student Clinical Planner (semester + clinical-day sheets), printable + GoodNotes | PDF ~30 pp | $9.99 | to build (reuse `build_pdfs.py`) |
| 5 | Night Shift Sleep & Recovery Tracker printable | PDF 4 pp | $4.99 | pages 5-6 of product 2 can seed it |
| 6 | New Grad RN First-90-Days Planner | PDF ~20 pp | $8.99 | to build |
| 7 | Caregiver Binder for Elderly Parent (meds, appointments, daily log) | PDF ~25 pp | $8.99 | to build |
| 8 | Shift Worker Budget & Overtime Tracker | PDF + Google Sheet | $6.99 | to build |
| 9 | 50 extra 12-hour Brain Sheets refill pack | PDF 50 pp | $5.99 | to build |
| 10 | **Shiftwise Nurse Bundle** (1+2+4+5+6+9) | ZIP/PDF links | $24.99 (~45% off $45.93 sum) | after 1-6 exist |

Ladder: $4.99 tracker (entry, review-getter) -> $7.99-$9.99 printable packs -> $14.99 hyperlinked planner -> $24.99 bundle. Upsells: yearly "dated 2027/2028" edition of #1 (+$4), refill packs, "add Pet/Caregiver pack for $3" message in the delivery note. Every file includes a page linking to the shop (permitted as a thank-you; check Etsy rules on external links in files before use).

**Design system (original):** palette deep teal ink #12343B, warm sand #F7F3EC, sage #7FB7A4, mist #E3EFEA, single coral accent #E4572E; Helvetica family; crescent-moon motif for the nurse line, paw motif for pets; rounded cards, hairline rules, coral = "active/next". Same right-hand 7-tab navigation on every digital page. Everything is generated by `products/build_pdfs.py`, so a new product reuses tokens and components.

## 4. Competitor teardown (real shops/products found; figures [snippet] unless noted)
| Competitor | Product / price seen | Strengths | Weaknesses | Our edge |
|---|---|---|---|---|
| ScrubNotes (Etsy) | Nursing school study guides/templates; 19,464 sales, 4.8 (1,252 reviews) | Trust, volume | Study content, not shift-life planning | Planner + recovery/pay/licence angle, hyperlinked |
| NurseInTheMaking (Etsy) | Guides $2-$128; 234.9K sales, 4.9 | Brand, breadth | Study-guide focus | We are not competing on study content |
| Clinical Shift Starter Kit (Gumroad, fowziee) | Printable: dosage cheat sheet, 12-hr time-block, lab chart; price not retrieved | Clinically oriented | Static printable; reference tables carry accuracy liability | Interactive iPad version; no dosing tables (liability) |
| Nurse Shift Planner 10-page (Payhip) | Student/RN 10 pp: assignments, meds, handoff | Matches need | Printable only, plain design | Digital + printable + A4/Letter, consistent design |
| PlanMindco (Etsy, ADHD) | 2,477 sales, 4.8 (185 reviews) | Proves digital ADHD planner demand | Different niche | Possible later cross-sell |
| DailyFocusClub (Etsy, ADHD) | 2,377 sales, 4.7 (227) | Same | | |
| ADHDplanner (Etsy) | 1,030 sales, 4.7 (111) | Same | | |
| ADHD Digital Planner listings | $3.40-$14.61 (discounted), bundle with 700+ pages and 8000+ stickers at $14.61 | Page-count marketing; discounts | Race to the bottom on price | Do not compete on price; compete on fit |
| Growfully Studio (Etsy) | 18-page planner in A4/A5/Letter | Multi-size delivery | Generic | We already ship A4 + Letter |
| Pet care printables (Etsy) | $1.25 (20+ pp), $7.22 dog planner, $14 (33-page binder, 30% off) | Cheap, many | Wide price spread, little brand | Cohesive design, sitter page, A4+Letter |
| Caregiver binders (Etsy) | $0.99-$9.99 | Meets need | Price floor at $1 via 75% sales | Clear design, fillable focus |

Price anchors: ADHD digital planners $3-$15; ADHD daily planner median $5.73 (range $0.99-$29.98) [snippet]. We price at $7-$15 and accept slower volume; Etsy shows "sale" strikethrough prices so we plan promos (see pricing).

## 5. Keywords / SEO
How found: RankHero keyword pages for volume/competition (cited), search-result product titles for phrasing, and Etsy-seller guides. **All volumes below are tool estimates; confirm in Etsy search autocomplete and eRank/Marmalead free tiers in week 1.**

| # | Term | Data |
|---|---|---|
| 1 | digital planner | ~27,100/mo; 693,616 listings; KD 58 [RankHero, estimate] |
| 2 | digital planner goodnotes | ~320/mo; KD 70 [RankHero] |
| 3 | digital planner pdf | ~480/mo [RankHero] |
| 4 | goodnotes | 368k/mo global; 140,326 listings [RankHero] |
| 5 | monthly planner | ~27,100/mo [RankHero] |
| 6 | digital life planner | ~140/mo [RankHero] |
| 7 | nurse planner | from search phrasing; untested |
| 8 | nurse shift planner | search phrasing; untested |
| 9 | nursing student planner | search phrasing; untested |
| 10 | 12 hour shift planner | search phrasing; untested |
| 11 | night shift planner | untested |
| 12 | nurse brain sheet printable | untested |
| 13 | nurse report sheet | untested |
| 14 | clinical day planner | untested |
| 15 | new grad nurse gift | gift intent; untested |
| 16 | shift work calendar | search phrasing; untested |
| 17 | rotating shift schedule printable | untested |
| 18 | undated digital planner | untested |
| 19 | hyperlinked planner ipad | untested |
| 20 | notability planner | untested |
| 21 | pet care binder printable | seen in listings |
| 22 | dog care planner printable | seen in listings |
| 23 | pet sitter instructions printable | seen in guides |
| 24 | caregiver binder printable | seen in listings |
| 25 | medication tracker printable | untested |
| 26 | A4 planner printable | untested |
| 27 | US letter planner printable | untested |
| 28 | sleep tracker printable | untested |

**Title template (140 chars max, front-load buyer words):** `[Product] for [Audience] | [Format/App] | [Size/Undated] | [Benefit or use]`
**Tag template (13, <=20 chars each):** 2 exact audience terms, 2 product terms, 2 app/format terms, 2 size terms, 2 gift/occasion, 3 long-tail variants.
**Description template:** line 1 benefit + audience; "What you get" bullets; "How it works" (3 steps); sizes/compatibility; "Not included/disclaimers"; FAQ; license ("personal use"); AI/design disclosure line.

## 6. Pricing and unit economics
Etsy: $0.20 listing (renews every 4 months or on sale), 6.5% transaction, 3% + $0.25 US payment processing [verified via fee guides: [checkoutpage](https://checkoutpage.com/blog/etsy-fees)]. Offsite Ads 15% if <$10k/yr (optional opt-out), 12% above and mandatory, capped $100/order [same]. Etsy collects/remits VAT/GST on digital downloads in the EU, UK and other regions [blog-claim, [outfy](https://www.outfy.com/blog/etsy-sales-tax-explained/)]; sellers still owe income tax.

| Product | Price | Fees (no ads) | Net | Net % | Net with 15% offsite ad |
|---|---|---|---|---|---|
| Digital planner | $14.99 | 0.20+0.97+0.70 = $1.87 | $13.12 | 88% | $10.87 |
| Printable pack | $7.99 | 0.20+0.52+0.49 = $1.21 | $6.78 | 85% | $5.58 |
| Tracker | $4.99 | 0.20+0.32+0.40 = $0.92 | $4.07 | 82% | $3.32 |
| Bundle | $24.99 | 0.20+1.62+1.00 = $2.82 | $22.17 | 89% | $18.42 |

(Listing fee is counted once per sale here, which overstates cost for items that sell more than once per 4 months.) COGS = $0; cost is time. Payment processing fee is approximate and varies by country/currency.
Pricing tactics: list at full price, run planned 20-30% sales (Etsy sale tool) at launch and seasons; bundle discount ~45%; never go below $4.99 to protect perceived value.

## 7. Revenue model (gross, monthly) [estimate]
Orders = listings x avg visits per listing x conversion. Visits include Etsy search + Pinterest. Benchmarks: Etsy average conversion 1-3%, new shops 0.5-1.5%, growing 1.5-3% [blog-claim, [merchize](https://merchize.com/what-is-a-good-conversion-rate-on-etsy/)]. Reality check: one Indie Hackers seller reported 738 planners over <10 months for about GBP 3,453 revenue [blog-claim, [source](https://www.indiehackers.com/post/how-i-made-7500-income-in-less-than-10-months-from-a-digital-planners-spending-less-than-2-hrs-a-week-792f3939a5)]; top sellers claiming 200-500 planner sales/month are outliers [blog-claim].

| Scenario | Month | Listings | Visits/listing/mo | Conv. | Orders | AOV | Gross |
|---|---|---|---|---|---|---|---|
| Conservative | 1 | 10 | 5 | 0.3% | 0 | - | ~$0 |
| | 3 | 15 | 25 | 0.5% | 2 | $8 | $15 |
| | 6 | 30 | 40 | 0.7% | 8 | $8 | $67 |
| | 12 | 55 | 80 | 0.7% | 31 | $9 | $280 |
| Base | 1 | 10 | 20 | 0.5% | 1 | $9 | $9 |
| | 3 | 20 | 50 | 1.0% | 10 | $9 | $90 |
| | 6 | 35 | 90 | 1.5% | 47 | $10 | $470 |
| | 12 | 55 | 140 | 1.8% | 139 | $11 | $1,525 |
| Optimistic | 1 | 12 | 40 | 1.0% | 5 | $10 | $50 |
| | 3 | 25 | 120 | 1.5% | 45 | $10 | $450 |
| | 6 | 45 | 250 | 2.2% | 248 | $11 | $2,700 |
| | 12 | 70 | 400 | 2.5% | 700 | $12 | $8,400 |

Net after fees about 82-89%, minus ads if used. Honest read: the base case is side-income of about $1.5k/month after a year of consistent work; the optimistic case needs a breakout bundle and Pinterest traction. The conservative case may never repay time spent; see kill criteria.

## 8. Startup cost and time
- Etsy: no subscription; $0.20 per listing; 10 listings = $2. Optional Etsy Plus $10/mo not needed. [verified for fees]
- Python/reportlab: free. Canva free tier or Figma free for mockups; GoodNotes (free tier limited, paid ~ one-time or annual: check current price), a stock-free approach avoids licence cost. Mockups: free Canva/Figma-built or screenshots from the real PDFs.
- Domain/Payhip optional: $0-$12/mo. Realistic cash cost to start: **$0-$40**.
- Time: ~10-12 h/week for 12 weeks (see calendar), ~5-6 h/week maintenance after.

## 9. 90-day launch calendar
| Week | Focus | Hours |
|---|---|---|
| 1 | Validate: Etsy autocomplete + search for 28 keywords; note top-20 listing prices/sales; set up Etsy shop (human: ID verification, bank), name, policies; open Pinterest business account | 10 |
| 2 | Polish products 1-3 (open PDFs in GoodNotes/Notability and on iPad: test every tab link); make 5 mockups each; publish listings 1-3 | 12 |
| 3 | Build + publish #4 and #5; first 10 Pinterest pins | 12 |
| 4 | Publish #6; ask friends/nurse contacts for honest first reviews (no incentives that break Etsy rules); review stats | 10 |
| 5 | Build #7, #8; 10 pins/week | 12 |
| 6 | Publish #7, #8; tune titles/tags of the 3 best-viewed listings | 10 |
| 7 | Build #9 refill pack; Nurse Bundle (#10) mockups | 12 |
| 8 | Publish #9 and #10; launch sale (20%) for nurse bundle; seasonal angle: nursing school start (Jan) and "new year planner" | 10 |
| 9 | Variants: second colourway or dated 2027 edition of #1; A5 sizes | 10 |
| 10 | Pet/caregiver expansion: 2 more listings; Pinterest 15 pins/week | 10 |
| 11 | Kill/keep review per listing (see criteria); rewrite low-CTR thumbnails | 8 |
| 12 | Plan next 10 products from what sold; consider Payhip store for email list | 8 |

## 10. Traffic plan
- **Etsy SEO:** keyword-rich titles, all 13 tags, 10 images/listing, a short video, renewals and consistent new listings; shop sections by persona.
- **Pinterest:** Pinterest is a visual search engine and a known driver of planner/printable traffic [blog-claim, [Ecommerce Fastlane](https://ecommercefastlane.com/how-to-use-pinterest-for-etsy-a-practical-guide-for-2026/)]. Plan 10-15 pins/week using real page screenshots; board names that match keywords; use Rich Pins.
- Free lead magnet: 1-page brain sheet via Payhip/email to build a list (optional).
- Etsy Ads: test $1-2/day only after a listing shows >2% conversion.
- Communities (nursing subreddits, TikTok/Instagram nurse creators): follow each community's self-promotion rules; do not spam.

## 11. Risks, rules, kill criteria
- **Etsy Creativity Standards / AI:** items must be "Made by", "Designed by", etc.; AI involvement must be disclosed; in June 2025 Etsy removed an allowance for templated designs, so designs must originate with the seller [blog-claim, [Listadum](https://www.listadum.com/blog/etsy-creativity-standards)]. Our files are scripted by us from our own design system with AI assistance in code and copy: tick "Designed by seller" and disclose AI help in the listing. Re-read the current policy before publishing.
- **Medical/privacy:** never include dosing, lab-value or clinical reference tables (accuracy/liability); keep the "no patient identifiers" warnings; add "not medical advice". Do not use hospital logos or brand names (e.g. "Epic", "Happy Planner" as keywords can trigger IP complaints).
- **IP:** no trademarked terms in titles/tags (check "Notion", "GoodNotes" - app names are commonly used descriptively for compatibility, but keep it factual: "compatible with"); fonts are built-in Helvetica (no licence issue); mockup assets must be our own or properly licensed.
- **Saturation/price war:** differentiate by niche fit, not price.
- **Technical:** GoodNotes links only work with writing mode off (explained in listing); test on real devices; some apps handle links differently.
- **Dependency:** Etsy fee/policy changes, suspension risk; keep source files and an email list.
- **Kill criteria:** after 90 days, if total views < 1,500 or conversion < 0.5% on listings with >100 visits each, rework thumbnails/titles once. After 6 months, if gross < $100/month with >=30 listings, stop building new Etsy listings in this niche and pivot to the pet/caregiver pair or another business in the lab. Stop any paid ads that don't return 1.5x spend after $30.
