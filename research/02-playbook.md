# Cross-business playbook: how digital sellers win in 2026

_Date: 2026-10-03. Companion to `01-market-report.md`. Tools to execute this live in `/home/user/learning/toolkit`._

## Evidence tags and a candid caveat
- **[verified]** = the same fact appeared in 3+ independent sources and matches the platform's known published structure. **Etsy, KDP and Amazon help pages were blocked by the research environment's network proxy, so I could not read any primary policy page this session.** Re-check every fee and policy on the official page before relying on it (links in section 13).
- **[blog-claim]** = one or two seller/tool blogs (often selling software, so they skew optimistic).
- **[estimate]** = my own reasoning or arithmetic, not a measured fact.

Sources used (all via web search, 2026): Etsy fee guides (checkoutpage.com, craftybase, growingyourcraft, nifty.ai), Marmalead and RankHero Etsy-algorithm posts, Gelato/Outfy/Merchize photo-size guides, ListifyAI blogs (ads, seasonality, Google Trends), eRank/Marmalead pricing roundups (craftybase, profittree, outfy), Payhip pricing/MoR reviews (sellfy, dodopayments, fungies), Gumroad fee reviews (checkoutpage, dodopayments), Stripe/commenda VAT pages, Outfy and madeurban sales-tax explainers, ecommercebytes (Etsy VAT), valueaddedresource and beancount.io (Regulatory Operating Fee), Pinterest guides (growingyourcraft, printify, ecommercefastlane), KDP policy coverage (Publishers Weekly, The Bookseller, ebookpbook), Etsy creativity-standards coverage (getcoai, ecomcrew, aimetadatacleaner), Chalkbeat on TPT AI content, TPT fee pages, KDP royalty guides (cartmango, bestwriting), Etsy buyer-messaging rules (ecommercebytes, community.etsy.com).

## 1. The core thesis
1. Marketplace sellers win by **being matched** (keywords in title/tags/attributes), then **being chosen** (thumbnail click-through, price, reviews), then **converting** (gallery, description, instant delivery). Ranking feeds on the last two. [verified: every source describes a match-then-rank two-phase system]
2. Digital goods have ~85-95% margins before time, so the scarce resource is **traffic and trust**, not cost. [verified arithmetic, see section 8]
3. Saturation is real; sellers who win pick a **narrow audience + specific use case** and bundle, rather than generic "planner". [blog-claim, consistent across sources]
4. Own-store (Payhip/Stripe) only pays when you can supply the traffic (email, Pinterest, SEO). Start on marketplaces, build an email list, graduate winners. [estimate/strategy]

## 2. Etsy SEO and ranking
- Two phases: **query matching** (title, tags, categories, attributes, description are read) then **ranking** (relevancy, listing quality score, customer/service history, shipping price for US, recency, translations, personalised "context specific" ranking). [verified: Etsy's own framing as relayed by Craftybase, RankHero, Marmalead, eRank glossary]
- Listing quality score is driven by CTR, add-to-cart, favourites, purchases after impression. [verified, consistent]
- 2026 claims: dwell time, video and complete attributes help. [blog-claim: Marmalead/RankHero only; Etsy has not published weights]
- Limits: **title 140 chars, 13 tags, 20 chars per tag.** [verified, multiple sources; enforced in `toolkit/labkit/listing.py`]
- First ~40 characters of the title matter most (mobile truncation). [blog-claim]. Commas recommended over dashes. [blog-claim]. Multi-word tags beat single words; do not repeat the same phrase across tags; skip plurals. [blog-claim, consistent]
- Do not stuff titles; repeating a phrase wastes characters and may trigger detection. [blog-claim]
- Timing: a new listing needs weeks to gain signals; publish seasonal items **6-8 weeks** before the buyer-search peak. [blog-claim: ListifyAI; "38% of GMS in 8 weeks" is also a blog-claim, treat as unproven]
- Conversion: typical Etsy shop 1-3%, strong >3%. [blog-claim]

**Playbook:** research one buyer phrase per listing, put it first in title, mirror it in tag 1 and attributes; fill all 13 tags; first image = clear thumbnail; add video/more photos if time allows; refresh underperformers after 30 days (change thumbnail first, then title). [estimate/process]

## 3. Keyword and competitor research that stays within the rules
Free, legitimate methods:
1. **Etsy search-bar autocomplete**: type the seed + each letter a-z; note suggestions (reflects real searches). Manual. [verified practice, widely recommended]
2. **eRank free plan**: ~5 keyword searches and 5 listing audits per day, no competitor tracking; paid $5.99-$29.99/mo. [blog-claim, 2026 roundups agree]
3. **Marmalead**: no free tier, $19/mo ($15.83 annual), 14-day trial. [blog-claim, consistent]
4. **Pinterest Trends** (free): autocomplete plus trend curves and related terms; useful for what rises before it peaks on Etsy. [verified exists/free; usage tips blog]
5. **Google Trends** (free): multi-year seasonality to schedule launches. [blog-claim on tactics; tool itself verified]
6. Competitor research by **looking** (best-sellers, reviews, price bands, bundle sizes, review text for unmet complaints). Do not copy images, copy or file structure.
- **Do not scrape Etsy.** Automated access to the site/API outside the approved API is prohibited by Etsy's terms (secondary sources; confirm in Etsy's API terms). Third-party SEO tools should be used via their own UIs. Scrapers on Apify etc. exist but carry account/legal risk. [blog-claim: webscraping.ai; treat as a risk, not legal advice]
- Cross-check: keep a keyword only if (a) autocomplete shows it, (b) the first page shows live sales/reviews on similar items, (c) you can make a visibly better or more specific product.

