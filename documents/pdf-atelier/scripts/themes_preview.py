#!/usr/bin/env python3
"""Builds a theme gallery PDF: every curated theme with its palette swatches, sample components and
contrast-audit result. Show it to the user so they can pick a theme.
Usage: python3 themes_preview.py [output.pdf]"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pdfkit import Doc
from themes import THEME_NAMES, THEME_MOODS, get_theme

out = sys.argv[1] if len(sys.argv) > 1 else "/mnt/user-data/outputs/theme-gallery.pdf"
d = Doc(rtl=False, title="Theme gallery", theme="graphite")
d.hero("pdf-atelier", "Theme gallery", "Every palette is generated in OKLCH and contrast-audited")
for i, name in enumerate(THEME_NAMES):
    t = get_theme(name)
    keys = ["brand", "accent", "accent_soft", "surface2", "ink", "muted"]
    sw = "".join(f'<td style="background:{t[k]};height:34px;border:0"></td>' for k in keys)
    sw2 = "".join(f'<td style="background:{c};height:14px;border:0"></td>' for c in t["series"])
    ok = all(a[3] for a in t.audit())
    d.raw(f'<div style="page-break-inside:avoid;margin:10px 0 14px 0;border:1px solid {get_theme("graphite")["line"]};border-radius:6px;padding:8px 12px">'
          f'<div style="font-weight:700;font-size:12pt;color:{t["brand"]}">{name} '
          f'<span style="font-weight:400;font-size:9pt;color:#64748b">· {THEME_MOODS[name]} · contrast {"pass" if ok else "FAIL"}</span></div>'
          f'<table style="width:100%;border-collapse:collapse;margin:6px 0 2px 0;border-radius:4px"><tr>{sw}</tr></table>'
          f'<table style="width:100%;border-collapse:collapse;margin:0 0 6px 0"><tr>{sw2}</tr></table>'
          f'<table style="width:100%;border-collapse:separate;border-spacing:6px 0;margin:0 -6px"><tr>'
          f'<td style="border:0;padding:0"><div style="background:{t["brand"]};color:#fff;border-radius:6px;padding:6px 10px;font-weight:700;border-bottom:3px solid {t["accent"]}">Heading on brand</div></td>'
          f'<td style="border:0;padding:0"><div style="background:{t["accent_soft"]};color:{t["accent_text"]};border-radius:6px;padding:6px 10px;border-left:4px solid {t["accent"]}">Info callout</div></td>'
          f'<td style="border:0;padding:0"><div style="background:{t["sem"]["warn"]["bg"]};color:{t["sem"]["warn"]["text"]};border-radius:6px;padding:6px 10px;border-left:4px solid {t["sem"]["warn"]["bar"]}">Warning</div></td>'
          f'</tr></table></div>')
d.save(out)
print("OK ->", out)
