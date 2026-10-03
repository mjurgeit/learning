# 06 - Seller Economics: what does a typical NEW seller actually earn?

_Date: 2026-10-03. Purpose: decide whether the effort is justified. Skeptical stance._

**Method limits (read first).** WebFetch was blocked by the network proxy for sec.gov, etsy.com, writtenwordmedia.com, selfpublishingadvice.org, marketplacepulse.com and others. Every figure below therefore comes from **search-result snippets**, not from reading the full page. Where a snippet quoted a primary document (Etsy 10-K), I tag it [primary-via-snippet]. Nothing here was invented; gaps say "not found".

Tags: [primary] = company filing, [survey] = survey/academic, [blog-claim] = blog/aggregator, [estimate] = my arithmetic.

## 1. Etsy: primary data and what it implies

| Item | Value | Tag / URL |
|---|---|---|
| Marketplace GMS 2025 | $10,460.7M | [primary-via-snippet] https://www.sec.gov/Archives/edgar/data/1370637/000137063726000019/etsy-20251231.htm |
| Marketplace active sellers, 31 Dec 2025 | 5.6M (down 1.5% YoY) | [primary-via-snippet] same 10-K; also https://www.barchart.com/story/news/300269/etsy-inc-reports-fourth-quarter-and-full-year-2025-results |
| Active buyers | 86.5M (down 3.4% YoY) | same |
| "Active seller" definition | Seller with a charge or sale in the last 12 months (broadened in Q3 2021 to any sale) | [primary-via-snippet] Etsy 10-K filings list, e.g. https://www.sec.gov/Archives/edgar/data/1370637/000137063725000017/etsy-20241231.htm |
| Marketplace revenue 2025 | $2,007.2M (down 0.7%) | [primary-via-snippet] https://www.sec.gov/Archives/edgar/data/1370637/000137063726000019/etsy-20251231.htm |
| Consolidated take rate 2025 | 24.2% (22.3% in 2024); consolidated revenue $2,883.5M | [primary-via-snippet] same |
| Digital share of GMS | **Not found** in primary data. A blog claims digital downloads are the most-sold item type, "$1.9B+ annually" (unverified) | [blog-claim] https://www.insightagent.app/guides/most-sold-items-etsy |
| New-seller counts / first-sale rate (current) | **Not found** in 10-K snippets | - |

**Key survivorship point:** "active sellers" counts only people who made at least one sale in the past 12 months. Shops that never sold are excluded from the denominator, so every Etsy per-seller average below is an average over *survivors*. The true per-new-shop average is lower.

### Computed (all [estimate])
- GMS per active seller = 10,460.7M / 5.6M = **~$1,868/yr = ~$156/month** gross sales (all categories, mostly physical).
- Marketplace-only take rate = 2,007.2 / 10,460.7 = **~19.2%** (the 24.2% headline includes Depop/Reverb GMS in the denominator: 2,883.5 / 11,916.9 = 24.2%, which reconciles). Revenue includes ads and payment fees, so this is Etsy's all-in cut of a typical dollar.
- Mean seller keeps about $1,868 x (1 - 0.192) = **~$1,510/yr (~$126/month)** before COGS, shipping, own ad spend and taxes. For digital goods COGS is near zero, but the mean here is dominated by physical-goods sellers.
- Mean is a ceiling for a "typical" seller. In power-law marketplaces the median is far below the mean. Etsy does not publish a median (**not found**). Comparable data: Gumroad median $72/mo vs. 1% of creators capturing 99.5% of revenue (section 4). If Etsy's median is 15-30% of its mean (my assumption, [estimate]), the median active seller grosses **~$25-50/month**. Blog claims of "median £100-250/month" (https://www.listifyai.net/blog/how-much-do-etsy-sellers-make-2026) and "$574/month" (marmalead blog) are unsourced and disagree with this arithmetic by 3-10x; treat as optimistic [blog-claim].
- Trend: active sellers and buyers both shrinking, GMS flat (Q4 2025 GMS $3,292.9M, +0.1% YoY). Not a growth tailwind. https://www.ecommercebytes.com/2026/02/20/etsy-marketplace-shows-flat-growth-in-gms-in-4th-quarter-of-2025/