## 4. Listing photos and mockups
- Etsy recommends images at least 2000 px on the shortest side, 4:3 ratio (3000x2250) or 1:1 (2000x2000 works); up to 10 images; JPG in sRGB, under ~1 MB; thumbnail crop around 570x456 (5:4). [blog-claim, 5+ sources consistent; confirm in Etsy Seller Handbook]
- For digital goods the mockup *is* the product. Winning gallery pattern: (1) bold thumbnail with headline + product preview + format badge, (2) what's included, (3) lifestyle/room mockup, (4) size/format info, (5) how it works (download steps), (6) print tips / editing proof, (7) shop trust (reviews, "instant download"). [blog-claim, consistent]
- State quantity, sizes, formats, software required, editable or not. Plain background, readable text on mobile. Thumbnail drives CTR (the "70%" figure is a blog-claim; treat as unproven). [blog-claim]
- Tool: `toolkit/labkit/mockup.py` (`build_set`) makes 5 gallery images from page renders. For realism, replace placeholder pages with real PDF renders and, optionally, licensed photo scenes you own.

## 5. Pricing and bundling
- Rough tiers: single printable $3-8 (to earn reviews), 3-5 item bundles $8-20 (sweet spot), 10+ item bundles/planners $20-50+. [blog-claim, consistent]
- Bundles: 3-packs at about 20-23% off singles; large bundles convert better because the buyer feels covered. [blog-claim]
- Do not race to the bottom: Etsy takes ~$1.4 on a $10 sale regardless; ad-driven sales cost much more (section 7). [verified arithmetic]
- Ladder: low-price "lead" item -> mid bundle -> premium bundle/licence -> own-store membership. Use `labkit.revenue compare` to see what each platform leaves you.
- Test price changes one at a time for 2-4 weeks. [estimate]

## 6. Reviews and social proof
- Zero-review shops convert poorly; first reviews come from fast, honest delivery plus a polite post-purchase note inside the file ("Enjoyed it? A review helps a small shop"). [blog-claim]
- Ranking uses purchases and customer-service history; a listing with the same views and more sales ranks better. [blog-claim, consistent]
- Never buy/swap reviews or incentivise them in ways Etsy forbids. [estimate: policy risk, check Etsy rules]

