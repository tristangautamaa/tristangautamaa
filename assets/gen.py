#!/usr/bin/env python3
"""Generates the monochrome 'technical document' SVG sections for the profile README.

Each SVG is theme-adaptive via prefers-color-scheme and has subtle, reduced-motion-safe animation.
Usage: gen.py OUTDIR
"""
import math
import sys
from xml.sax.saxutils import escape

OUT = sys.argv[1] if len(sys.argv) > 1 else "assets"
W = 800
L, R = 8, 792
SNAPSHOT = "2026-11-09"

FONT = 'ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,"Liberation Mono","DejaVu Sans Mono",monospace'

STYLE = f"""<style>
text{{font-family:{FONT}}}
.fg{{fill:#0d1117}}.mu{{fill:#57606a}}.ac{{fill:#0f766e}}
.ln{{stroke:#0d1117}}.lm{{stroke:#8c959f}}.la{{stroke:#0f766e}}
.nf{{fill:none}}
.h0{{fill:#0d1117;fill-opacity:.07}}.h1{{fill:#0d1117;fill-opacity:.28}}.h2{{fill:#0d1117;fill-opacity:.5}}.h3{{fill:#0d1117;fill-opacity:.75}}.h4{{fill:#0d1117;fill-opacity:1}}
.tk{{fill:#0d1117;fill-opacity:.08;stroke:#0d1117;stroke-width:1}}
.bar{{fill:#0d1117}}
@media (prefers-color-scheme:dark){{
.fg{{fill:#f0f6fc}}.mu{{fill:#8b949e}}.ac{{fill:#2dd4bf}}
.ln{{stroke:#f0f6fc}}.lm{{stroke:#6e7681}}.la{{stroke:#2dd4bf}}
.h0{{fill:#f0f6fc;fill-opacity:.08}}.h1{{fill:#f0f6fc;fill-opacity:.3}}.h2{{fill:#f0f6fc;fill-opacity:.52}}.h3{{fill:#f0f6fc;fill-opacity:.76}}.h4{{fill:#f0f6fc;fill-opacity:1}}
.tk{{fill:#f0f6fc;fill-opacity:.1;stroke:#f0f6fc}}
.bar{{fill:#f0f6fc}}
}}
@keyframes flow{{to{{stroke-dashoffset:-16}}}}
@keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
@keyframes grow{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
@keyframes rise{{from{{transform:scaleY(0)}}to{{transform:scaleY(1)}}}}
.flow{{stroke-dasharray:3 5;animation:flow 1.4s linear infinite}}
.cur{{animation:blink 1.1s steps(1) infinite}}
.dot{{animation:pulse 2s ease-in-out infinite}}
.gx{{transform-box:fill-box;transform-origin:left center;animation:grow .9s ease-out both}}
.gy{{transform-box:fill-box;transform-origin:center bottom;animation:rise .9s ease-out both}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>"""


def esc(s):
    return escape(str(s))


def T(x, y, s, cls="fg", size=12, anchor="start", weight="400", ls=None, fit=True, extra=""):
    """Text. With fit=True a textLength pins the width so layout is stable across mono fonts."""
    s = str(s)
    attrs = f'x="{x}" y="{y}" class="{cls}" font-size="{size}" font-weight="{weight}"'
    if anchor != "start":
        attrs += f' text-anchor="{anchor}"'
    adv = size * 0.6 + (ls or 0)
    if ls:
        attrs += f' letter-spacing="{ls}"'
    if fit and len(s) > 1:
        attrs += f' textLength="{round(len(s) * adv - (ls or 0), 1)}" lengthAdjust="spacing"'
    if extra:
        attrs += " " + extra
    return f"<text {attrs}>{esc(s)}</text>"


def line(x1, y1, x2, y2, cls="ln", sw=1, extra=""):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cls}" stroke-width="{sw}" {extra}/>'


def rect(x, y, w, h, cls="ln nf", sw=1, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="{cls}" stroke-width="{sw}" {extra}/>'


def svg(h, body, label):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" '
        f'role="img" aria-label="{esc(label)}">\n<title>{esc(label)}</title>\n{STYLE}\n{body}\n</svg>\n'
    )