### Etsy distribution evidence (old but primary-ish)
- Etsy's own 2012 seller survey (94,000 US sellers with >=1 sale sampled, Nov 2012): 74% call the shop a "business", including **65% of those who made under $100 last year**; median *household* income $44,900; 26% under $25k household income. [survey, Etsy-run, via search snippet] https://extfiles.etsy.com/Press/reports/Etsy_RedefiningEntrepreneurshipReport_2013.pdf ; critique: https://www.slate.com/blogs/xx_factor/2013/11/08/etsy_economic_impact_report_etsy_crafters_generate_895_million_in_annual.html . The fact that a headline figure had to be about household income, and that a large block earned <$100/yr, is itself disconfirming.
- Share earning under $100/month or year in 2026 blogs ("over half under $100/month") [blog-claim], no primary source found.

### First sale
- 2017: of ~500,000 new Etsy sellers analysed by Marketplace Pulse, **31% had made at least one sale**; 61% still had listings; of those with a sale, 35% sold in the last 30 days. [blog/analyst, secondary, via snippet] https://www.marketplacepulse.com/articles/etsy-has-already-added-500000-sellers-in-2017 (Could not open page; method unverified. 2017 data, pre-AI-flood.)
- Time to first sale: **no systematic data found**. Only anecdotes in Etsy forum threads ("days to months") [blog-claim] https://community.etsy.com/t5/Creative-Biz-Talk/How-did-you-make-your-first-sale/m-p/125435888
- So roughly **~69% of new shops never sell** (2017, [estimate] from the 31% figure).

## 2. Amazon KDP / self-publishing (surveys, heavily biased toward serious authors)

- Written Word Media 2025 indie author survey: ~44% earn <=$100/month; ~20% earn $500-5,000/month; ~13% >$5,000/month; ~8% >$10,000/month. Analysts note it skews to prolific authors who buy marketing services. [survey, via snippet] https://www.writtenwordmedia.com/2025-author-survey/amp/ ; commentary https://www.vappingo.com/word-blog/kdp-income-reports/
- ALLi Indie Author Income Survey 2023: median $12,759 (2022 income), but sample limited to authors who spent >=50% of work time on writing/publishing; mean >$80,000; almost a quarter earned $0-1K. [survey, heavily self-selected] https://thebookseller.com/news/self-published-authors-earn-more-than-traditionally-published-counterparts-according-to-alli-report
- Pooled claim across 2022-25 surveys: ~40% of published authors earn <$500/yr, 2-3% earn >$100k/yr. [blog-claim, aggregator] https://www.vappingo.com/word-blog/how-much-do-kdp-authors-earn/
- Not found: KDP low-content/journal-specific earnings distribution; hours per book.

## 3. Teachers Pay Teachers
- ~1% of sellers earn >=$100k/yr; ~half earn under $20/month; top 1% = 81% of sales. [blog-claim, repeated by many sites, no primary found] https://wealthvieu.com/salaries/profession-salary-guides/teachers-pay-teachers/ ; ref in 01 report: https://trtc.io/blog/details/Teachers-Pay-Teachers
- Peer-reviewed analysis of TPT transactions exists (Koehler et al. 2020, "Where does all the money go? Free and paid transactions on TeachersPayTeachers.com") but the page was blocked; I could not extract its numbers. https://spencergreenhalgh.com/research/2020-koehler-et-al-tpt/
- New seller trajectory "$0-50/mo in months 3-6, $100-500/mo after 12-18 months": [blog-claim], unsourced.

## 4. Gumroad / Payhip
- Gumroad analysis of ~146,000 active products (2024-26, third-party site): median creator ~$72/month gross (another source $84), ~$62 after the 13.2% effective fee; <5% of creators gross >$1,000/month; 44% of products earned exactly $0; top 1% of creators earn >=$10k/month and capture 99.5% of revenue. [blog-claim, third-party scrape, methodology unverified] https://profitable.app/gumroad/stats
- Payhip: **not found** (no distribution data).

## 5. Disconfirming evidence / survivorship checklist
- Public income reports (YouTube, Medium, "how I made $10k/mo") come from winners, often selling the course. Treat as upper tail.
- Etsy per-seller GMS excludes zero-sale shops and includes physical goods and long-tenured pros.
- ALLi and Written Word Media respondents are engaged, prolific authors; non-respondents (one-book dabblers) are missing.
- Etsy active sellers falling and buyers falling: more competition per buyer.
- No source found separating *digital* seller earnings from overall Etsy.
- Reported hours: Etsy sellers average ~12 hrs/week, top sellers ~33 hrs/week, serious (>=20% of income) ~28 hrs/week [blog-claim citing survey, unverified] https://blog.marmalead.com/how-much-can-you-make-on-etsy-in-2023/

