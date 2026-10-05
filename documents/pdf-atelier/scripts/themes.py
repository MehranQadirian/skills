"""
themes.py - perceptual (OKLCH) palette engine.

Every theme is *generated*, not hand-picked: a tonal scale built in OKLCH (so equal lightness steps
look equally light in every hue), then each text/background pair is audited against WCAG contrast
and nudged until it passes. Result: any hue gives a balanced, readable, print-safe palette.

    from themes import get_theme, Theme, THEME_NAMES
    t = get_theme("ocean")                 # curated
    t = Theme.from_hex("#0f766e")          # derive a whole palette from a brand colour
    t = Theme.make("mine", brand_hue=260, accent_hue=85)   # navy + gold style (two hues)
    t.audit()                              # [(label, ratio, minimum, passed), ...]
"""
from __future__ import annotations
import math

# ----------------------------------------------------------------------------- colour maths
def _srgb_to_lin(v):  return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
def _lin_to_srgb(v):  return 12.92 * v if v <= 0.0031308 else 1.055 * (max(v, 0) ** (1 / 2.4)) - 0.055

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

def rgb_to_hex(r, g, b):
    return "#" + "".join(f"{max(0, min(255, round(v * 255))):02x}" for v in (r, g, b))

def oklch_to_rgb_lin(L, C, h):
    a, b = C * math.cos(math.radians(h)), C * math.sin(math.radians(h))
    l_, m_, s_ = L + 0.3963377774 * a + 0.2158037573 * b, L - 0.1055613458 * a - 0.0638541728 * b, L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    return (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
            -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
            -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)

def oklch(L, C, h):
    """OKLCH -> hex, reducing chroma until the colour fits the sRGB gamut."""
    c = C
    for _ in range(60):
        rgb = oklch_to_rgb_lin(L, c, h)
        if all(-0.0004 <= v <= 1.0004 for v in rgb):
            break
        c *= 0.95
    return rgb_to_hex(*[_lin_to_srgb(min(1, max(0, v))) for v in rgb])

def hex_to_oklch(hx):
    r, g, b = [_srgb_to_lin(v) for v in hex_to_rgb(hx)]
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = l ** (1 / 3), m ** (1 / 3), s ** (1 / 3)
    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    bb = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    return L, math.hypot(a, bb), (math.degrees(math.atan2(bb, a)) % 360)

def luminance(hx):
    r, g, b = [_srgb_to_lin(v) for v in hex_to_rgb(hx)]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

def _fit(L, C, h, against, minimum, step=-0.01, floor=0.05, ceil=0.98):
    """Move lightness (step<0 = darker, >0 = lighter) until contrast with `against` >= minimum."""
    for _ in range(80):
        hx = oklch(L, C, h)
        if contrast(hx, against) >= minimum:
            return hx
        L = min(ceil, max(floor, L + step))
    return oklch(L, C, h)

