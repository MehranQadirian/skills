"""
extras.py - OPTIONAL add-on, only for documents that literally need a macOS Terminal or code-editor
window mockup (e.g. software docs). Not part of the general design system.

    from extras import TechDoc
    doc = TechDoc(rtl=False, theme="graphite")
    doc.terminal([("Name:", "Ali"), "Hello Ali"], command="python3 app.py")
    doc.code_window("print('hi')", filename="app.py")
"""
from __future__ import annotations
from pathlib import Path
from pdfkit import Doc, esc

_CSS = """
.win { direction: ltr; text-align: left; border: 1px solid #0b0b0d; border-radius: 8px; overflow: hidden; margin: 0 0 4px 0; page-break-inside: avoid; }
.win .tb { position: relative; height: 26px; border-bottom: 1px solid #0b0b0d; }
.win .dots { position: absolute; left: 11px; top: 7px; }
.dot { display: inline-block; width: 11px; height: 11px; border-radius: 50%; margin-right: 7px; }
.dot.r { background: #ff5f57; border: 0.5px solid #de4a42; } .dot.y { background: #febc2e; border: 0.5px solid #d99d1f; }
.dot.g { background: #28c840; border: 0.5px solid #1da832; }
.win .ttl { position: absolute; left: 0; right: 0; top: 0; line-height: 26px; text-align: center; font-family: 'DejaVu Sans', sans-serif; font-size: 8.3pt; }
.win pre { margin: 0; padding: 8px 14px 9px 14px; font-family: 'JetBrains Mono', 'DejaVu Sans Mono', monospace; line-height: 1.42; white-space: pre-wrap; direction: ltr; text-align: left; }
.win.dark { background: #1c1c1e; } .win.dark .tb { background: #3a3a3c; } .win.dark .ttl { color: #c9c9cf; } .win.dark pre { color: #d4d4d8; }
.win.dark .u { color: #7ee787; } .win.dark .d { color: #79b8ff; } .win.dark .pc { color: #e4e4e7; } .win.dark .cmd { color: #fff; font-weight: 700; }
.win.dark .q { color: #a1a1aa; } .win.dark .in { color: #ffd479; font-weight: 700; } .win.dark .hd { color: #5fd7e8; }
.win.dark .ok { color: #7ee787; } .win.dark .err { color: #ff7b72; } .win.dark .dim { color: #8b8b94; } .win.dark .cur { background: #d4d4d8; }
.win.light { background: #fff; border-color: #b9b9be; } .win.light .tb { background: #e8e8ea; border-bottom-color: #c9c9ce; } .win.light .ttl { color: #4a4a50; } .win.light pre { color: #1c1c1e; }
.win.light .u { color: #1a7f37; } .win.light .d { color: #0550ae; } .win.light .pc { color: #1c1c1e; } .win.light .cmd { color: #000; font-weight: 700; }
.win.light .q { color: #6e6e76; } .win.light .in { color: #9a6700; font-weight: 700; } .win.light .hd { color: #0a7487; }
.win.light .ok { color: #1a7f37; } .win.light .err { color: #cf222e; } .win.light .dim { color: #8b8b94; } .win.light .cur { background: #1c1c1e; }
"""
_EXT = {".py": "python", ".js": "javascript", ".ts": "typescript", ".cs": "csharp", ".java": "java", ".cpp": "cpp",
        ".c": "c", ".sql": "sql", ".html": "html", ".css": "css", ".json": "json", ".sh": "bash", ".go": "go", ".rs": "rust"}


def _highlight(code, lexer):
    if not lexer:
        return esc(code)
    try:
        from pygments import highlight
        from pygments.formatters import HtmlFormatter
        from pygments.lexers import get_lexer_by_name
        return highlight(code, get_lexer_by_name(lexer), HtmlFormatter(style="monokai", noclasses=True, nowrap=True))
    except Exception:
        return esc(code)


class TechDoc(Doc):
    def __init__(self, *a, **kw):
        kw["extra_css"] = _CSS + kw.get("extra_css", "")
        super().__init__(*a, **kw)

    def _win(self, theme, title, body, font_pt):
        self.parts.append(
            f'<div class="win {theme}"><div class="tb"><span class="dots"><span class="dot r"></span><span class="dot y"></span>'
            f'<span class="dot g"></span></span><div class="ttl">{esc(title)}</div></div><pre style="font-size:{font_pt}pt">{body}</pre></div>')

    def code_window(self, code, filename="app.py", lexer=None, font_pt=8.2):
        self._win("dark", filename, _highlight(code, lexer or _EXT.get(Path(filename).suffix.lower())), font_pt)

    def terminal(self, lines, title="project — -zsh — 80×24", user="student@MacBook-Pro", cwd="project",
                 command=None, theme="dark", font_pt=7.8, show_end_prompt=True):
        """lines: None=blank | "text" | ("question","typed input") | ("@hd|@ok|@err|@dim", "text") | ("@cmd","shell command")"""
        pr = f'<span class="u">{esc(user)}</span> <span class="d">{esc(cwd)}</span> <span class="pc">%</span>'
        out = [f'{pr} <span class="cmd">{esc(command)}</span>'] if command else []
        for it in lines:
            if it is None:
                out.append("")
            elif isinstance(it, tuple) and it[0].startswith("@"):
                out.append(f'{pr} <span class="cmd">{esc(it[1])}</span>' if it[0] == "@cmd" else f'<span class="{it[0][1:]}">{esc(it[1])}</span>')
            elif isinstance(it, tuple):
                out.append(f'<span class="q">{esc(it[0])}</span> <span class="in">{esc(it[1])}</span>')
            elif str(it).startswith("--- "):
                out.append(f'<span class="hd">{esc(it)}</span>')
            else:
                out.append(esc(it))
        if show_end_prompt:
            out.append(f'{pr} <span class="cur">&nbsp;</span>')
        self._win(theme, title, "\n".join(out), font_pt)