def section(num, label, tag, y):
    """'01  WHOAMI ──────── ~/01-whoami' header. Returns (svg, next_y)."""
    ls = 4
    lab_adv = 11.5 * 0.6 + ls
    lab_w = len(label) * lab_adv - ls
    tag_w = len(tag) * 10.5 * 0.6
    out = [
        T(L, y + 34, num, "fg", 40, weight="300"),
        T(L + 64, y + 27, label.upper(), "fg", 11.5, weight="700", ls=ls),
        line(L + 64 + lab_w + 16, y + 23, R - tag_w - 16, y + 23, "ln", 1),
        T(R, y + 27, tag, "mu", 10.5, anchor="end"),
    ]
    return "\n".join(out), y + 70


def strip(y, left, right):
    return "\n".join(
        [
            T(L, y, left, "fg", 10.5, weight="600", ls=2),
            T(R, y, right, "fg", 10.5, weight="600", ls=2, anchor="end"),
            line(L, y + 10, R, y + 10, "ln", 1.2),
        ]
    )


# ---------------------------------------------------------------- header
def header():
    b = []
    b.append(strip(26, "PORTFOLIO — INDEX Nº 001", "JAKARTA, ID — 6.21° S"))
    name = "Tristan Gautama"
    b.append(T(L, 122, name, "fg", 64, weight="500", fit=False, extra=f'textLength="{round(len(name) * 64 * 0.6, 1)}" lengthAdjust="spacing"'))
    cx = L + len(name) * 64 * 0.6 + 12
    b.append(f'<rect x="{round(cx, 1)}" y="78" width="26" height="46" class="ac cur"/>')
    b.append(T(L + 2, 158, "Software, Data & Geospatial ML — Jakarta, Indonesia.", "fg", 16, weight="700"))
    for yy, k, v in ((198, "focus", "web & full-stack · geospatial ML · data analysis · AI-integrated products"),
                     (220, "now", "co-founder @ ATS · data analyst intern @ Kawan Lama Group · researcher")):
        b.append(T(L + 2, yy, k, "mu", 11.5))
        b.append(T(L + 52, yy, "▸", "mu", 11.5))
        b.append(T(L + 78, yy, v, "fg", 11.5))
    b.append(line(L, 246, R, 246, "lm", 1))
    cols = ["WEB & FULL-STACK", "GEOSPATIAL ML", "DATA ANALYSIS"]
    x = L
    for c in cols:
        w = len(c) * (10 * 0.6 + 2) - 2
        b.append(T(x, 270, c, "fg", 10, weight="600", ls=2))
        x += w + 16
        if c != cols[-1]:
            b.append(f'<circle cx="{x:.1f}" cy="266.5" r="1.6" class="mu"/>')
        x += 16
    b.append(T(R, 270, "UMN — JAKARTA", "fg", 10, weight="600", ls=2, anchor="end"))
    return svg(292, "\n".join(b), "Tristan Gautama — Software, Data and Geospatial ML, Jakarta, Indonesia")


# ---------------------------------------------------------------- whoami
def whoami():
    s, y = section("01", "whoami", "~/01-whoami", 0)
    b = [s]
    y += 14
    lines = [
        "student at multimedia nusantara university, jakarta.",
        "co-founder of architech technology solutions — custom software for businesses in indonesia.",
        "researching geospatial ML to decide where renewable-energy access should go first.",
    ]
    for i, t in enumerate(lines):
        b.append(T(L + 2, y + i * 24, t, "fg", 12.5))
    y += 24 * 3 + 6
    b.append(line(L, y, R, y, "lm", 1))
    y += 30
    rows = [
        ("FOCUS", "web & full-stack · geospatial ML · data analysis · AI-integrated products"),
        ("NOW", "data analyst intern, kawan lama group · business development, sensify"),
        ("BUILDING", "custom software at ATS · energy-access decision support · products for clients"),
        ("BASE", "jakarta, indonesia · multimedia nusantara university"),
    ]
    for i, (k, v) in enumerate(rows):
        yy = y + i * 29
        b.append(T(L + 2, yy, k, "mu", 10, weight="600", ls=2))
        b.append(T(L + 130, yy, v, "fg", 12))
    h = y + 4 * 29 + 4
    return svg(h, "\n".join(b), "About Tristan: student, co-founder of ATS, geospatial ML researcher, data analyst intern")


