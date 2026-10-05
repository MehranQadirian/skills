#!/usr/bin/env bash
# One-time environment check/installation for the pdf-atelier skill.
set -e
python3 -c "import weasyprint" 2>/dev/null || pip install weasyprint --break-system-packages -q
python3 -c "import PIL" 2>/dev/null || pip install pillow --break-system-packages -q
python3 -c "import pygments" 2>/dev/null || pip install pygments --break-system-packages -q
command -v pdftoppm >/dev/null || echo "WARNING: pdftoppm (poppler-utils) missing - cannot render previews"
python3 -c "import weasyprint; print('weasyprint', weasyprint.__version__)"
