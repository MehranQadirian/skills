# Design rules

## 1. Page and rhythm
- A4 (change with `Doc(page="Letter")`), margins 14mm top / 15mm sides / 16mm bottom, footer `n / total`.
- Body 10pt / line-height 1.7. Vertical rhythm: 6px between cards/items, 10-14px before section headings.
- Target 1-4 pages. If content spills by a few lines, tighten (shorter text, fewer words per bullet, merge tiny
  sections) before shrinking fonts. Never go below 9pt body text.
- Start a large block on a new page with `h2(..., page_break=True)` instead of letting it split.

## 2. Type scale (Vazirmatn for all scripts; JetBrains Mono for `mono()`)
| Role | Size / weight |
|---|---|
| Cover title | 34pt / 700 |
| Hero title | 21pt / 700 |
| KPI value | 19pt / 700 |
| h2 | 13pt / 700 brand colour + accent bar |
| Item title | 12pt / 700 |
| Lead paragraph | 11.5pt |
| Body | 10pt |
| Table | 9.5-9.8pt |
| Chips / captions / notes | 8.5-9pt |

## 3. Shape
6px for cards, items, notes, hero, stat tiles; 4-5px for badges and chips; 3px for inline mono; 8px for windows;
true circles only for dots. 1px hairlines instead of shadows (shadows are not supported). Accent "bars"
(4px) mark headings, callouts and tiles on the start side (right in RTL).

## 4. Colour engineering
Palettes are generated in **OKLCH** (perceptually uniform lightness) from one or two hues:

| Token | L | C | Purpose |
|---|---|---|---|
| brand | ~0.28 | 0.10 | hero/cover background, h2 text, table headers |
| accent | ~0.56 | 0.17 | number badges, bars, markers, links |
| accent_soft | 0.955 | 0.03 | chip and info-callout background |
| accent_text | ~0.46 | 0.15 | text on accent_soft |
| ink / text / muted | 0.22 / 0.32 / 0.54 | tinted neutrals | headings / body / secondary |
| surface, surface2, line, line_strong | 0.978 / 0.958 / 0.925 / 0.875 | tinted neutrals | panels, table head, hairlines |
| semantic warn/ok/bad | hues 75 / 152 / 27 | same tonal rules | callouts only |
| series[0..5] | 0.60 | 0.13 | charts and categorical chips, hues spaced 55 degrees apart from the accent |

Rules: 60-30-10 (neutrals / brand / accent); series colours never carry text on them; contrast targets are enforced
by `theme.audit()` (white on brand >= 7, body >= 7, muted >= 4.5, badges/chips >= 4.5, callout text >= 4.5).
Every theme survives greyscale printing because lightness steps are fixed across hues; use `graphite` when the
document will certainly be printed in black and white.

Choosing a theme: match the subject and audience (finance/legal -> ocean/executive; health -> teal; kids/lifestyle ->
rose/sunset; long reading -> paper; unsure -> indigo or graphite). One theme per document. Bilingual or multi-part
documents keep the same theme.

## 5. Layout patterns
- **One-pager**: hero, lead, stats row, 2 sections (table or bars + list), note.
- **Report**: cover, executive summary (lead + stats), sections with tables/bars, timeline, appendix.
- **Proposal / quote**: hero, lead, stats, numbered phases, table with total row, kv (client/contact), terms note.
- **Handout / study sheet**: hero, lead, numbered items with chips, table(s), checklist, final practice/summary card.
- **Menu / price list**: hero, columns of kv lists, tags for dietary markers.
- **Certificate / invitation**: cover-style single page; use `extra_css` for centred layout.
- **Resume**: hero (name, role), columns (left: experience timeline; right: skills as tags, kv contacts).

## 6. Writing for the reader
Short sentences; numbers instead of adjectives; headings that say what the section tells ("Sales grew 14%" beats
"Sales"). Tables for anything with 2+ attributes. Never repeat the same information in a table and a paragraph.

## 7. Delivery checklist
1. Every page viewed as an image: no clipped edges, no orphan headings, no large blank areas, footers present.
2. Numbers computed by code; units, names and spelling consistent.
3. Theme tokens only; `theme.audit()` clean for custom themes.
4. RTL: Latin tokens in `mono()`, columns aligned correctly, script characters render correctly.
5. Saved in `/mnt/user-data/outputs/` and presented with `present_files`.