# ---------------------------------------------------------------- ecosystem
HUB_W, HUB_H = 200, 52
CLUSTERS = [
    # title, items (name, desc), center x, center y (before offset), width
    ("RESEARCH & GEOSPATIAL", [("research", "geospatial ML"), ("energy-dss", "decision support")], 140, 120, 250),
    ("COMPANY", [("architech", "custom software")], 400, 104, 240),
    ("AI & DATA", [("speak", "AI coach"), ("stock-alert", "WhatsApp alerts"), ("diabetes-ml", "scikit-learn")], 660, 120, 250),
    ("INTERNAL TOOLS", [("seaport", "freight tariffs"), ("nawarx", "OOH pricing")], 140, 462, 250),
    ("MOBILE & EARLY WORK", [("zeat-app", "Flutter"), ("zero-eat", "Laravel")], 400, 470, 240),
    ("CLIENT PLATFORMS", [("migravia", "immigration"), ("sensify", "AI storefront"), ("griyaplast", "manufacturer"),
                          ("pph-website", "padel venue"), ("giseu", "fashion")], 660, 472, 250),
]


def edge(cx, cy, w, h, tx, ty):
    dx, dy = tx - cx, ty - cy
    if dx == 0 and dy == 0:
        return cx, cy
    sx = (w / 2) / abs(dx) if dx else float("inf")
    sy = (h / 2) / abs(dy) if dy else float("inf")
    t = min(sx, sy)
    return cx + dx * t, cy + dy * t


def ecosystem():
    s, y = section("02", "system map", "~/02-ecosystem", 0)
    b = [s]
    y0 = y + 6
    b.append(strip(y0, "SYSTEM MAP — PUBLIC AND CLIENT WORK, ONE PIPELINE", "FIG. 01"))
    off = 31
    hx, hy = 400, 300 + off
    geo = []
    for title, items, cx, cy, w in CLUSTERS:
        h = 34 + 16 * len(items) + 6
        geo.append((title, items, cx, cy + off, w, h))
    for title, items, cx, cy, w, h in geo:
        x1, y1 = edge(hx, hy, HUB_W, HUB_H, cx, cy)
        x2, y2 = edge(cx, cy, w, h, hx, hy)
        b.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="lm" stroke-width="1"/>')
        b.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="la flow" stroke-width="1.2"/>')
    b.append(rect(hx - HUB_W / 2, hy - HUB_H / 2, HUB_W, HUB_H, "ln nf", 1.6))
    b.append(T(hx, hy - 3, "TRISTAN.SYS", "fg", 14, "middle", "700", ls=1.5))
    b.append(T(hx, hy + 16, "builder · analyst · researcher", "mu", 9.5, "middle"))
    ymax = 0
    for title, items, cx, cy, w, h in geo:
        x0, y_0 = cx - w / 2, cy - h / 2
        b.append(rect(x0, y_0, w, h, "ln nf", 1))
        b.append(T(x0 + 12, y_0 + 20, title, "fg", 9.5, weight="700", ls=1.5))
        for i, (n, d) in enumerate(items):
            yy = y_0 + 40 + 16 * i
            b.append(T(x0 + 12, yy, n, "fg", 10.5, weight="600"))
            b.append(T(x0 + w - 12, yy, d, "mu", 9, "end"))
        ymax = max(ymax, y_0 + h)
    ybot = ymax + 26
    b.append(line(L, ybot, R, ybot, "lm", 1))
    b.append(T(R, ybot + 20, "DASHED LINES — IDEAS IN MOTION", "mu", 9.5, "end", ls=2))
    return svg(int(ybot + 34), "\n".join(b), "System map: Tristan's projects grouped into research and geospatial, company, AI and data, internal tools, mobile and early work, and client platforms")