## 7. Etsy Ads ROI
- Fees context: Offsite Ads cost **15%** of the order (12% once you pass $10k/yr, then mandatory), capped at $100 per order. [verified, 4+ sources]
- Onsite ads: start $1-5/day, only on listings that already convert; judge after ~30 days. [blog-claim, consistent]
- ROAS >3 is the usual "keep" threshold; but compute your own break-even: for a $10 Etsy sale net is $8.60, so break-even ROAS is 1.16 on onsite ad spend before time; with Offsite 15% it is much worse. `labkit.revenue fees --price 10` prints it. [estimate/arithmetic, tool-verified]
- Verdict: ads are a **multiplier on proven listings**, not a way to rescue weak ones. Budget cap in the first 90 days: $0-$90. [estimate]

## 8. Fees by platform (as of 2026-10-03)
| Platform | Rate | Tag |
|---|---|---|
| Etsy | $0.20 listing; 6.5% transaction; payment processing 3% + $0.25 (US); UK 4% + £0.20, many EU 4% + €0.30; 2.5% currency conversion; Offsite Ads 15%/12% cap $100 | [verified: many sources] |
| Etsy Regulatory Operating Fee | none for US shops; UK 0.48%, France 1.14%, Italy 0.80%, Spain 0.88%, Hungary 1.97%, Canada 1.15% etc. from 2026-06-22 | [blog-claim: valueaddedresource, beancount.io] |
| Gumroad | 10% + $0.50 on direct sales, 30% on Discover; merchant of record since Jan 2025 | [blog-claim, 4 sources agree] |
| Payhip | Free 5%, Plus $29/mo 2%, Pro $99/mo 0%, plus Stripe/PayPal ~2.9%+$0.30; collects EU/UK VAT; US/CA sales-tax handling announced from 2026-07-01 | [blog-claim] |
| Stripe direct | ~2.9% + $0.30; you are seller of record | [verified, widely published] |
| TPT | Basic: 55% payout + $0.30 per sale; Premium $59.95/yr: 80% payout, $0.15 only on orders under $3 | [blog-claim; one source conflicted, check TPT] |
| KDP | eBook 70% for $2.99-$12.99 (cap raised from $9.99 on 2026-07-07) minus $0.15/MB delivery; paperback 60% at >=$9.99 else 50%, minus print cost | [blog-claim, 4 sources] |

Margin per $12 digital sale (tool output): Stripe-direct $11.35 (94.6%), Payhip Free $10.75 (89.6%), Etsy $10.41 (86.8%), Gumroad $10.30, TPT Premium $9.60, Etsy via Offsite Ad $8.61 (71.8%), TPT Basic $6.30 (52.5%). [estimate from table above]

## 9. Pinterest traffic
- Pinterest behaves like a visual search engine; pins can rank for months/years (vs. hours on feeds). [blog-claim, consistent]
- Needs **fresh pins** (new image/layout per pin even for the same URL); steady posting beats bursts; use Pinterest Trends for keywords. [blog-claim, consistent]
- Practical plan: 3-5 fresh pin designs per listing, 1-3 pins/day via scheduler, keyword-rich titles/descriptions, board per niche. Expect a slow ramp: 2-3 months before meaningful clicks. [estimate]
- Pinterest traffic to Etsy is "cold" so conversion is usually lower than Etsy search; its main job is feeding your email list and your own store. [estimate]

