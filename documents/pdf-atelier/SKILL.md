---
name: pdf-atelier
description: House style for creating ANY new PDF with Claude - reports, proposals, brochures, menus, resumes, certificates, newsletters, invoices, study notes, handouts, one-pagers, manuals. Builds the document as HTML/CSS rendered by WeasyPrint with an engineered design system - cards, stat tiles, tables, timelines, bar charts, callouts, cover pages - 12 ready colour themes (OKLCH-generated and WCAG contrast-audited, switchable per document or derived from any brand colour), bundled Vazirmatn + JetBrains Mono fonts, and first-class right-to-left (RTL) support for Arabic, Hebrew and Persian. Use this skill whenever the user asks Claude to create, design, write or export a PDF in any language and topic, even if they only say "make me a PDF", "a clean PDF" or "export this as a PDF", and whenever visual quality matters. Not for merging, splitting, filling forms, OCR or editing an existing PDF (use the pdf skill for those).
---

# pdf-atelier

One consistent, professional design language for every PDF: calm hierarchy, generous but tight spacing, 6px corners
(never sharp, never pill-like), engineered colour palettes, perfect RTL. Topic does not matter; the content decides
which components to use and the theme decides the mood.

```
pdf-atelier/
├── SKILL.md
├── assets/
│   ├── fonts/            Vazirmatn 400/500/700, JetBrains Mono 400/700 (+ OFL licences)
│   └── theme-gallery.pdf pre-rendered preview of all 12 themes
├── scripts/
│   ├── setup.sh          installs weasyprint / pillow if missing
│   ├── themes.py         OKLCH palette engine + 12 curated themes + contrast audit
│   ├── pdfkit.py         Doc class: all components (import this)
│   ├── example.py        runnable demo (RTL report + LTR proposal)
│   ├── themes_preview.py regenerates the theme gallery PDF
│   ├── render_preview.sh PDF -> PNG pages + contact sheet (visual QA)
│   └── extras.py         OPTIONAL terminal/code windows - only if the content truly needs them
└── references/
    ├── design-rules.md   spacing, type scale, colour engineering, layout patterns, checklist
    └── pitfalls.md       rendering traps and fixes
```

## Workflow

1. **Setup once**: `bash <skill>/scripts/setup.sh` (fonts need no installation).
2. **Choose the theme** (see table). If the user names a colour/brand, use `Theme.from_hex("#...")`. If they gave no
   hint, pick by subject and mention the theme name in one phrase; offer `assets/theme-gallery.pdf` when they want
   to browse.
3. **Plan** pages and sections before writing: aim for 1-4 A4 pages (a dedicated `cover()` only for long formal
   documents). Map each piece of content to a component (table below). Keep text short; prefer tables, tiles,
   lists and charts over paragraphs. One idea per bullet.
4. **Check facts and numbers with code** (totals, percentages, dates, conversions). Never do arithmetic by hand in
   the document. Keep units and spelling consistent everywhere.
5. **Write the build script** (in `/home/claude`) and save to `/mnt/user-data/outputs/<name>.pdf`:
   ```python
   import sys; sys.path.insert(0, "/mnt/skills/user/pdf-atelier/scripts")    # use the real install path
   from pdfkit import Doc, mono, b, ul, tag
   doc = Doc(rtl=False, theme="ocean", title="Quarterly report")           # rtl=True for fa/ar/he
   doc.hero("Internal · Q3", "Quarterly report", "Highlights and next steps")
   doc.stats([("1.2M", "Revenue", "▲ 14%"), ("92", "NPS"), ("3,400", "Active users")])
   doc.h2("Regions"); doc.bars([("North", 480), ("South", 310)], colors=True)
   doc.save("/mnt/user-data/outputs/report.pdf")
   ```
6. **Look at every page**: `bash <skill>/scripts/render_preview.sh <pdf> 75` then `view /tmp/preview/sheet.png`
   (zoom with `/tmp/preview/page-N.png`). Fix clipping, orphan headings, big empty areas, flipped symbols; re-render.
   Judge RTL by the picture, never by `pdftotext` (extracted RTL text always looks scrambled).
7. **Deliver** with `present_files`. One or two sentences, no long recap.

## Themes (all contrast-audited: brand/white >= 7:1, body >= 7:1, muted >= 4.5:1, chips/badges >= 4.5:1)