# ----------------------------------------------------------------------------- theme
class Theme:
    def __init__(self, name: str, t: dict):
        self.name, self.t = name, t

    def __getitem__(self, k):  return self.t[k]

    @classmethod
    def make(cls, name, brand_hue, accent_hue=None, chroma=1.0, neutral_chroma=0.012,
             brand_L=0.28, accent_L=0.56, warm=0.0):
        """
        brand_hue   hue (0-360, OKLCH) of the dark brand colour (hero, headings)
        accent_hue  hue of the accent (numbers, bars, chips); defaults to brand_hue
        chroma      saturation multiplier (0 = greyscale ... 1.3 = vivid)
        warm        shifts neutrals toward warm paper tones (0..1)
        """
        ah = brand_hue if accent_hue is None else accent_hue
        nh = brand_hue if warm == 0 else (brand_hue * (1 - warm) + 75 * warm)
        k = chroma
        white = "#ffffff"
        brand = _fit(brand_L, 0.10 * k, brand_hue, white, 9.0)
        accent = _fit(accent_L, 0.17 * k, ah, white, 4.6)
        accent_soft = oklch(0.955, 0.028 * k, ah)
        accent_text = _fit(0.46, 0.15 * k, ah, accent_soft, 5.5)
        ink = _fit(0.22, neutral_chroma * 1.5, nh, white, 14)
        text = _fit(0.32, neutral_chroma * 1.5, nh, white, 10)
        muted = _fit(0.54, neutral_chroma * 1.2, nh, white, 4.6)
        surface = oklch(0.978, neutral_chroma * 0.7, nh)
        surface2 = oklch(0.958, neutral_chroma, nh)
        line = oklch(0.925, neutral_chroma, nh)
        line_strong = oklch(0.875, neutral_chroma * 1.2, nh)
        hero_tag = _fit(0.80, 0.09 * k, ah, brand, 4.6, step=+0.01)
        hero_sub = _fit(0.88, 0.04 * k, brand_hue, brand, 7.0, step=+0.01)
        # semantic colours: fixed hues, same tonal rules, so they sit well with every theme
        def semantic(h):
            return dict(bg=oklch(0.972, 0.030 * max(k, .7), h), line=oklch(0.86, 0.075 * max(k, .7), h),
                        bar=oklch(0.60, 0.17 * max(k, .7), h), text=_fit(0.40, 0.12, h, oklch(0.972, 0.03, h), 6.5))
        sem = dict(warn=semantic(75), ok=semantic(152), bad=semantic(27), info=dict(
            bg=accent_soft, line=oklch(0.86, 0.06 * k, ah), bar=accent, text=accent_text))
        # categorical series for charts / tags: 6 hues, equal L & C
        series = [oklch(0.60, 0.13 * max(k, .6), (ah + 55 * i) % 360) for i in range(6)]
        series_soft = [oklch(0.94, 0.04 * max(k, .6), (ah + 55 * i) % 360) for i in range(6)]
        return cls(name, dict(brand=brand, accent=accent, accent_soft=accent_soft, accent_text=accent_text,
                              ink=ink, text=text, muted=muted, surface=surface, surface2=surface2, line=line,
                              line_strong=line_strong, hero_tag=hero_tag, hero_sub=hero_sub, sem=sem,
                              series=series, series_soft=series_soft, white=white,
                              mono_bg=surface2, mono_fg=_fit(0.42, 0.13 * k, (ah + 330) % 360, surface2, 6.0)))

    @classmethod
    def from_hex(cls, hx, name="custom", **kw):
        L, C, h = hex_to_oklch(hx)
        return cls.make(name, brand_hue=h, chroma=min(1.4, max(0.2, C / 0.15)), **kw)

    def audit(self):
        t, out = self.t, []
        def chk(label, fg, bg, mn):
            r = contrast(fg, bg); out.append((label, round(r, 2), mn, r >= mn))
        chk("white on brand", "#ffffff", t["brand"], 7)
        chk("white on accent (number badges)", "#ffffff", t["accent"], 4.5)
        chk("accent_text on accent_soft (chips)", t["accent_text"], t["accent_soft"], 4.5)
        chk("body text on white", t["text"], "#ffffff", 7)
        chk("muted on white", t["muted"], "#ffffff", 4.5)
        chk("muted on surface", t["muted"], t["surface"], 4.5)
        chk("hero subtitle on brand", t["hero_sub"], t["brand"], 4.5)
        chk("hero tag on brand", t["hero_tag"], t["brand"], 4.5)
        for k, s in t["sem"].items():
            chk(f"{k} text on {k} bg", s["text"], s["bg"], 4.5)
        return out


# ----------------------------------------------------------------------------- curated library
# (name, kwargs, mood / when to use)
_CURATED = [
    ("indigo",    dict(brand_hue=268),                                   "default; education, tech, product docs"),
    ("ocean",     dict(brand_hue=240, accent_hue=225, brand_L=0.30),     "trustworthy blue; corporate, reports, finance"),
    ("executive", dict(brand_hue=258, accent_hue=82, chroma=0.9, brand_L=0.25, accent_L=0.60), "navy + gold; proposals, legal, premium"),
    ("teal",      dict(brand_hue=195, accent_hue=190, brand_L=0.30),     "calm and clean; health, science, wellness"),
    ("emerald",   dict(brand_hue=162, accent_hue=158),                   "fresh; sustainability, growth, nutrition"),
    ("forest",    dict(brand_hue=148, accent_hue=140, chroma=0.8, brand_L=0.28, warm=0.25), "earthy; nature, outdoors, organic"),
    ("sunset",    dict(brand_hue=40,  accent_hue=48, brand_L=0.30, accent_L=0.60, warm=0.3), "warm orange; events, food, creative"),
    ("crimson",   dict(brand_hue=22,  accent_hue=25, brand_L=0.28),      "bold red; urgent, sports, awards"),
    ("rose",      dict(brand_hue=355, accent_hue=5,  chroma=0.95),       "soft magenta-rose; lifestyle, beauty, kids"),
    ("violet",    dict(brand_hue=300, accent_hue=305),                   "creative purple; design, arts, music"),
    ("graphite",  dict(brand_hue=255, accent_hue=255, chroma=0.18, neutral_chroma=0.006, accent_L=0.50), "neutral grey; minimal, formal, print-first"),
    ("paper",     dict(brand_hue=60,  accent_hue=45, chroma=0.55, brand_L=0.30, accent_L=0.52, warm=0.8), "warm sepia; essays, literature, long reading"),
]
THEME_NAMES = [n for n, _, _ in _CURATED]
THEME_MOODS = {n: m for n, _, m in _CURATED}
_CACHE: dict[str, Theme] = {}

def get_theme(name: str = "indigo") -> Theme:
    if name not in _CACHE:
        kw = {n: k for n, k, _ in _CURATED}.get(name)
        if kw is None:
            raise KeyError(f"unknown theme {name!r}; choose from {THEME_NAMES} or use Theme.from_hex()")
        _CACHE[name] = Theme.make(name, **kw)
    return _CACHE[name]

if __name__ == "__main__":
    bad = 0
    for n in THEME_NAMES:
        for label, r, mn, ok in get_theme(n).audit():
            if not ok:
                bad += 1; print(f"FAIL {n:10s} {label}: {r} < {mn}")
    print("all themes pass contrast audit" if not bad else f"{bad} failures")
