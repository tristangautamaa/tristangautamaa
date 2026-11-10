"""Hero banner, link pills, 'now' bar and section headings."""
import data as D
from svgkit import EMBER, GLACIER, ICE, NAVY, NAVY_D, NAVY_L, T, icon, svg, tw

W = 800
L, R = 12, 788


# ------------------------------------------------------------------ headings (adaptive light/dark)
def heading(num, label, title, note, y=0):
    """Eyebrow + display title + underline. Returns (markup, next_y)."""
    tws = tw(title, "d", 26)
    out = [
        T(L, y + 14, f"{num} / {label}", "mb", 11, "ac", ls=3),
        T(L, y + 50, title, "d", 26, "fg"),
        T(R, y + 48, note, "s", 13, "mu", "end"),
        f'<rect x="{L}" y="{y + 62}" width="{R - L}" height="1.5" class="slm" fill="none"/>',
        f'<rect x="{L}" y="{y + 61.5}" width="{tws:.0f}" height="2.5" rx="1" class="acf"/>',
    ]
    return "\n".join(out), y + 92


def heading_svg(num, label, title, note):
    body, h = heading(num, label, title, note)
    return svg(W, h - 16, body, f"{num} {label}: {title}")


# ------------------------------------------------------------------ hero
def hero():
    b = []
    stats = [(f"{D.TOTAL:,}", "CONTRIBS · 12M"), (f"{D.ACTIVE}", "ACTIVE DAYS"), (f"{D.PUBLIC_REPOS}", "PUBLIC REPOS"), (f"{D.LONGEST}", "DAY STREAK")]
    size = round(min(84, 716 / tw("Tristan Gautama", "d", 1)), 1)
    y_eyebrow = 106
    y_name = y_eyebrow + size + 22
    y_sub = y_name + 52
    y_cards = y_sub + 52
    H = int(y_cards + 56 + 30)
    defs = (
        f'<clipPath id="hc"><rect width="{W}" height="{H}" rx="18"/></clipPath>'
        f'<pattern id="hg" width="34" height="34" patternUnits="userSpaceOnUse"><path d="M34 0H0V34" fill="none" stroke="{GLACIER}" stroke-opacity=".10"/></pattern>'
        f'<radialGradient id="hE"><stop offset="0" stop-color="{EMBER}" stop-opacity=".62"/><stop offset="1" stop-color="{EMBER}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="hG"><stop offset="0" stop-color="{GLACIER}" stop-opacity=".5"/><stop offset="1" stop-color="{GLACIER}" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="hT" x1="0" x2="1"><stop offset="0" stop-color="{EMBER}"/><stop offset="1" stop-color="#FFB27A"/></linearGradient>'
    )
    b.append(
        f'<g clip-path="url(#hc)"><rect width="{W}" height="{H}" fill="{NAVY}"/><rect width="{W}" height="{H}" fill="url(#hg)"/>'
        f'<circle cx="700" cy="{H}" r="400" fill="url(#hE)"/><circle cx="40" cy="10" r="330" fill="url(#hG)"/></g>'
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{GLACIER}" stroke-opacity=".35"/>'
    )
    # availability pill (top-left)
    pill = "Data Analyst Intern · Kawan Lama Group"
    pw = tw(pill, "m", 10.5) + 40
    b.append(f'<rect x="28" y="28" width="{pw:.0f}" height="28" rx="14" fill="{ICE}" fill-opacity=".06" stroke="{ICE}" stroke-opacity=".2"/>')
    b.append(f'<circle cx="44" cy="42" r="3.5" fill="{EMBER}" class="pulse"/>')
    b.append(T(56, 46, pill, "m", 10.5, ICE))
    # eyebrow + headline + subtitle
    b.append(T(28, y_eyebrow, "DATA ANALYST + PRODUCT BUILDER", "mb", 11, EMBER, ls=3))
    b.append(T(26, y_name, "Tristan ", "d", size, ICE, cls="fadeup", extra='style="animation-delay:.1s"'))
    b.append(T(26 + tw("Tristan ", "d", size), y_name, "Gautama", "d", size, "url(#hT)", cls="fadeup", extra='style="animation-delay:.25s"'))
    b.append(T(28, y_sub, "Data analyst and product builder in Jakarta.", "s", 16.5, ICE))
    b.append(T(28, y_sub + 23, "Dashboards, analytics and web apps for real businesses.", "s", 14, GLACIER))
    # stat cards across the full width
    gap = 12
    cw = (744 - 3 * gap) / 4
    for i, (n, lab) in enumerate(stats):
        x = 28 + i * (cw + gap)
        b.append(f'<g class="fadeup" style="animation-delay:{0.35 + i * 0.08:.2f}s">'
                 f'<rect x="{x:.1f}" y="{y_cards}" width="{cw:.1f}" height="56" rx="10" fill="{ICE}" fill-opacity=".055" stroke="{ICE}" stroke-opacity=".14"/>'
                 f'{T(x + 14, y_cards + 28, n, "d", 19, ICE)}{T(x + 14, y_cards + 45, lab, "m", 8.5, GLACIER, ls=1)}</g>')
    return svg(W, H, "\n".join(b), "Tristan Gautama: data analyst and product builder in Jakarta, Indonesia", defs=defs)


# ------------------------------------------------------------------ pills
def _globe(x, y, c):
    return (f'<g transform="translate({x} {y})" fill="none" stroke="{c}" stroke-width="1.4"><circle cx="8" cy="8" r="7"/>'
            f'<ellipse cx="8" cy="8" rx="3" ry="7"/><path d="M1 8h14"/></g>')


def _diamond(x, y, c):
    return f'<path transform="translate({x} {y})" d="M8 1l6 7-6 7-6-7z" fill="{c}"/>'


def pill_svg(label, kind):
    tl = tw(label, "mb", 10.5, 1.6)
    w = int(18 + 16 + 9 + tl + 18)
    h = 40
    pad = 24
    if kind == "globe":
        ic = _globe(18, 12, EMBER)
    elif kind == "diamond":
        ic = _diamond(18, 12, EMBER)
    else:
        ic = icon(kind, 18, 12, 16)
    body = (f'<g transform="translate(0 {pad})"><rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="20" fill="{NAVY}" stroke="{GLACIER}" stroke-opacity=".5"/>'
            f"{ic}{T(18 + 16 + 9, 25, label, 'mb', 10.5, ICE, ls=1.6)}</g>")
    return svg(w, h + pad + 2, body, label), w


# ------------------------------------------------------------------ now bar
def nowbar():
    H = 56
    txt = "Data Analyst Intern @ Kawan Lama Group & Business Development @ Sensify"
    body = (f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="{NAVY}" stroke="{GLACIER}" stroke-opacity=".4"/>'
            f'<rect x="12" y="12" width="56" height="32" rx="16" fill="{EMBER}"/>{T(40, 32, "NOW", "mb", 10.5, NAVY, "middle", ls=2)}'
            f'<circle cx="88" cy="28" r="4" fill="{EMBER}" class="pulse"/>{T(104, 33, txt, "s", 14, ICE)}')
    return svg(W, H, body, "Now: Data Analyst Intern at Kawan Lama Group and Business Development at Sensify")
