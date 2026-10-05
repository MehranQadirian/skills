"""
pdfkit.py - a small design system for beautiful PDFs of ANY kind (reports, proposals, brochures,
menus, resumes, certificates, newsletters, study notes, invoices ...). Built on WeasyPrint.

 * RTL-first-class: Doc(rtl=True) mirrors the whole layout (Arabic / Hebrew / Persian).
 * Colours come from themes.py (OKLCH-generated, contrast-audited palettes).
 * Fonts load from ../assets/fonts via @font-face (nothing to install).

    import sys; sys.path.insert(0, "<skill>/scripts")
    from pdfkit import Doc, mono, b, ul
    doc = Doc(rtl=False, theme="ocean", title="Quarterly report")
    doc.cover("Quarterly Report", "Q3 2026", meta=[("Prepared by", "Finance team")])
    doc.h2("Highlights")
    doc.stats([("1.2M", "Revenue"), ("+14%", "Growth"), ("92", "NPS")])
    doc.save("/mnt/user-data/outputs/report.pdf")
"""
from __future__ import annotations

import html as _html
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from themes import Theme, get_theme, THEME_NAMES  # noqa: E402,F401

try:
    from weasyprint import HTML
except ImportError as e:  # pragma: no cover
    raise SystemExit("weasyprint missing: pip install weasyprint --break-system-packages") from e

SKILL_DIR = Path(__file__).resolve().parent.parent
FONT_DIR = SKILL_DIR / "assets" / "fonts"


# ------------------------------------------------------------------------------ inline helpers
def esc(t) -> str:
    return _html.escape(str(t), quote=False)


def mono(text) -> str:
    """Inline monospace token (codes, IDs, SKUs, formulas, English terms). Always LTR + isolated,
    so it never gets scrambled inside RTL sentences."""
    return f"<code>{esc(text)}</code>"


def b(text) -> str:
    return f"<b>{text}</b>"


def tag(text, color: int | None = None) -> str:
    """Small chip. color = index 0-5 into the theme's categorical series (None = accent)."""
    cls = f"tag s{color}" if color is not None else "tag"
    return f'<span class="{cls}">{esc(text)}</span>'


def ul(items) -> str:
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def ol(items) -> str:
    return "<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"