# ---------------------------------------------------------------- projects
PROJECTS = [
    ("ENERGY ACCESS PLANNER", "live",
     ["Decision-support dashboard ranking Indonesia's 514 districts for renewable-energy access programs.",
      "Blends night-time light, poverty, road access and terrain into a 0–100 access disadvantage index."],
     "JAVASCRIPT · MAPLIBRE GL · GEOJSON · DECISION SUPPORT"),
    ("MIGRAVIA", "live",
     ["Immigration-services platform for visa, KITAS and KITAP cases in Indonesia.",
      "Company website, WhatsApp-first intake and a client portal with case tracking and renewal alerts."],
     "REACT · VITE · TYPESCRIPT · TAILWIND · WHATSAPP"),
    ("SENSIFY", "live",
     ["AI-powered storefront for Indonesian brands: an owned official website beside the marketplace.",
      "Cinematic interactive homepage with a shader-gradient hero."],
     "REACT · VITE · THREE.JS · TAILWIND"),
    ("SEAPORT — VENDOR EKSPEDISI KLG", "internal",
     ["Internal freight-tariff portal: imports vendor RFQ spreadsheets and matches them to master data.",
      "Keeps monthly rates with full revision history and compares vendors lane by lane."],
     "NEXT.JS · REACT · TAILWIND · RADIX UI · SHEETJS"),
    ("NAWARX", "internal",
     ["Billboard (OOH) intelligence tool: price database, price calculator and negotiation advisor.",
      "Benchmarks quotes against deal history and maps nearby sites and vendors."],
     "VITE · TYPESCRIPT · LEAFLET · SUPABASE · PYTHON"),
    ("GRIYAPLAST", "live",
     ["Website for a plastic household-goods manufacturer with a product catalog and wholesale ordering.",
      "WhatsApp ordering and a shipping-cost estimator built in."],
     "NEXT.JS · TYPESCRIPT · WHATSAPP"),
    ("PONCOL PADEL HOUSE", "live",
     ["Website for a padel venue with scroll-driven animation and a responsive Next.js front end."],
     "NEXT.JS · TYPESCRIPT · FRAMER MOTION · GSAP"),
    ("GISEU", None,
     ["Editorial fashion site in a quiet-luxury, modern-Japanese-minimal style.",
      "One continuous smooth-scrolling page with a fullscreen rolling-text navigation."],
     "VITE · REACT · TYPESCRIPT · FRAMER MOTION · GSAP · LENIS"),
    ("SPEAK", None,
     ["AI communication coach for speaking with calm confidence.",
      "Live transcription, AI coaching feedback and communication metrics tracked over time."],
     "NEXT.JS · TYPESCRIPT · PYTHON · AI"),
    ("STOCK AI WHATSAPP ALERT", None,
     ["Private AI-assisted stock research system that analyzes stocks daily.",
      "Rule-based signal scoring with optional AI enrichment, delivered as WhatsApp alerts. It never trades."],
     "PYTHON · FASTAPI · DOCKER · WHATSAPP"),
    ("ZEAT APP", None,
     ["Food-ordering app: menu, cart, pickup and delivery tracking, admin dashboard and a chatbot."],
     "FLUTTER · DART · FIREBASE"),
    ("DIABETES PREDICTION", None,
     ["Comparison of machine-learning algorithms for diabetes prediction with class-imbalance handling.",
      "Streamlit front end for exploring the results."],
     "PYTHON · PANDAS · SCIKIT-LEARN · STREAMLIT"),
    ("ZERO-EAT", None,
     ["Laravel web app with user registration, login, profiles and a product catalog."],
     "LARAVEL · PHP · BLADE · TAILWIND"),
]


def projects():
    s, y = section("03", "projects", "~/03-projects", 0)
    b = [s]
    y += 14
    for i, (title, tag, desc, tags) in enumerate(PROJECTS, 1):
        b.append(T(L + 2, y + 14, f"{i:02d} / {title}", "fg", 13, weight="700"))
        if tag == "live":
            b.append(f'<circle cx="{R - 42}" cy="{y + 10.5}" r="3" class="ac dot"/>')
            b.append(T(R, y + 14, "LIVE", "ac", 9.5, "end", "700", ls=2))
        elif tag == "internal":
            b.append(T(R, y + 14, "INTERNAL", "mu", 9.5, "end", "700", ls=2))
        for j, d in enumerate(desc):
            b.append(T(L + 2, y + 36 + j * 17, d, "fg", 11.2))
        ty = y + 36 + len(desc) * 17 + 6
        b.append(T(L + 2, ty, tags, "mu", 9.5, ls=1))
        y = ty + 16
        b.append(line(L, y, R, y, "lm" if i < len(PROJECTS) else "ln", 1))
        y += 22
    return svg(int(y - 10), "\n".join(b), "Selected projects: Energy Access Planner, Migravia, Sensify, Seaport, NawarX, Griyaplast, Poncol Padel House, GISEU, SPEAK, Stock AI WhatsApp Alert, ZEAT app, diabetes prediction, Zero-EAT")


