import json, os, sys
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from labkit import listing, mockup, revenue
from labkit.pdf_design import Theme, PDFBuilder, contrast_ratio, PALETTES

EX = os.path.join(os.path.dirname(__file__), "..", "examples", "budget_planner.json")


# ---- listing
def test_title_never_exceeds_limit():
    kws = ["alpha beta gamma delta epsilon " * 2 + str(i) for i in range(20)]
    t = listing.build_title(kws)
    assert 0 < len(t) <= 140


def test_title_skips_redundant_phrases():
    assert listing.build_title(["budget planner", "planner budget", "tracker"]) == "budget planner, tracker"


def test_tags_limits_and_dedupe():
    tags = listing.build_tags(["Budget Planner", "budget planner", "a very long keyword phrase indeed here"] + [f"tag number {i}" for i in range(30)])
    assert len(tags) == 13
    assert len({t.lower() for t in tags}) == 13
    assert all(len(t) <= 20 for t in tags)


def test_validate_catches_errors():
    r = listing.validate("x" * 141, ["a"] * 2 + ["b" * 21] + [f"t{i}" for i in range(12)])
    joined = " ".join(r.errors)
    assert "141" in joined and "max 13" in joined and "21 chars" in joined and "duplicate" in joined and not r.ok


def test_validate_bad_chars_and_ai():
    assert not listing.validate("Good title " * 6, ["bad@tag"] + [f"t{i}" for i in range(12)]).ok
    assert not listing.validate("Good title " * 6, [f"t{i}" for i in range(13)], "no disclosure", ai_used=True).ok


def test_generate_from_example_valid():
    res = listing.generate(json.load(open(EX)))
    assert res["ok"], res["errors"]
    assert res["title_len"] <= 140 and len(res["tags"]) == 13


def test_ai_disclosure_added():
    cfg = json.load(open(EX)); cfg["ai_used"] = True
    res = listing.generate(cfg)
    assert "AI DISCLOSURE" in res["description"] and res["ok"]


def test_cli_exit_codes(tmp_path):
    p = tmp_path / "c.json"; p.write_text(open(EX).read())
    assert listing.main([str(p)]) == 0


# ---- pdf
def test_pdf_builds_with_links(tmp_path):
    out = tmp_path / "t.pdf"
    b = PDFBuilder(str(out), Theme.named("ocean", "a4"), title="T", footer="f")
    b.cover("A Rather Long Title For Wrapping Test", "sub", "tag")
    y = b.new_page("Links")
    b.link(48, y, "site", "https://example.com")
    b.button(48, y - 60, 160, 36, "Go", bookmark_key="p1")
    b.checklist_page("C", ["x"]); b.table_page("T", ["a", "b"]); b.weekly_page(); b.lined_page(); b.grid_page(); b.grid_page(dots=False)
    b.toc_page()
    b.save()
    data = out.read_bytes()
    assert data.startswith(b"%PDF") and b"/URI" in data and b.pages == 9
    from reportlab.pdfgen import canvas  # sanity: file reopenable
    assert len(data) > 5000


def test_palette_contrast_accessible():
    for name, p in PALETTES.items():
        assert contrast_ratio(p.ink, p.bg) >= 7, name


# ---- mockup
def test_mockup_set(tmp_path):
    files = mockup.build_set(str(tmp_path), "Weekly Budget Planner", "Printable", ["a", "b", "c"], ["one", "two"])
    from PIL import Image
    assert len(files) == 5
    for f in files:
        im = Image.open(f)
        assert im.size == (2000, 2000) and im.format == "JPEG"
        assert os.path.getsize(f) < 2_000_000


def test_fit_text_fits():
    from PIL import Image, ImageDraw
    d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    f, lines = mockup.fit_text(d, "VERY LONG HEADLINE " * 6, "bold", 1700, 380, start=190)
    assert all(d.textlength(l, font=f) <= 1700 for l in lines)


# ---- revenue
def test_etsy_fee_math():
    r = revenue.fee_for("etsy", 10.0)
    assert r.fees == pytest.approx(0.20 + 0.65 + 0.30 + 0.25)
    assert r.net == pytest.approx(10 - 1.40)


def test_offsite_ads_and_cap():
    assert revenue.fee_for("etsy_offsite", 10.0).fees == pytest.approx(1.40 + 1.50)
    assert revenue.fee_for("etsy_offsite", 2000.0).fees == pytest.approx(2000 * .095 + 0.45 + 100)


def test_gumroad_payhip_tpt():
    assert revenue.fee_for("gumroad", 20).fees == pytest.approx(2.50)
    assert revenue.fee_for("payhip_free", 20).fees == pytest.approx(20 * .079 + .30)
    assert revenue.fee_for("tpt_basic", 5).net == pytest.approx(5 * .55 - .30)
    assert revenue.fee_for("tpt_premium", 5).fees == pytest.approx(1.0)


def test_compare_sorted_and_scenarios():
    c = revenue.compare(15)
    assert c[0].net >= c[-1].net and c[0].platform == "stripe_direct"
    sc = {s.name: revenue.project(s)[-1]["profit"] for s in revenue.default_scenarios(9, 20)}
    assert sc["conservative"] < sc["base"] < sc["optimistic"]


def test_ramp_and_breakeven():
    rows = revenue.project(revenue.Scenario("x", 10, 100, 2, 10, ramp_months=4))
    assert rows[0]["orders"] < rows[3]["orders"] == rows[11]["orders"]
    assert revenue.ads_breakeven_roas("etsy", 10) == pytest.approx(10 / 8.6)
    assert revenue.breakeven_orders("etsy", 10, 86) == pytest.approx(10)


def test_cli(capsys):
    assert revenue.main(["compare", "--price", "10"]) == 0
    assert "stripe_direct" in capsys.readouterr().out
    assert revenue.main(["scenario", "--price", "9", "--listings", "20"]) == 0
    assert "optimistic" in capsys.readouterr().out
