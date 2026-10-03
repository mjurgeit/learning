"""End-to-end demo: PDF + listing + mockups + revenue scenario. Run: python examples/demo.py [outdir]"""
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from labkit.pdf_design import Theme, PDFBuilder
from labkit import listing, mockup, revenue

out = sys.argv[1] if len(sys.argv) > 1 else "demo_out"
os.makedirs(out, exist_ok=True)
b = PDFBuilder(f"{out}/budget_planner.pdf", Theme.named("sage"), title="Weekly Budget Planner", footer="Demo Shop")
b.cover("Weekly Budget Planner", "US Letter - Printable PDF", "Plan every paycheck")
b.new_page("Start Here")
b.paragraph(48, 700, "Print these pages or fill them in on a tablet. Tap a link to jump around.", 500)
b.link(48, 650, "Visit our shop", "https://example.com")
b.checklist_page("Bills to pay", ["Rent", "Power"])
b.table_page("Budget", ["Category", "Planned", "Actual"])
b.weekly_page("Week of ____")
b.lined_page("Notes")
b.save()
res = listing.generate(json.load(open(os.path.join(os.path.dirname(__file__), "budget_planner.json"))))
print(res["title"], len(res["title"]), res["tags"], res["errors"])
print(mockup.build_set(f"{out}/mockups", "Weekly Budget Planner", "Printable PDF", ["12 pages", "US Letter + A4", "Clickable contents"],
                       ["Buy and download", "Open the PDF", "Print or fill on tablet"]))
print(revenue.compare(12.0)[:3])