# ---------------------------------------------------------------- telemetry
YEARS = [("2021", 2), ("2022", 2), ("2023", 2), ("2024", 43), ("2025", 264), ("2026", 2323)]
LANGS = [("JavaScript", 36.9), ("TypeScript", 18.2), ("Python", 15.5), ("CSS", 6.2),
         ("Jupyter", 5.7), ("Blade", 4.6), ("PHP", 4.5), ("C++", 1.8)]
LEVELS_2026 = "00000000000000000000000100110000000011202002000000000000000000000010100100001001111211110124112220000000000000000000000100001000101101111001012442220000000000000000000000000011000010210011110111224213000000000000000000000001000010101100211011111113343440000000000000000000000000000101010021111220210142241200000000000000001000000000011011000000000001011100040000000"
MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
MDAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def telemetry():
    s, y = section("04", "telemetry", "~/04-telemetry", 0)
    b = [s]
    y += 8
    # KPI strip
    kp = [("2,323", "CONTRIBUTIONS · 2026"), ("114", "ACTIVE DAYS · 2026"), ("1,093", "PEAK MONTH · OCT 2026"), ("14", "PUBLIC REPOS")]
    cw = (R - L) / 4
    b.append(rect(L, y, R - L, 78, "ln nf", 1))
    for i, (n, lab) in enumerate(kp):
        x = L + i * cw
        if i:
            b.append(line(x, y + 12, x, y + 66, "lm", 1))
        b.append(T(x + 18, y + 42, n, "fg", 30, weight="300"))
        b.append(T(x + 18, y + 62, lab, "mu", 9, ls=1.2))
    y += 78 + 26

    # two panels
    pw = (R - L - 24) / 2
    # left: yearly
    b.append(T(L, y, "CONTRIBUTIONS / YEAR", "fg", 10.5, weight="700", ls=2))
    b.append(line(L, y + 9, L + pw, y + 9, "ln", 1))
    base = y + 168
    maxv = max(v for _, v in YEARS)
    bw = 34
    gap = (pw - len(YEARS) * bw) / (len(YEARS) + 1)
    for i, (yr, v) in enumerate(YEARS):
        x = L + gap + i * (bw + gap)
        h = max(2.0, 118 * v / maxv)
        b.append(f'<rect x="{x:.1f}" y="{base - h:.1f}" width="{bw}" height="{h:.1f}" class="bar gy" style="animation-delay:{i * 0.08:.2f}s"/>')
        b.append(T(x + bw / 2, base - h - 8, f"{v:,}", "fg", 10, "middle", "600"))
        b.append(T(x + bw / 2, base + 16, yr, "mu", 9.5, "middle"))
    b.append(line(L, base + 3, L + pw, base + 3, "lm", 1))
    b.append(T(L, base + 36, "trend — accelerating", "mu", 9.5))

    # right: languages
    rx = L + pw + 24
    b.append(T(rx, y, "LANGUAGES / PUBLIC REPOS", "fg", 10.5, weight="700", ls=2))
    b.append(line(rx, y + 9, R, y + 9, "ln", 1))
    track_x = rx + 92
    track_w = pw - 92 - 52
    for i, (lg, pct) in enumerate(LANGS):
        yy = y + 36 + i * 20
        b.append(T(rx, yy, lg.upper(), "fg", 9.5, weight="600", ls=0.8))
        b.append(rect(track_x, yy - 10, track_w, 12, "ln nf", 1))
        b.append(f'<rect x="{track_x}" y="{yy - 10}" width="{track_w * pct / 40:.1f}" height="12" class="bar gx" style="animation-delay:{i * 0.07:.2f}s"/>')
        b.append(T(R, yy, f"{pct:.1f}%", "mu", 9.5, "end"))
    y = base + 36 + 34

    # heatmap
    b.append(T(L, y, "DAILY ACTIVITY — 2026", "fg", 10.5, weight="700", ls=2))
    b.append(line(L, y + 9, R, y + 9, "ln", 1))
    gx0, gy0 = L + 34, y + 46
    pitch, cell = 13.7, 11
    start_dow = 4  # 2026-01-01 is a Thursday
    for i, ch in enumerate(LEVELS_2026):
        col, row = (i + start_dow) // 7, (i + start_dow) % 7
        b.append(f'<rect x="{gx0 + col * pitch:.1f}" y="{gy0 + row * pitch:.1f}" width="{cell}" height="{cell}" rx="1.5" class="h{ch}"/>')
    # month labels
    d = 0
    for m in range(12):
        col = (d + start_dow) // 7
        b.append(T(gx0 + col * pitch, y + 32, MONTHS[m], "mu", 8.5, ls=1))
        d += MDAYS[m]
    for r_, lab in ((1, "MON"), (3, "WED"), (5, "FRI")):
        b.append(T(L, gy0 + r_ * pitch + 9, lab, "mu", 8.5, ls=1))
    yb = gy0 + 7 * pitch + 14
    # legend
    lx = R - 5 * 16 - 62
    b.append(T(lx - 8, yb + 9, "LESS", "mu", 8.5, "end", ls=1))
    for k in range(5):
        b.append(f'<rect x="{lx + k * 16}" y="{yb}" width="11" height="11" rx="1.5" class="h{k}"/>')
    b.append(T(lx + 5 * 16 + 4, yb + 9, "MORE", "mu", 8.5, ls=1))
    b.append(T(L, yb + 9, f"snapshot {SNAPSHOT} · includes private repositories · counts only", "mu", 9))
    return svg(int(yb + 30), "\n".join(b), "GitHub telemetry: 2,323 contributions in 2026, yearly growth, language mix of public repos and a daily activity heatmap")


