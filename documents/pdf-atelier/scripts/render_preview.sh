#!/usr/bin/env bash
# Render every page of a PDF to PNG (for visual QA) and build one contact sheet.
# Usage: render_preview.sh file.pdf [dpi=75]   -> /tmp/preview/page-N.png and /tmp/preview/sheet.png
set -e
PDF="$1"; DPI="${2:-75}"
OUT=/tmp/preview; rm -rf "$OUT"; mkdir -p "$OUT"
pdftoppm -r "$DPI" -png "$PDF" "$OUT/page"
python3 - <<PY
from PIL import Image
import glob
fs = sorted(glob.glob("$OUT/page-*.png"))
ims = [Image.open(f) for f in fs]
W = sum(i.width for i in ims); H = max(i.height for i in ims)
sheet = Image.new("RGB", (W, H), "white"); x = 0
for i in ims:
    sheet.paste(i, (x, 0)); x += i.width
sheet.save("$OUT/sheet.png")
print(len(ims), "page(s) ->", "$OUT/sheet.png")
PY
