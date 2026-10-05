# PDF Atelier

Beautiful, consistent PDFs from a single prompt. A [Claude skill](../../README.md) that turns reports, proposals, resumes, menus and more into polished documents with RTL support (Arabic, Hebrew, Persian) built in.

## Why

- **One design language** for every document: clean hierarchy, tight spacing, 6px corners.
- **12 themes**, all contrast-audited. Or generate one from any brand color.
- **RTL done right**: layout, tables, charts and bullets mirror automatically.
- **Real components**: cover, hero, stat tiles, tables, bar charts, timelines, checklists, callouts.
- **Fonts included**: Vazirmatn and JetBrains Mono, no install needed.

## Try it

Ask Claude:

> Make me a clean PDF proposal for a website redesign, use the executive theme.

> Create a quarterly report PDF with the ocean theme.

## Themes

| Theme | Good for |
|---|---|
| `indigo` (default) | Education, tech, product |
| `ocean` | Corporate, finance, reports |
| `executive` | Proposals, legal, premium |
| `teal` | Health, science, wellness |
| `emerald` | Sustainability, nutrition |
| `forest` | Nature, outdoors |
| `sunset` | Events, food, creative |
| `crimson` | Sports, awards, urgent |
| `rose` | Lifestyle, beauty, kids |
| `violet` | Design, arts, music |
| `graphite` | Minimal, formal, B&W print |
| `paper` | Essays, long reading |

Custom brand color: `Theme.from_hex("#0f766e")`. Full gallery: [`assets/theme-gallery.pdf`](assets/theme-gallery.pdf).

## Install

**Claude.ai:** zip this folder, then go to Settings > Capabilities > Skills > Upload.

**Claude Code:**

```bash
cp -r documents/pdf-atelier ~/.claude/skills/
```

Requires Python 3 and `weasyprint` (installed by `scripts/setup.sh`). `poppler-utils` is optional, used for visual previews.

## Use as a library

```python
from pdfkit import Doc

doc = Doc(rtl=False, theme="ocean", title="Quarterly report")
doc.hero("Internal", "Quarterly report", "Highlights and next steps")
doc.stats([("1.2M", "Revenue", "+14%"), ("92", "NPS"), ("3,400", "Users")])
doc.h2("Regions")
doc.bars([("North", 480), ("South", 310)], colors=True)
doc.save("report.pdf")
```

Run the full demo: `python3 scripts/example.py ./out`

## Structure

```
pdf-atelier/
├── SKILL.md           skill instructions for Claude
├── assets/            fonts, theme gallery
├── scripts/           pdfkit.py (components), themes.py, setup.sh, example.py
└── references/        design rules and rendering pitfalls
```

## Not for

Merging, splitting, filling forms, OCR or editing existing PDFs. Use a general PDF skill for those.

## License

Fonts are under the SIL Open Font License (see `assets/fonts`).