| theme | mood / use |
|---|---|
| `indigo` (default) | education, tech, product documents |
| `ocean` | trustworthy blue: corporate, finance, reports |
| `executive` | navy + gold: proposals, legal, premium |
| `teal` | calm clean: health, science, wellness |
| `emerald` | fresh: sustainability, growth, nutrition |
| `forest` | earthy: nature, outdoors, organic |
| `sunset` | warm orange: events, food, creative |
| `crimson` | bold red: urgent, sports, awards |
| `rose` | soft magenta: lifestyle, beauty, kids |
| `violet` | creative purple: design, arts, music |
| `graphite` | neutral grey: minimal, formal, print-first / B&W printers |
| `paper` | warm sepia: essays, literature, long reading |

Custom: `Theme.from_hex("#0f766e")` (whole palette from one colour) or
`Theme.make("name", brand_hue=258, accent_hue=82, chroma=0.9)` (two-hue schemes) -> pass as `theme=`.
`theme.audit()` returns every contrast pair with pass/fail; run it for custom themes and fix failures by changing
chroma/lightness. Never hand-pick extra colours: use theme tokens (`doc.t["accent"]`, `doc.t["series"][i]`, ...).

## Components (`pdfkit.Doc`)

| Need | Method |
|---|---|
| Full cover page (own page, no footer) | `cover(title, subtitle, tag_line, meta=[(k, v)])` |
| Title banner on page 1 | `hero(tag_line, title, subtitle)` |
| Section / sub-section / paragraph / intro | `h2(text, page_break=False)`, `h3`, `p`, `lead` |
| Soft panel / callout (info, warn, ok, bad) | `card(html, title)`, `note(html, kind, title)` |
| Numbered steps, chapters, features | `numbered(n, title, body_html, tags=[...])` |
| KPI tiles | `stats([(value, label, note?)], colors=False)` (3-4 per row) |
| Table (zebra, aligned columns, total row) | `table(headers, rows, widths, align, total_row)`; align: `start/end/center/ltr` |
| Key-value list (contact, specs) | `kv([(k, v)])` |
| Bar chart (pure CSS) | `bars([(label, value)], colors, fmt)` |
| Timeline / roadmap | `timeline([(when, title, desc)])` |
| Checklist | `checklist(["a", ("b", True)])` |
| Two columns | `columns(left_html, right_html, ratio=(1, 1))` |
| Quote | `quote(text, by)` |
| Image / SVG with caption | `figure('<img src="file:///...">', caption)` |
| Divider, page break, raw HTML | `divider()`, `pagebreak()`, `raw(html)` |
| Inline helpers | `b()`, `mono()` (LTR code/IDs/English terms), `tag()`, `ul()`, `ol()` |

Charts beyond bars: draw inline SVG (use theme colours) and pass it to `figure()`, or render with matplotlib to PNG
using the theme colours and embed with `file://`.

## Design principles (details: `references/design-rules.md`)

- Hierarchy: one hero/cover -> `h2` sections with an accent bar -> content in cards, tiles or tables.
- Colour discipline: brand (dark) for banners and headings, ONE accent for markers, neutrals for surfaces;
  amber/green/red only for status callouts; series colours only for charts/chips.
- Density: 10pt body, 1.7 line-height, 6px gaps. Prefer fewer, fuller pages; avoid pages with only 3 lines.
- Components never split across pages (`page-break-inside: avoid`); use `h2(..., page_break=True)` to start a big
  block on a fresh page.
- Write for the reader: short sentences, concrete numbers, no filler. Beginners: define a term once, in a chip or
  a table, not in a paragraph.

## Right-to-left (Arabic / Hebrew / Persian)

- `Doc(rtl=True, lang="ar")` mirrors layout, bullets, accent bars, tables, timelines and charts automatically.
- Wrap every Latin token inside RTL sentences (names, codes, formulas, URLs) in `mono()` so symbols never flip.
  For table columns with Latin/code content use `align="ltr"`; numbers use `align="end"`.
- RTL typography: use the correct script variants and joiners for the language, and keep program output and IDs exactly as they are.
- Footer page numbers stay LTR (`2 / 5`).

## Optional: terminal and code windows

Only when the content genuinely shows software output: `from extras import TechDoc` (subclass of `Doc`) adds
`terminal(...)` (macOS Terminal mockup, dark/light) and `code_window(...)`. Not part of the normal design system.

## Do not

- Hide text in the PDF (white-on-white, tiny fonts, metadata tricks); it is unreliable and hurts accessibility.
- Use `box-shadow` (WeasyPrint ignores it), wkhtmltopdf or reportlab for RTL, or hard-code hex colours outside the theme.
- Deliver without having looked at every rendered page.