# ------------------------------------------------------------------------------ document
class Doc:
    def __init__(self, rtl: bool = False, lang: str | None = None, title: str = "Document",
                 theme: str | Theme = "indigo", footer: bool = True, base_pt: float = 10.0,
                 margins_mm=(14, 15, 16, 15), page: str = "A4", extra_css: str = ""):
        self.rtl = rtl
        self.lang = lang or ("ar" if rtl else "en")
        self.title = title
        self.theme = get_theme(theme) if isinstance(theme, str) else theme
        self.t = self.theme.t
        self.footer = footer
        self.base_pt = base_pt
        self.margins = margins_mm
        self.page = page
        self.extra_css = extra_css
        self.parts: list[str] = []
        self.start = "right" if rtl else "left"
        self.end = "left" if rtl else "right"

    # ---------------------------------------------------------------- page-level
    def cover(self, title: str, subtitle: str = "", tag_line: str = "", meta: list[tuple[str, str]] | None = None):
        """Full-bleed cover page (own page, no footer). Put it first."""
        rows = "".join(f'<tr><td class="mk">{esc(k)}</td><td class="mv">{v}</td></tr>' for k, v in (meta or []))
        meta_html = f'<table class="cover-meta">{rows}</table>' if rows else ""
        sub = f'<p class="cv-sub">{subtitle}</p>' if subtitle else ""
        tg = f'<p class="cv-tag">{tag_line}</p>' if tag_line else ""
        self.parts.append(
            f'<div class="cover"><div class="cv-bar"></div>{tg}<h1>{title}</h1>{sub}{meta_html}</div>')

    def hero(self, tag_line: str, title: str, subtitle: str = ""):
        """Compact title banner for the top of page 1 (use instead of cover for short documents)."""
        sub = f'<p class="sub">{subtitle}</p>' if subtitle else ""
        self.parts.append(f'<div class="hero"><p class="tag-line">{tag_line}</p><h1>{title}</h1>{sub}</div>')

    def pagebreak(self):
        self.parts.append('<div style="page-break-after: always;"></div>')

    # ---------------------------------------------------------------- text
    def h2(self, text: str, page_break: bool = False):
        st = ' style="page-break-before: always;"' if page_break else ""
        self.parts.append(f"<h2{st}>{text}</h2>")

    def h3(self, text: str):
        self.parts.append(f"<h3>{text}</h3>")

    def p(self, text: str):
        self.parts.append(f"<p>{text}</p>")

    def lead(self, text: str):
        """Larger intro paragraph."""
        self.parts.append(f'<p class="lead">{text}</p>')

    def quote(self, text: str, by: str = ""):
        who = f'<div class="by">{by}</div>' if by else ""
        self.parts.append(f'<blockquote><div class="qt">{text}</div>{who}</blockquote>')

    def divider(self):
        self.parts.append("<hr>")

    def caption(self, text: str):
        self.parts.append(f'<div class="cap">{text}</div>')

    # ---------------------------------------------------------------- surfaces
    def card(self, inner_html: str, title: str = ""):
        head = f'<div class="card-t">{title}</div>' if title else ""
        self.parts.append(f'<div class="card">{head}{inner_html}</div>')

    def note(self, inner_html: str, kind: str = "info", title: str = ""):
        """kind: info | warn | ok | bad"""
        head = f'<div class="note-t">{title}</div>' if title else ""
        self.parts.append(f'<div class="note {kind}">{head}<p style="margin:0">{inner_html}</p></div>')

    def numbered(self, number, title: str, body_html: str = "", tags: list[str] | None = None):
        """Numbered block: badge + title + chips + free HTML body. For steps, chapters, features, rules."""
        chips = "".join(tag(x) for x in (tags or []))
        self.parts.append(
            f'<div class="item"><div class="ih"><span class="num">{number}</span>{title} {chips}</div>{body_html}</div>')

    def figure(self, inner_html: str, caption: str = ""):
        """inner_html: <img src="file:///..."> or inline <svg>."""
        cap = f'<div class="fig-cap">{caption}</div>' if caption else ""
        self.parts.append(f'<div class="fig">{inner_html}{cap}</div>')

    def columns(self, left_html: str, right_html: str, ratio: tuple[int, int] = (1, 1), gap_mm: float = 6):
        a, c = ratio
        tot = a + c
        self.parts.append(
            f'<table class="cols"><tr><td style="width:{a / tot * 100:.1f}%;padding-{self.end}:{gap_mm / 2}mm">{left_html}</td>'
            f'<td style="width:{c / tot * 100:.1f}%;padding-{self.start}:{gap_mm / 2}mm">{right_html}</td></tr></table>')

    # ---------------------------------------------------------------- data
    def table(self, headers: list[str], rows: list[list[str]], widths: list[str] | None = None,
              align: list[str] | None = None, zebra: bool = True, total_row: bool = False):
        """
        Cells are raw HTML. align per column: 'start' (default) | 'end' | 'center' | 'ltr'
        ('ltr' = left-aligned LTR text such as codes/English; use 'end' for numbers).
        total_row=True styles the last row bold with a top rule.
        """
        align = align or ["start"] * len(headers)

        def cls(i):
            return f' class="{ {"start": "", "end": "e", "center": "c", "ltr": "l"}[align[i]] }"' if align[i] != "start" else ""

        def w(i):
            return f' style="width:{widths[i]}"' if widths else ""
        head = "".join(f"<th{cls(i)}{w(i)}>{x}</th>" for i, x in enumerate(headers))
        body = []
        for ri, row in enumerate(rows):
            klass = []
            if zebra and ri % 2:
                klass.append("alt")
            if total_row and ri == len(rows) - 1:
                klass.append("total")
            tr = f' class="{" ".join(klass)}"' if klass else ""
            body.append(f"<tr{tr}>" + "".join(f"<td{cls(i)}>{x}</td>" for i, x in enumerate(row)) + "</tr>")
        self.parts.append(f"<table class='data'><tr>{head}</tr>{''.join(body)}</table>")

    def stats(self, items: list[tuple], colors: bool = False):
        """KPI cards in one row. items: (value, label) or (value, label, note). Max ~4 per row."""
        n = len(items)
        cells = []
        any_note = any(len(it) > 2 for it in items)
        for i, it in enumerate(items):
            val, lab = it[0], it[1]
            note = f'<div class="st-n">{it[2]}</div>' if len(it) > 2 else ('<div class="st-n">&nbsp;</div>' if any_note else "")
            style = f' style="border-{self.start}-color:{self.t["series"][i % 6]}"' if colors else ""
            cells.append(f'<td style="width:{100 / n:.1f}%"><div class="stat"{style}><div class="st-v">{val}</div>'
                         f'<div class="st-l">{lab}</div>{note}</div></td>')
        self.parts.append(f'<table class="stats"><tr>{"".join(cells)}</tr></table>')

    def kv(self, pairs: list[tuple[str, str]], key_width: str = "30%"):
        rows = "".join(f'<tr><td class="k" style="width:{key_width}">{k}</td><td class="v">{v}</td></tr>' for k, v in pairs)
        self.parts.append(f'<table class="kv">{rows}</table>')

    def bars(self, data: list[tuple], max_value: float | None = None, fmt: str = "{:,.0f}", colors: bool = False,
             label_width: str = "26%", value_width: str = "14%"):
        """Horizontal bar chart in pure CSS. data: [(label, value)]."""
        mx = max_value or max(v for _, v in data) or 1
        rows = []
        for i, (lab, v) in enumerate(data):
            pct = max(1.5, v / mx * 100)
            col = self.t["series"][i % 6] if colors else self.t["accent"]
            rows.append(
                f'<tr><td class="bl" style="width:{label_width}">{lab}</td>'
                f'<td class="bt"><div class="track"><div class="fill" style="width:{pct:.1f}%;background:{col}"></div></div></td>'
                f'<td class="bv" style="width:{value_width}">{fmt.format(v)}</td></tr>')
        self.parts.append(f'<table class="bars">{"".join(rows)}</table>')

    def timeline(self, items: list[tuple]):
        """items: (when, title, description)."""
        rows = []
        for when, title, desc in items:
            rows.append(f'<div class="tl-i"><span class="tl-dot"></span><div class="tl-w">{when}</div>'
                        f'<div class="tl-t">{title}</div><div class="tl-d">{desc}</div></div>')
        self.parts.append(f'<div class="tl">{"".join(rows)}</div>')

    def checklist(self, items: list):
        out = []
        for it in items:
            text, done = (it, False) if isinstance(it, str) else it
            out.append(f'<div class="ck"><span class="box{" on" if done else ""}">{"✓" if done else ""}</span>{text}</div>')
        self.parts.append("".join(out))

    def raw(self, html: str):
        self.parts.append(html)

    # ---------------------------------------------------------------- build
    def css(self) -> str:
        t, st, en = self.t, self.start, self.end
        d = "rtl" if self.rtl else "ltr"
        fonts = "".join(
            f"@font-face {{ font-family: '{fam}'; font-weight: {w}; src: url('{(FONT_DIR / fn).as_uri()}'); }}\n"
            for fam, w, fn in [
                ("Vazirmatn", 400, "Vazirmatn-Regular.ttf"), ("Vazirmatn", 500, "Vazirmatn-Medium.ttf"),
                ("Vazirmatn", 700, "Vazirmatn-Bold.ttf"),
                ("JetBrains Mono", 400, "JetBrainsMono-Regular.ttf"), ("JetBrains Mono", 700, "JetBrainsMono-Bold.ttf")])
        m = self.margins
        footer = (f"@bottom-center {{ content: counter(page) ' / ' counter(pages); font-family: 'Vazirmatn'; "
                  f"font-size: 8.5pt; color: {t['muted']}; direction: ltr; }}") if self.footer else ""
        sem_css = "".join(
            f".note.{k} {{ background: {v['bg']}; border-color: {v['line']}; border-{st}-color: {v['bar']}; }}\n"
            f".note.{k} .note-t {{ color: {v['text']}; }}\n" for k, v in t["sem"].items())
        series_css = "".join(
            f".tag.s{i} {{ background: {t['series_soft'][i]}; color: {t['ink']}; border: 1px solid {t['series'][i]}; }}\n"
            for i in range(6))
        return f"""
{fonts}
@page {{ size: {self.page}; margin: {m[0]}mm {m[1]}mm {m[2]}mm {m[3]}mm; {footer} }}
@page cover {{ margin: 0; @bottom-center {{ content: none; }} }}
html {{ direction: {d}; }}
body {{ font-family: 'Vazirmatn', 'DejaVu Sans', sans-serif; font-size: {self.base_pt}pt; line-height: 1.7;
       color: {t['text']}; direction: {d}; margin: 0; }}
p {{ margin: 4px 0; }}
b {{ color: {t['ink']}; }}
a {{ color: {t['accent_text']}; text-decoration: none; }}
hr {{ border: 0; border-top: 1px solid {t['line_strong']}; margin: 14px 0; }}

/* ---------- cover & hero ---------- */
.cover {{ page: cover; box-sizing: border-box; height: 296mm; background: {t['brand']}; color: #fff;
          padding: 70mm 24mm 0 24mm; page-break-after: always; }}
.cv-bar {{ width: 46px; height: 5px; background: {t['accent']}; border-radius: 3px; margin-bottom: 14px; }}
.cv-tag {{ margin: 0 0 6px 0; color: {t['hero_tag']}; font-size: 11pt; }}
.cover h1 {{ margin: 0; font-size: 34pt; line-height: 1.35; font-weight: 700; color: #fff; }}
.cv-sub {{ margin: 10px 0 0 0; font-size: 14pt; color: {t['hero_sub']}; }}
.cover-meta {{ margin-top: 40mm; border-collapse: collapse; }}
.cover-meta td {{ border: 0; padding: 3px 0; font-size: 10.5pt; }}
.cover-meta .mk {{ color: {t['hero_tag']}; padding-{en}: 18px; }}
.cover-meta .mv {{ color: #fff; }}

.hero {{ background: {t['brand']}; color: #fff; border-radius: 6px; padding: 14px 24px 12px 24px; margin-bottom: 10px;
         border-bottom: 4px solid {t['accent']}; }}
.hero .tag-line {{ font-size: 9pt; color: {t['hero_tag']}; margin: 0 0 2px 0; }}
.hero h1 {{ margin: 0; font-size: 21pt; line-height: 1.5; font-weight: 700; color: #fff; }}
.hero .sub {{ margin: 2px 0 0 0; font-size: 10pt; color: {t['hero_sub']}; }}

/* ---------- headings & text ---------- */
h2 {{ font-size: 13pt; color: {t['brand']}; margin: 14px 0 6px 0; padding-{st}: 10px; border-{st}: 4px solid {t['accent']};
      line-height: 1.4; page-break-after: avoid; }}
h3 {{ font-size: 11.5pt; color: {t['ink']}; margin: 10px 0 4px 0; page-break-after: avoid; }}
.lead {{ font-size: 11.5pt; line-height: 1.8; color: {t['ink']}; margin: 6px 0 8px 0; }}
blockquote {{ margin: 10px 0; padding: 4px 16px; border-{st}: 4px solid {t['accent']}; background: {t['surface']};
              border-radius: 6px; page-break-inside: avoid; }}
blockquote .qt {{ font-size: 11.5pt; color: {t['ink']}; line-height: 1.8; }}
blockquote .by {{ font-size: 9pt; color: {t['muted']}; margin-top: 2px; }}
ul, ol {{ margin: 2px 0; padding-{st}: 20px; padding-{en}: 0; }}
li {{ margin-bottom: 1px; }}
.cap {{ margin: 8px 0 5px 0; font-weight: 700; color: {t['brand']}; font-size: 11pt; page-break-after: avoid; }}

/* ---------- surfaces (6px radius: neither sharp nor pill-like) ---------- */
.card {{ background: {t['surface']}; border: 1px solid {t['line']}; border-radius: 6px; padding: 8px 16px; margin: 6px 0;
         page-break-inside: avoid; }}
.card-t {{ font-weight: 700; color: {t['brand']}; margin-bottom: 2px; }}
.note {{ border: 1px solid; border-{st}-width: 4px; border-radius: 6px; padding: 7px 16px; margin: 8px 0; page-break-inside: avoid; }}
.note-t {{ font-weight: 700; margin-bottom: 1px; }}
{sem_css}
.item {{ border: 1px solid {t['line']}; border-radius: 6px; margin: 6px 0; padding: 6px 16px 4px 16px; background: #fff;
         page-break-inside: avoid; }}
.ih {{ margin: 0 0 3px 0; font-size: 12pt; font-weight: 700; color: {t['ink']}; line-height: 1.6; }}
.num {{ display: inline-block; width: 24px; height: 24px; line-height: 24px; text-align: center; background: {t['accent']};
        color: #fff; border-radius: 5px; font-size: 10.5pt; margin-{en}: 8px; font-weight: 700; }}
.tag {{ display: inline-block; font-size: 8.5pt; font-weight: 400; color: {t['accent_text']}; background: {t['accent_soft']};
        border-radius: 4px; padding: 0 7px; margin-{en}: 4px; line-height: 1.6; }}
{series_css}
.fig {{ margin: 8px 0; text-align: center; page-break-inside: avoid; }}
.fig img, .fig svg {{ max-width: 100%; border-radius: 6px; }}
.fig-cap {{ font-size: 9pt; color: {t['muted']}; margin-top: 3px; }}
table.cols {{ width: 100%; border-collapse: collapse; margin: 4px 0; page-break-inside: avoid; }}
table.cols td {{ vertical-align: top; border: 0; }}

code {{ direction: ltr; unicode-bidi: isolate; white-space: nowrap; font-family: 'JetBrains Mono', 'DejaVu Sans Mono', monospace;
        font-size: 9pt; background: {t['mono_bg']}; color: {t['mono_fg']}; padding: 0 4px; border-radius: 3px; }}

/* ---------- tables ---------- */
table.data {{ border-collapse: collapse; width: 100%; margin: 6px 0; page-break-inside: avoid; }}
table.data th {{ background: {t['surface2']}; color: {t['brand']}; padding: 3px 10px; font-size: 9.5pt; text-align: {st};
                 border: 1px solid {t['line_strong']}; }}
table.data td {{ border: 1px solid {t['line']}; padding: 2px 10px; font-size: 9.8pt; vertical-align: middle; }}
table.data tr.alt td {{ background: {t['surface']}; }}
table.data tr.total td {{ font-weight: 700; border-top: 2px solid {t['brand']}; background: {t['accent_soft']}; color: {t['ink']}; }}
table.data .e {{ text-align: {en}; }} table.data .c {{ text-align: center; }}
table.data .l {{ text-align: left; direction: ltr; }}

table.stats {{ width: calc(100% + 16px); border-collapse: separate; border-spacing: 8px 0; margin: 6px -8px; page-break-inside: avoid; }}
table.stats td {{ border: 0; padding: 0; vertical-align: top; }}
.stat {{ border: 1px solid {t['line']}; border-{st}: 4px solid {t['accent']}; border-radius: 6px; background: {t['surface']};
         padding: 8px 14px; }}
.st-v {{ font-size: 19pt; font-weight: 700; color: {t['brand']}; line-height: 1.3; }}
.st-l {{ font-size: 9.5pt; color: {t['muted']}; }}
.st-n {{ font-size: 8.5pt; color: {t['accent_text']}; margin-top: 1px; }}

table.kv {{ width: 100%; border-collapse: collapse; margin: 4px 0; page-break-inside: avoid; }}
table.kv td {{ border: 0; border-bottom: 1px solid {t['line']}; padding: 3px 4px; font-size: 9.8pt; }}
table.kv td.k {{ color: {t['muted']}; }} table.kv td.v {{ color: {t['ink']}; font-weight: 500; }}

table.bars {{ width: 100%; border-collapse: collapse; margin: 6px 0; page-break-inside: avoid; }}
table.bars td {{ border: 0; padding: 3px 4px; font-size: 9.5pt; vertical-align: middle; }}
table.bars .bv {{ text-align: {en}; color: {t['ink']}; font-weight: 700; direction: ltr; }}
.track {{ height: 9px; background: {t['surface2']}; border-radius: 4px; }}
.fill {{ height: 9px; border-radius: 4px; }}

.tl {{ margin: 6px 0; padding-{st}: 18px; border-{st}: 2px solid {t['line_strong']}; }}
.tl-i {{ position: relative; margin-bottom: 9px; page-break-inside: avoid; }}
.tl-dot {{ position: absolute; {st}: -26px; top: 6px; width: 10px; height: 10px; border-radius: 50%; background: {t['accent']};
           border: 2px solid #fff; }}
.tl-w {{ font-size: 8.8pt; color: {t['accent_text']}; font-weight: 700; }}
.tl-t {{ font-weight: 700; color: {t['ink']}; line-height: 1.5; }}
.tl-d {{ font-size: 9.8pt; color: {t['text']}; }}

.ck {{ margin: 2px 0; }}
.box {{ display: inline-block; width: 13px; height: 13px; line-height: 13px; text-align: center; border: 1.5px solid {t['accent']};
        border-radius: 3px; margin-{en}: 8px; font-size: 8pt; color: #fff; vertical-align: middle; }}
.box.on {{ background: {t['accent']}; }}

{self.extra_css}
"""

    def html(self) -> str:
        return (f'<!DOCTYPE html><html lang="{self.lang}" dir="{"rtl" if self.rtl else "ltr"}"><head>'
                f'<meta charset="utf-8"><title>{esc(self.title)}</title><style>{self.css()}</style></head>'
                f'<body>{"".join(self.parts)}</body></html>')

    def save(self, out_path: str, keep_html: str | None = None) -> str:
        out_path = str(out_path)
        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
        html = self.html()
        if keep_html:
            Path(keep_html).write_text(html, encoding="utf-8")
        HTML(string=html, base_url=str(SKILL_DIR)).write_pdf(out_path)
        return out_path