## 10. Email list
- Average email ROI figures ($36-$42 per $1) and "2% digital product conversion" are vendor stats. [blog-claim; do not plan on them]
- **Etsy rules:** you may message buyers only about their active order; you may not add buyer emails to marketing lists without explicit consent; no unsolicited promotion. [blog-claim from community/ecommercebytes; read Etsy's current policy]
- Compliant approach: put an optional freebie/opt-in link *inside* the product PDF or on Pinterest and your own site; use double opt-in and a working unsubscribe (CAN-SPAM/GDPR). [estimate/legal-sense; consult a professional]
- Free tiers: use a provider with a free tier (check current limits) or Payhip's built-in email. [estimate]

## 11. Own-store checkout (Payhip / Stripe)
- **Payhip** = lowest effort: hosts files, collects EU/UK VAT, 5% on free plan. Break-even for Plus over Free is about $967/mo sales. [blog-claim, arithmetic]
- **Gumroad** = full merchant of record (handles global tax) at 10% + $0.50; simplest for tax, priciest. [blog-claim]
- **Stripe only** = cheapest but **you** own VAT/sales-tax registration and filing; Stripe Tax calculates but legal responsibility stays with you. [verified: Stripe docs/commenda]
- Rule: until you have steady traffic of your own (> ~500 visits/mo) the marketplace is cheaper per sale than your time. [estimate]

## 12. Taxes and VAT on digital goods (summary only; consult an accountant)
- Etsy collects and remits VAT on digital downloads to EU/UK (and other regions) buyers and US sales tax where it is marketplace facilitator; you still report your Etsy income yourself. [verified: Etsy help center content as relayed by 4+ sources]
- Etsy has Digital Services Tax pass-through ("Regulatory Operating Fee") in several non-US countries. [blog-claim]
- US states increasingly tax digital products/software (e.g., Utah expansion 2026-07-01; California/Colorado software/SaaS changes from 2027). Economic-nexus thresholds typically $100k or 200 transactions per state, some states dropped the 200 count. [blog-claim: dodopayments, taxcloud, anrok]
- Selling on your own store via Stripe means **you** may owe VAT/sales tax from the first sale in some jurisdictions (EU digital VAT has no small-seller threshold for non-EU sellers). [estimate, high-risk: ask an accountant]
- Action items: keep monthly records of platform payouts; track Etsy fees as expenses; get an accountant before launching own-store sales to EU/UK buyers or reaching ~$5k/yr.

## 13. AI-disclosure and content rules
| Platform | Rule | Tag |
|---|---|---|
| **Etsy** | Creativity Standards (introduced July 2024) allow AI-assisted designs as "Designed by a seller" but require disclosure: tick the AI checkbox in the listing form, choose the right production attribution, and say so in the description. Many listings were removed in 2025 for non-disclosure (figure "17,000+" is a blog-claim). Etsy also bans items you did not make/design or resell; stock-art, resale of PLR may be disallowed. | [blog-claim: several coverage pieces agree on the checkbox/labels; verify in Etsy Seller Policy] |
| **KDP** | Must tell KDP when text, images or translations are AI-**generated** (even if edited); AI-**assisted** (you wrote it, tool polished it) need not be disclosed. You are responsible for copyright/quality; low-quality/near-duplicate titles are removed. | [verified: Publishers Weekly, The Bookseller, several summaries agree] |
| **TPT** | I could not find a published seller-AI-disclosure rule in the sources I could reach; Chalkbeat (2026-08-03) reports AI "slop" with factual errors on the marketplace and complaints from teachers. Expect quality enforcement; disclose AI use anyway and fact-check everything. | [blog-claim/unknown: check TPT's seller policy] |
- The `toolkit` listing generator adds an AI disclosure paragraph when `ai_used: true` and fails validation if it is missing; always also tick the platform checkbox where it exists.
- General: do not copy competitors' designs, use trademarked characters/brands, or embed fonts/art whose licence forbids resale. Keep a licence log for every font, image and template element.

## 14. Do-this-first checklist (any business)
1. Pick a narrow persona + job-to-be-done; list 20 keyword phrases via autocomplete + Pinterest Trends; keep ones with live competitors.
2. Build the product with `labkit.pdf_design` (consistent palette, clickable TOC, terms page, shop link).
3. Generate title/tags/description with `labkit.listing`; fix all errors.
4. Generate the gallery with `labkit.mockup`; swap in real page renders.
5. Run `labkit.revenue compare/scenario` to set price and an honest 90-day expectation.
6. Launch 10-20 listings, no ads for 30 days; then ads on the top 3 only.
7. Pinterest 3-5 fresh pins/listing/month; opt-in freebie inside the PDF to start an email list.
8. Review monthly: kill listings with <100 views after 60 days after improving thumbnail+title once.
9. Talk to an accountant before own-store EU/UK sales or around $5k/yr.

## 15. What is still unverified
Etsy's real ranking weights (never published), actual conversion/revenue per niche (blogs only), TPT's AI rule and exact fees (conflicting secondary sources), Payhip's July-2026 sales-tax change details, current Etsy Offsite Ads thresholds. All primary pages (help.etsy.com, kdp.amazon.com, chalkbeat.org) were blocked this session; re-verify before committing money.