# ---------------------------------------------------------------- route
def route():
    s, y = section("05", "the route", "~/05-journey", 0)
    b = [s]
    y += 6
    b.append(strip(y, "THE ROUTE SO FAR", "FIG. 02"))
    ay = y + 92
    pts = [
        (104, "2021", "github account created", "up"),
        (224, "2024", "first public projects", "down"),
        (344, "2025", "ML + mobile apps", "up"),
        (464, "FEB 2026", "kawan lama group", "down"),
        (584, "MAY 2026", "sensify · client platforms", "up"),
        (684, "OCT 2026", "energy-dss · peak month", "down"),
    ]
    b.append(line(L, ay, R - 14, ay, "ln", 1.4))
    b.append(f'<path d="M{R - 14} {ay - 5} L{R - 4} {ay} L{R - 14} {ay + 5}" class="ln nf" stroke-width="1.4"/>')
    for x, yr, lab, side in pts:
        b.append(f'<circle cx="{x}" cy="{ay}" r="4" class="fg"/>')
        if side == "up":
            b.append(line(x, ay - 6, x, ay - 24, "lm", 1))
            b.append(T(x, ay - 48, yr, "fg", 10.5, "middle", "700", ls=1))
            b.append(T(x, ay - 32, lab, "mu", 9.5, "middle"))
        else:
            b.append(line(x, ay + 6, x, ay + 24, "lm", 1))
            b.append(T(x, ay + 40, yr, "fg", 10.5, "middle", "700", ls=1))
            b.append(T(x, ay + 54, lab, "mu", 9.5, "middle"))
    # now marker
    b.append(f'<circle cx="772" cy="{ay}" r="4" class="ac dot"/>')
    b.append(line(772, ay - 6, 772, ay - 24, "lm", 1))
    b.append(T(R, ay - 48, "NOW", "ac", 10.5, "end", "700", ls=1))
    b.append(T(R, ay - 32, "ATS · research", "mu", 9.5, "end"))
    y = ay + 84
    b.append(line(L, y, R, y, "ln", 1.2))
    b.append(T(L, y + 24, "EXPERIENCE", "fg", 10.5, weight="700", ls=2))
    rows = [
        ("FEB 2026 – FEB 2027", "Data Analyst Intern", "Kawan Lama Group",
         "operations officer Feb – Apr 2026, data analyst from May 2026"),
        ("MAY 2026 – NOW", "Business Development Representative", "Sensify",
         "part-time · AI-powered storefronts for growing brands"),
        ("ONGOING", "Co-founder", "Architech Technology Solutions",
         "custom software company in Indonesia"),
        ("EDUCATION", "Student", "Multimedia Nusantara University",
         "Jakarta, Indonesia"),
    ]
    y += 52
    for i, (per, role, org, sub) in enumerate(rows):
        yy = y + i * 50
        b.append(T(L + 2, yy, per, "mu", 9.5, weight="600", ls=1))
        b.append(T(L + 180, yy, role, "fg", 12.5, weight="700"))
        b.append(T(L + 180, yy + 17, f"{org} — {sub}", "mu", 10.5))
        if i < len(rows) - 1:
            b.append(line(L, yy + 31, R, yy + 31, "lm", 0.8))
    h = y + len(rows) * 50 - 6
    return svg(h, "\n".join(b), "Timeline and experience: Kawan Lama Group data analyst intern, Sensify business development, Architech co-founder, Multimedia Nusantara University student")


