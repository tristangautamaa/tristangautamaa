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
def _chip(x, y, key, label, delay, dur):
    w = 14 + 18 + 8 + tw(label, "sb", 12.5) + 16
    g = (
        f'<g class="floaty" style="animation-delay:{delay}s;animation-duration:{dur}s">'
        f'<rect x="{x}" y="{y}" width="{w:.0f}" height="32" rx="16" fill="{NAVY_D}" fill-opacity=".92" stroke="{ICE}" stroke-opacity=".22"/>'
        f"{icon(key, x + 12, y + 7, 18)}"
        f"{T(x + 38, y + 21, label, 'sb', 12.5, ICE)}</g>"
    )
    return g, w


def hero():
    H = 440
    b = []
    defs = (
        f'<clipPath id="hc"><rect width="{W}" height="{H}" rx="18"/></clipPath>'
        f'<pattern id="hg" width="34" height="34" patternUnits="userSpaceOnUse"><path d="M34 0H0V34" fill="none" stroke="{GLACIER}" stroke-opacity=".10"/></pattern>'
        f'<radialGradient id="hE"><stop offset="0" stop-color="{EMBER}" stop-opacity=".62"/><stop offset="1" stop-color="{EMBER}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="hG"><stop offset="0" stop-color="{GLACIER}" stop-opacity=".5"/><stop offset="1" stop-color="{GLACIER}" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="hT" x1="0" x2="1"><stop offset="0" stop-color="{EMBER}"/><stop offset="1" stop-color="#FFB27A"/></linearGradient>'
    )
    b.append(
        f'<g clip-path="url(#hc)"><rect width="{W}" height="{H}" fill="{NAVY}"/><rect width="{W}" height="{H}" fill="url(#hg)"/>'
        f'<circle cx="690" cy="430" r="380" fill="url(#hE)"/><circle cx="40" cy="10" r="330" fill="url(#hG)"/></g>'
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{GLACIER}" stroke-opacity=".35"/>'
    )
    # brand row
    b.append(f'<rect x="28" y="26" width="38" height="38" rx="10" fill="{EMBER}"/>')
    b.append(T(47, 51, "TG", "d", 14, NAVY, "middle"))
    b.append(T(78, 41, "TRISTAN GAUTAMA", "mb", 11, ICE, ls=3))
    b.append(T(78, 57, "tristangautama.xyz", "m", 10.5, GLACIER))
    pill = "Data Analyst Intern · Kawan Lama Group"
    pw = tw(pill, "m", 10.5) + 40
    b.append(f'<rect x="{772 - pw:.0f}" y="31" width="{pw:.0f}" height="28" rx="14" fill="{ICE}" fill-opacity=".06" stroke="{ICE}" stroke-opacity=".2"/>')
    b.append(f'<circle cx="{772 - pw + 16:.0f}" cy="45" r="3.5" fill="{EMBER}" class="pulse"/>')
    b.append(T(772 - pw + 28, 49, pill, "m", 10.5, ICE))
    # eyebrow + headline
    b.append(T(28, 128, "DATA ANALYST + PRODUCT BUILDER", "mb", 11, EMBER, ls=3))
    size = min(66, 400 / max(tw("Tristan", "d", 1), tw("Gautama", "d", 1)))
    b.append(T(26, 128 + size * 1.0 + 14, "Tristan", "d", round(size, 1), ICE, cls="fadeup", extra='style="animation-delay:.1s"'))
    b.append(T(26, 128 + size * 2.0 + 18, "Gautama", "d", round(size, 1), "url(#hT)", cls="fadeup", extra='style="animation-delay:.25s"'))
    sy = 128 + size * 2.0 + 56
    b.append(T(28, sy, "Data analyst and product builder in Jakarta.", "s", 16.5, ICE))
    b.append(T(28, sy + 23, "Dashboards, analytics and web apps for real businesses.", "s", 14, GLACIER))
    # stat cards
    stats = [(f"{D.TOTAL:,}", "CONTRIBS · 12M"), (f"{D.ACTIVE}", "ACTIVE DAYS"), (f"{D.PUBLIC_REPOS}", "PUBLIC REPOS"), ("3", "LIVE PRODUCTS")]
    cw, gap, y0 = 99, 10, 366
    for i, (n, lab) in enumerate(stats):
        x = 28 + i * (cw + gap)
        b.append(f'<g class="fadeup" style="animation-delay:{0.35 + i * 0.08:.2f}s">'
                 f'<rect x="{x}" y="{y0}" width="{cw}" height="56" rx="10" fill="{ICE}" fill-opacity=".055" stroke="{ICE}" stroke-opacity=".14"/>'
                 f'{T(x + 12, y0 + 27, n, "d", 18, ICE)}{T(x + 12, y0 + 45, lab, "m", 8, GLACIER, ls=1)}</g>')

    # right: floating analytics card (monthly activity, real data)
    mx = [m[1] for m in D.MONTHS]
    top = max(mx) or 1
    cx0, cy0 = 462, 108
    card = [f'<g class="floaty">',
            f'<rect x="{cx0}" y="{cy0}" width="310" height="214" rx="16" fill="{NAVY_D}" fill-opacity=".72" stroke="{ICE}" stroke-opacity=".18"/>']
    for i, col in enumerate((EMBER, GLACIER, ICE)):
        card.append(f'<circle cx="{cx0 + 20 + i * 14}" cy="{cy0 + 20}" r="3.5" fill="{col}" fill-opacity="{1 if i < 2 else .4}"/>')
    card.append(T(cx0 + 290, cy0 + 24, "last 12 months", "m", 9.5, GLACIER, "end"))
    card.append(T(cx0 + 20, cy0 + 68, f"{D.TOTAL:,}", "d", 28, ICE))
    card.append(T(cx0 + 20, cy0 + 86, "CONTRIBUTIONS", "m", 9, GLACIER, ls=1.5))
    if D.DELTA is not None:
        up = D.DELTA >= 0
        txt = f"{abs(D.DELTA)}% vs prior 90d"
        bw = tw(txt, "mb", 9) + 30
        card.append(f'<rect x="{cx0 + 290 - bw:.0f}" y="{cy0 + 50}" width="{bw:.0f}" height="22" rx="11" fill="{EMBER if up else GLACIER}" fill-opacity=".18"/>')
        tri = f"M{cx0 + 290 - bw + 11:.0f} {cy0 + 64} l4 -7 l4 7z" if up else f"M{cx0 + 290 - bw + 11:.0f} {cy0 + 57} l4 7 l4 -7z"
        card.append(f'<path d="{tri}" fill="{EMBER if up else GLACIER}"/>')
        card.append(T(cx0 + 290 - bw + 24, cy0 + 65, txt, "mb", 9, EMBER if up else ICE))
    n = len(mx)
    bw_, bg = 15.5, 7.5
    base = cy0 + 192
    for i, v in enumerate(mx):
        h = max(3, 76 * v / top)
        x = cx0 + 20 + i * (bw_ + bg)
        peak = v == top
        card.append(f'<rect x="{x:.1f}" y="{base - h:.1f}" width="{bw_}" height="{h:.1f}" rx="3" fill="{EMBER if peak else GLACIER}" '
                    f'fill-opacity="{1 if peak else .55}" class="rise" style="animation-delay:{0.4 + i * 0.06:.2f}s"/>')
    card.append(f'<rect x="{cx0 + 20}" y="{base + 3}" width="270" height="1" fill="{ICE}" fill-opacity=".18"/>')
    card.append("</g>")
    b.append("".join(card))
    chips = [("python", "Python", 612, 86, 0, 5.5), ("nextjs", "Next.js", 462, 338, 1.2, 6.2),
             ("typescript", "TypeScript", 572, 352, 2.0, 5.0), ("flutter", "Flutter", 694, 334, 0.6, 6.8)]
    for key, lab, x, y, dl, du in chips:
        g, w = _chip(x, y, key, lab, dl, du)
        b.append(g)
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
    if kind == "globe":
        ic = _globe(18, 12, EMBER)
    elif kind == "diamond":
        ic = _diamond(18, 12, EMBER)
    else:
        ic = icon(kind, 18, 12, 16)
    body = (f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="20" fill="{NAVY}" stroke="{GLACIER}" stroke-opacity=".5"/>'
            f"{ic}{T(18 + 16 + 9, 25, label, 'mb', 10.5, ICE, ls=1.6)}")
    return svg(w, h, body, label), w


# ------------------------------------------------------------------ now bar
def nowbar():
    H = 56
    txt = "Data analyst intern at Kawan Lama Group · business development at Sensify"
    body = (f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="{NAVY}" stroke="{GLACIER}" stroke-opacity=".4"/>'
            f'<rect x="12" y="12" width="56" height="32" rx="16" fill="{EMBER}"/>{T(40, 32, "NOW", "mb", 10.5, NAVY, "middle", ls=2)}'
            f'<circle cx="88" cy="28" r="4" fill="{EMBER}" class="pulse"/>{T(104, 33, txt, "s", 14, ICE)}')
    return svg(W, H, body, "Now: data analyst intern at Kawan Lama Group and business development at Sensify")
