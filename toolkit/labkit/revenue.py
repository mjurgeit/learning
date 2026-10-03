"""Revenue-model calculator: platform fees + traffic/conversion scenarios.

Fee table = published rates as researched on 2026-10-03 (see research/02-playbook.md for tags).
Rates change: edit PLATFORMS or pass --override. Not tax or accounting advice.

CLI:
  python -m labkit.revenue fees --price 12
  python -m labkit.revenue compare --price 12
  python -m labkit.revenue scenario --platform etsy --price 9 --listings 20
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class Platform:
    key: str
    name: str
    pct: float = 0.0          # % of price taken by platform (commission/transaction)
    fixed: float = 0.0        # fixed $ per order (platform)
    proc_pct: float = 0.0     # payment processing %
    proc_fixed: float = 0.0   # payment processing fixed $
    listing_fee: float = 0.0  # per listing (Etsy $0.20 per listing, once per sale for digital: relisted automatically)
    ads_pct: float = 0.0      # extra % when sale comes via platform ad (Etsy Offsite Ads)
    note: str = ""


PLATFORMS: dict[str, Platform] = {p.key: p for p in [
    Platform("etsy", "Etsy (US shop)", pct=6.5, proc_pct=3.0, proc_fixed=0.25, listing_fee=0.20,
             note="Offsite Ads 15% (12% over $10k/yr, mandatory), capped $100/order. No VAT/regulatory fee for US shops."),
    Platform("etsy_offsite", "Etsy via Offsite Ad (15%)", pct=6.5, proc_pct=3.0, proc_fixed=0.25, listing_fee=0.20, ads_pct=15.0),
    Platform("gumroad", "Gumroad direct", pct=10.0, fixed=0.50, note="Merchant of record since 2025; Discover sales 30%."),
    Platform("gumroad_discover", "Gumroad Discover", pct=30.0, note="Flat 30% on Discover-originated sales."),
    Platform("payhip_free", "Payhip Free + Stripe", pct=5.0, proc_pct=2.9, proc_fixed=0.30,
             note="Payhip handles EU/UK VAT; US/CA sales tax handling changes from 2026-07-01 - verify."),
    Platform("payhip_plus", "Payhip Plus ($29/mo) + Stripe", pct=2.0, proc_pct=2.9, proc_fixed=0.30),
    Platform("stripe_direct", "Own store + Stripe only", proc_pct=2.9, proc_fixed=0.30,
             note="You are seller of record: VAT/sales-tax registration is yours (Stripe Tax helps, costs extra)."),
    Platform("tpt_basic", "TPT Basic seller", pct=45.0, fixed=0.30, note="blog-claim: 55% payout + $0.30"),
    Platform("tpt_premium", "TPT Premium ($59.95/yr)", pct=20.0, fixed=0.15, note="blog-claim: 80% payout; $0.15 only if order < $3"),
]}


@dataclass
class FeeResult:
    platform: str
    price: float
    fees: float
    net: float
    margin_pct: float


def fee_for(platform: str, price: float, platforms: dict[str, Platform] = PLATFORMS) -> FeeResult:
    p = platforms[platform]
    fixed = p.fixed
    if platform == "tpt_premium" and price >= 3:
        fixed = 0.0
    ads_fee = min(price * p.ads_pct / 100.0, 100.0)  # Etsy caps Offsite Ads fee at $100/order
    fees = price * (p.pct + p.proc_pct) / 100.0 + ads_fee + fixed + p.proc_fixed + p.listing_fee
    fees = round(fees, 4)
    net = round(price - fees, 4)
    return FeeResult(p.key, price, fees, net, round(100 * net / price, 2) if price else 0.0)


def compare(price: float) -> list[FeeResult]:
    return sorted((fee_for(k, price) for k in PLATFORMS), key=lambda r: -r.net)


@dataclass
class Scenario:
    name: str
    listings: int
    views_per_listing_month: float
    conversion_pct: float
    price: float
    ramp_months: int = 6      # linear ramp of traffic to full over this many months
    ads_spend_month: float = 0.0
    fixed_costs_month: float = 0.0


def project(s: Scenario, platform: str = "etsy", months: int = 12, orders_per_sale: float = 1.0) -> list[dict]:
    """Monthly projection. Traffic ramps linearly to its steady state over ramp_months (an estimate model)."""
    fr = fee_for(platform, s.price)
    rows, cum = [], 0.0
    for m in range(1, months + 1):
        ramp = min(1.0, m / s.ramp_months) if s.ramp_months else 1.0
        views = s.listings * s.views_per_listing_month * ramp
        orders = views * s.conversion_pct / 100.0 * orders_per_sale
        gross = orders * s.price
        fees = orders * fr.fees
        profit = gross - fees - s.ads_spend_month - s.fixed_costs_month
        cum += profit
        rows.append({"month": m, "views": round(views), "orders": round(orders, 1), "gross": round(gross, 2),
                     "fees": round(fees, 2), "profit": round(profit, 2), "cumulative": round(cum, 2)})
    return rows


def default_scenarios(price: float, listings: int) -> list[Scenario]:
    """Illustrative [estimate] scenarios; replace with your own measured data as soon as you have it."""
    return [
        Scenario("conservative", listings, 20, 0.8, price, 8),
        Scenario("base", listings, 60, 1.5, price, 6),
        Scenario("optimistic", listings, 150, 2.5, price, 4),
    ]


def breakeven_orders(platform: str, price: float, fixed_month: float) -> float:
    n = fee_for(platform, price).net
    return float("inf") if n <= 0 else fixed_month / n


def ads_breakeven_roas(platform: str, price: float) -> float:
    """ROAS (revenue / ad spend) at which an ad-driven sale makes zero profit: price / net."""
    n = fee_for(platform, price).net
    return float("inf") if n <= 0 else price / n


def _table(rows: list[dict]) -> str:
    if not rows:
        return ""
    cols = list(rows[0])
    w = {c: max(len(c), *(len(str(r[c])) for r in rows)) for c in cols}
    out = ["  ".join(c.rjust(w[c]) for c in cols)]
    out += ["  ".join(str(r[c]).rjust(w[c]) for c in cols) for r in rows]
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="labkit.revenue", description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fees"); f.add_argument("--price", type=float, required=True); f.add_argument("--platform", default="etsy")
    c = sub.add_parser("compare"); c.add_argument("--price", type=float, required=True)
    s = sub.add_parser("scenario")
    s.add_argument("--platform", default="etsy"); s.add_argument("--price", type=float, required=True)
    s.add_argument("--listings", type=int, default=20); s.add_argument("--months", type=int, default=12)
    s.add_argument("--ads", type=float, default=0.0, help="ad spend per month"); s.add_argument("--fixed", type=float, default=0.0)
    s.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.cmd == "fees":
        r = fee_for(a.platform, a.price)
        print(json.dumps(asdict(r), indent=2))
        print(f"ad break-even ROAS: {ads_breakeven_roas(a.platform, a.price):.2f}")
    elif a.cmd == "compare":
        print(_table([{"platform": r.platform, "fees": f"{r.fees:.2f}", "net": f"{r.net:.2f}", "margin%": r.margin_pct} for r in compare(a.price)]))
    else:
        out = {}
        for sc in default_scenarios(a.price, a.listings):
            sc.ads_spend_month, sc.fixed_costs_month = a.ads, a.fixed
            out[sc.name] = project(sc, a.platform, a.months)
        if a.json:
            print(json.dumps(out, indent=2))
        else:
            for name, rows in out.items():
                print(f"\n== {name} ({a.platform}, ${a.price}, {a.listings} listings) [estimate] ==")
                print(_table([r for r in rows if r["month"] in (1, 3, 6, 12)]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
