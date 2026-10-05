#!/usr/bin/env python3
"""Demo: one mirrored RTL and one standard LTR document using most components.
Usage: python3 example.py [output_dir] [theme_rtl] [theme_en]"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pdfkit import Doc, mono, b, ul, tag

out = Path(sys.argv[1] if len(sys.argv) > 1 else "/mnt/user-data/outputs")
th_rtl = sys.argv[2] if len(sys.argv) > 2 else "ocean"
th_en = sys.argv[3] if len(sys.argv) > 3 else "executive"

# ------------------------------------------------------------------ RTL (mirrored layout) report
d = Doc(rtl=True, lang="ar", title="Quarterly report", theme=th_rtl)
d.cover("Q3 Performance Report", "Results, trends and next quarter plan", tag_line="Internal report · 2026",
        meta=[("Prepared by", "Analytics team"), ("Version", "1.0"), ("Date", "October 2026")])
d.hero("Executive summary", "Q3 results at a glance", "Everything important on one page")
d.lead("Sales grew compared to last quarter and customer satisfaction stayed above target. The main numbers and the next steps follow.")
d.stats([("1.2M", "Revenue (USD)", "▲ 14% vs last quarter"), ("92", "Satisfaction score"), ("3,400", "Active customers", "▲ 210")])
d.h2("Sales by region")
d.bars([("North", 480), ("East", 310), ("South", 240), ("West", 170)], colors=True)
d.h2("Financial table")
d.table(["#", "Item", "Q2", "Q3"],
        [["1", "Product sales", "820", "930"], ["2", "After-sales service", "180", "210"], ["3", "Total", "1,000", "1,140"]],
        widths=["10%", "50%", "20%", "20%"], align=["center", "start", "end", "end"], total_row=True)
d.note("Figures are in thousands of USD and before tax.", "warn", title="Note")
d.h2("Project timeline")
d.timeline([("Oct", "Kickoff", "Form the team and set goals"), ("Nov", "Pilot", "Run the pilot in two cities"),
            ("Dec", "Public launch", "Roll out to all regions")])
d.columns("<h3>Done</h3>" + ul(["Redesigned the home page", "Reduced response time"]),
          "<h3>Next</h3>" + ul(["Train the sales team", "Expand to two new cities"]))
d.quote("Quality means doing it right even when no one is looking.", "Management office")
d.checklist([("Budget approved", True), ("Contract signed", True), ("Final review", False)])
d.save(out / "pdf-atelier-example-rtl.pdf")

# ------------------------------------------------------------------ English / LTR proposal
e = Doc(rtl=False, title="Project proposal", theme=th_en)
e.hero("Proposal · 2026", "Customer Portal Redesign", "Scope, timeline and investment")
e.lead("We propose a three-phase redesign that shortens support requests by a third and gives customers one place for everything.")
e.stats([("−32%", "Support tickets", "target"), ("6 wks", "Delivery time"), ("$48k", "Fixed price")], colors=True)
e.h2("Phases")
e.numbered(1, "Discovery", ul(["Interview 12 customers", "Audit current portal"]), tags=["2 weeks"])
e.numbered(2, "Design", ul(["Wireframes and prototype", "Usability test"]), tags=["2 weeks"])
e.numbered(3, "Build and launch", ul(["Front-end and integrations", f"Go-live checklist {mono('v1.0')}"]), tags=["2 weeks"])
e.h2("Investment")
e.table(["Item", "Hours", "Amount"], [["Discovery", "60", "$9,000"], ["Design", "120", "$18,000"], ["Build", "140", "$21,000"], ["Total", "320", "$48,000"]],
        widths=["56%", "18%", "26%"], align=["start", "end", "end"], total_row=True)
e.kv([("Client", "Northwind Co."), ("Start", "1 November 2026"), ("Contact", "hello@example.com")])
e.note("Prices exclude VAT. The offer is valid for 30 days.", "info", title="Terms")
e.save(out / "pdf-atelier-example-en.pdf")
print("OK ->", out)
