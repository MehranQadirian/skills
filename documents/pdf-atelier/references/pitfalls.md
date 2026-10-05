# Pitfalls and fixes

| Symptom | Cause | Fix |
|---|---|---|
| Tiny text, content cut off on the right, weak RTL shaping | wkhtmltopdf / unpatched Qt | Use WeasyPrint via `pdfkit.Doc`; never wkhtmltopdf or reportlab for RTL |
| `ModuleNotFoundError: weasyprint` | not installed | `bash scripts/setup.sh` |
| RTL text shows as boxes | fonts not loaded | build through `Doc` (it sets `base_url` and `@font-face`) |
| `a > b` appears as `b > a`, parentheses jump sides in RTL text | bidi reordering | wrap the whole Latin fragment in `mono()`; avoid starting an RTL line with a Latin word |
| `pdftotext` output looks scrambled for RTL | extraction order differs from visual order | ignore; verify with rendered PNGs |
| Footer `1 / 3` reversed | footer inherits RTL | already forced LTR |
| `box-shadow` has no effect | unsupported in WeasyPrint | use borders / accent bars |
| Big blank gap at page bottom | an unbreakable block did not fit | reorder, shorten previous section, or reduce spacing |
| Component splits across pages | block taller than the page remainder | already `page-break-inside: avoid`; add `page_break=True` to the heading before it |
| Cover shows a blank second page | cover height exceeds page | cover is 296mm on a 297mm page; for Letter set `extra_css=".cover{height:278mm}"` |
| Table text overflows | very long unbroken strings | give the column an explicit width in `widths`, shorten text, or use `mono()` for short tokens only |
| Colours look off / low contrast | hand-picked hex | use theme tokens; run `theme.audit()` |
| Wrong totals or percentages | arithmetic done mentally | compute in Python, then paste |
| Hidden text for "AI protection" | unreliable and harms accessibility | do not use |

Fonts: Vazirmatn and JetBrains Mono are SIL OFL 1.1 (licences in `assets/fonts/`); WeasyPrint embeds subsets in
each PDF automatically.
