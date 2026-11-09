"""Drawing kit shared by gen.py: palette, embedded subset fonts, text measuring, shared CSS.

GitHub renders README images without web fonts, so every SVG embeds a subset of the fonts it
actually uses (as base64 woff2). Text is measured with the same font files so wrapping and
right-aligned layout stay exact.
"""
import base64
import io
import os
import sys
from xml.sax.saxutils import escape

from fontTools import subset
from fontTools.ttLib import TTFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from icons import ICONS  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")

# ------------------------------------------------------------------ palette
NAVY = "#233D4D"      # Storm Navy
EMBER = "#FE7F2D"     # Citrus Ember
GLACIER = "#6594B1"   # Glacier Blue
NAVY_D = "#192D3B"    # deeper navy, panels on navy
NAVY_L = "#2E4C5F"    # lighter navy, raised cards
ICE = "#EAF1F6"       # near-white with a blue cast, text on navy

# ------------------------------------------------------------------ fonts
# key -> (family, weight, file).  d = display, s/sb = body, m/mb = labels.
FONTS = {
    "d": ("Unbounded", 700, "unbounded-latin-700-normal.woff2"),
    "s": ("Instrument Sans", 400, "instrument-sans-latin-400-normal.woff2"),
    "sb": ("Instrument Sans", 600, "instrument-sans-latin-600-normal.woff2"),
    "m": ("JetBrains Mono", 500, "jetbrains-mono-latin-500-normal.woff2"),
    "mb": ("JetBrains Mono", 700, "jetbrains-mono-latin-700-normal.woff2"),
}
FALLBACK = {
    "d": '"Arial Black",Impact,sans-serif',
    "s": 'system-ui,-apple-system,"Segoe UI",Roboto,sans-serif',
    "sb": 'system-ui,-apple-system,"Segoe UI",Roboto,sans-serif',
    "m": 'ui-monospace,SFMono-Regular,Menlo,Consolas,monospace',
    "mb": 'ui-monospace,SFMono-Regular,Menlo,Consolas,monospace',
}
_USED = {}
_METRICS = {}


def _metrics(key):
    if key not in _METRICS:
        f = TTFont(os.path.join(FONT_DIR, FONTS[key][2]))
        _METRICS[key] = (f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm)
    return _METRICS[key]


def tw(s, font, size, ls=0.0):
    """Rendered width of `s` in px (advance widths + letter spacing)."""
    cmap, hmtx, upm = _metrics(font)
    total = 0
    for ch in s:
        g = cmap.get(ord(ch))
        total += hmtx[g][0] if g else upm * 0.55
    return total * size / upm + ls * len(s)


def wrap(s, font, size, maxw, ls=0.0):
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if cur and tw(trial, font, size, ls) > maxw:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def esc(s):
    return escape(str(s))


def T(x, y, s, font="s", size=14, fill="fg", anchor="start", ls=0.0, extra="", cls=""):
    """Text. `fill` is a #hex colour or the name of an adaptive class (fg, mu, ac)."""
    s = str(s)
    _USED.setdefault(font, set()).update(s)
    hexfill = fill.startswith(("#", "url("))
    cls = f"f{font}" + ("" if hexfill else f" {fill}") + (f" {cls}" if cls else "")
    a = f'x="{x:.1f}" y="{y:.1f}" font-size="{size}" class="{cls}"' + (f' fill="{fill}"' if hexfill else "")
    if anchor != "start":
        a += f' text-anchor="{anchor}"'
    if ls:
        a += f' letter-spacing="{ls}"'
    if extra:
        a += " " + extra
    return f"<text {a}>{esc(s)}</text>"


def icon(key, x, y, size, mono_fill=ICE, extra=""):
    vb, inner, mono = ICONS[key]
    fill = f' fill="{mono_fill}"' if mono else ""
    return f'<g transform="translate({x:.1f} {y:.1f}) scale({size / 128:.4f})"{fill} {extra}>{inner}</g>'


# ------------------------------------------------------------------ css
ANIM_CSS = """
@keyframes floaty{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
@keyframes fadeup{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
@keyframes pop{from{opacity:0;transform:scale(.6)}to{opacity:1;transform:none}}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}
@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}
@keyframes draw{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}
@keyframes rise{from{transform:scaleY(0)}to{transform:scaleY(1)}}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes sweep{0%{transform:scaleX(.08)}70%,100%{transform:scaleX(1)}}
@keyframes shimmer{from{transform:translateX(-120%)}to{transform:translateX(220%)}}
@keyframes ring{from{stroke-dashoffset:var(--len)}to{stroke-dashoffset:0}}
@keyframes dots{0%,80%,100%{opacity:.25}40%{opacity:1}}
.floaty{animation:floaty 5s ease-in-out infinite}
.fadeup{animation:fadeup .7s ease-out both}
.pop{transform-box:fill-box;transform-origin:center;animation:pop .5s cubic-bezier(.2,.9,.3,1.4) both}
.pulse{animation:pulse 2s ease-in-out infinite}
.blink{animation:blink 1.1s steps(1) infinite}
.draw{stroke-dasharray:1;animation:draw 1.6s ease-out both}
.rise{transform-box:fill-box;transform-origin:center bottom;animation:rise .9s cubic-bezier(.2,.8,.2,1) both}
.grow{transform-box:fill-box;transform-origin:left center;animation:grow 1s ease-out both}
.sweep{transform-box:fill-box;transform-origin:left center;animation:sweep 3.2s ease-in-out infinite alternate}
.shim{animation:shimmer 3.6s ease-in-out infinite}
.ring{animation:ring 1.4s ease-out both}
.dt{animation:dots 1.2s infinite}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
"""

THEME_CSS = """
.fg{fill:#233D4D}.mu{fill:#4F7690}.ac{fill:#C2570A}.acf{fill:#FE7F2D}
.sfg{stroke:#233D4D}.slm{stroke:#233D4D;stroke-opacity:.2}.ffg{fill:#233D4D}.flm{fill:#233D4D;fill-opacity:.08}
@media (prefers-color-scheme:dark){
.fg{fill:#EAF1F6}.mu{fill:#6594B1}.ac{fill:#FE7F2D}
.sfg{stroke:#EAF1F6}.slm{stroke:#EAF1F6;stroke-opacity:.2}.ffg{fill:#EAF1F6}.flm{fill:#EAF1F6;fill-opacity:.08}
}
"""


def _font_face(key):
    fam, wt, fn = FONTS[key]
    chars = "".join(sorted(_USED.get(key, set()) | {" "}))
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga"]
    opts.notdef_outline = True
    f = TTFont(os.path.join(FONT_DIR, fn))
    sub = subset.Subsetter(opts)
    sub.populate(text=chars)
    sub.subset(f)
    f.flavor = "woff2"
    buf = io.BytesIO()
    f.save(buf)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return (f'@font-face{{font-family:"{fam}";font-weight:{wt};src:url(data:font/woff2;base64,{b64}) format("woff2")}}'
            f'.f{key}{{font-family:"{fam}",{FALLBACK[key]};font-weight:{wt}}}')


def svg(w, h, body, label, defs="", extra_css="", attrs=""):
    """Wrap a body into a complete SVG. Embeds only the glyphs that were drawn since the last call."""
    faces = "".join(_font_face(k) for k in FONTS if k in _USED)
    _USED.clear()
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
        f'aria-label="{esc(label)}"{(" " + attrs) if attrs else ""}>\n<title>{esc(label)}</title>\n'
        f"<style>{faces}{THEME_CSS}{ANIM_CSS}{extra_css}</style>\n<defs>{defs}</defs>\n{body}\n</svg>\n"
    )