# ---------------------------------------------------------------- stack
def stack():
    s, y = section("06", "stack", "~/06-stack", 0)
    b = [s]
    y += 10
    rows = [
        ("LANGUAGES", "JavaScript · TypeScript · Python · Java · PHP · Dart"),
        ("WEB", "React · Next.js · Vite · Tailwind CSS · Radix UI · Three.js · Framer Motion · GSAP · Lenis"),
        ("MOBILE", "Flutter · Firebase"),
        ("BACKEND", "FastAPI · Laravel · Supabase · Docker"),
        ("DATA & ML", "pandas · scikit-learn · imbalanced-learn · Streamlit · Jupyter · SheetJS"),
        ("GEOSPATIAL", "MapLibre GL · Leaflet · GeoJSON · district-level spatial indices"),
        ("TOOLING", "Git · GitHub · Vercel · Claude"),
    ]
    x0 = L + 130
    top = y
    for i, (k, v) in enumerate(rows):
        yy = y + 14 + i * 28
        b.append(T(L + 2, yy, k, "mu", 10, weight="600", ls=2))
        b.append(T(x0 + 16, yy, v, "fg", 12))
    b.append(line(x0, top, x0, y + 14 + (len(rows) - 1) * 28 + 10, "ln", 1))
    h = y + 14 + (len(rows) - 1) * 28 + 22
    return svg(h, "\n".join(b), "Technical stack: JavaScript, TypeScript, Python, React, Next.js, Flutter, FastAPI, pandas, scikit-learn, MapLibre GL")


# ---------------------------------------------------------------- footer
def footer():
    b = []
    b.append(line(L, 10, R, 10, "ln", 1.2))
    b.append(f'<circle cx="{L + 14}" cy="42" r="9" class="nf ln" stroke-width="1.2"/>')
    b.append(f'<circle cx="{L + 14}" cy="42" r="4" class="ac dot"/>')
    b.append(T(L + 36, 38, "STATUS — BUILDING", "fg", 10.5, weight="700", ls=2))
    b.append(T(L + 36, 56, "forever learning.", "mu", 11))
    b.append(T(R, 38, "tristangautama.xyz  ·  Jakarta, ID  ·  © 2026", "fg", 11, "end"))
    return svg(72, "\n".join(b), "Status: building. Forever learning. tristangautama.xyz, Jakarta, Indonesia")


if __name__ == "__main__":
    import os
    os.makedirs(OUT, exist_ok=True)
    files = {
        "header.svg": header(), "whoami.svg": whoami(), "ecosystem.svg": ecosystem(),
        "projects.svg": projects(), "telemetry.svg": telemetry(), "route.svg": route(),
        "stack.svg": stack(), "footer.svg": footer(),
    }
    for n, c in files.items():
        with open(os.path.join(OUT, n), "w", encoding="utf-8") as f:
            f.write(c)
        print(n, len(c))