## 6. Summary table

| Platform | Metric | Value | Source | Reliability |
|---|---|---|---|---|
| Etsy | Marketplace GMS 2025 | $10.46B | SEC 10-K FY2025 | High (primary) |
| Etsy | Active sellers (>=1 sale in 12 mo) | 5.6M, -1.5% YoY | SEC 10-K FY2025 | High (primary) |
| Etsy | GMS per active seller | ~$1,868/yr (~$156/mo) | derived from above | Medium ([estimate], survivor-only mean) |
| Etsy | Marketplace take (revenue/GMS) | ~19.2% (24.2% consolidated) | derived from 10-K | Medium-high |
| Etsy | Median active seller | not found; est. $25-50/mo gross | my assumption | Low |
| Etsy | % new shops with a sale | ~31% (2017) | Marketplace Pulse | Low-medium (old, secondary) |
| Etsy | Time to first sale | not found | - | - |
| Etsy | Sellers who made <$100 in a year calling it a business | 65% of that group | Etsy 2012 survey | Medium (old, Etsy-run) |
| Etsy | Hours/week typical | ~12 | blog citing survey | Low |
| KDP | Authors <=$100/mo | ~44% | Written Word Media 2025 | Medium (biased up) |
| KDP | Median income | $12,759 (full-time-ish authors) | ALLi 2023 | Medium (biased up heavily) |
| TPT | Half of sellers < $20/mo; top 1% = 81% of sales | | blog aggregators | Low |
| Gumroad | Median creator $72/mo; <5% over $1k/mo | | profitable.app | Low-medium |
| Payhip | any distribution | not found | - | - |

## 7. What the data says about expected hourly earnings for a new seller, months 1-12

Assumptions ([estimate]): 10 hours/week for 52 weeks = **520 hours** (consistent with ~12 hrs/wk reported average); digital product, near-zero COGS; Etsy all-in cut 19.2% (Etsy) or ~13% (Gumroad); pre-tax, ignoring ad spend and tools. Ranges are explicit scenarios, not forecasts.

| Case | Year-1 gross | Net after fees | Net / 520 h |
|---|---|---|---|
| **Expected value across all new shops (low)**: 31% ever sell; sellers who do make ~$300 gross -> 0.31 x $300 = $93 expected gross; net ~ $75 | ~$93 | ~$75 | **~$0.15/h** (69% of shops earn $0/h) |
| **Median surviving seller (mid)**: ~$40/mo x 12 = $480 gross (midpoint of the $25-50 estimate) | $480 | ~$390 | **~$0.75/h** |
| **Mean active seller (mid-high)**: $1,868 gross | $1,868 | ~$1,510 | **~$2.90/h** |
| **Top ~5% (high)**: reaches >$1,000/mo gross (Gumroad <5% threshold) for ~6 of 12 months -> $6,000 | $6,000 | ~$5,000 | **~$9.60/h** |

**Summary: low ~$0-0.20/h, mid ~$0.75-3/h, high ~$10/h** over months 1-12. Even the high case is below minimum wage and requires being in roughly the top 5%. Revenue typically lags: most listings take 3-6 months to rank, so month 1-3 is near $0 for nearly everyone.

**Break-even in hours:** if startup costs are ~$100 (tools, listing fees, mockups) and net is ~$0.75/h, break-even needs ~130 hours of *selling-phase* effort beyond build time, which a median seller never reaches in year 1; the mean seller recovers $100 in ~35 hours of equivalent output. Break-even probability for a new shop in year 1 is roughly the probability of making >$100 net: roughly the top third at best ([estimate], from 31% first-sale rate; true figure not found).

**Verdict for the lab:** the data do not support treating one new shop as a reliable income source in 12 months. They support (a) small portfolio bets with near-zero cash outlay, (b) treating the work as a skill/asset-building investment with payoff concentrated in the top few percent, and (c) strict kill criteria (see 02-playbook). Because Etsy's own survivor mean is only ~$156/mo gross, any plan that assumes much above that per shop in year 1 needs specific justification (niche proof, 50+ listings, outside traffic).

## 8. Not found (do not fill with guesses)
Etsy median seller income; digital share of Etsy GMS; current share of new Etsy shops with a first sale; time-to-first-sale distribution; Payhip distributions; KDP low-content income distribution; TPT primary numbers; academic study of Etsy seller hourly earnings.
