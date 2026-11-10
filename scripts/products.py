"""Three wide product covers (Migravia, Sensify, Griyaplast): header text on the left, the real
product screenshot in a browser frame on the right. Screenshots live in scripts/shots/ and are
embedded as data URIs so the SVG works inside a README <img>."""
import base64
import os

from svgkit import EMBER, GLACIER, ICE, NAVY, NAVY_D, T, svg, tw, wrap

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 800, 350
FX, FW, BAR, FH = 316, 456, 26, 267          # frame x, width, title-bar height, content height
FY = (H - (BAR + FH)) / 2
TX, TW = 36, 256                              # text column
BODY = "#C9D8E2"

# (key, eyebrow, headline lines, sub, url, label, theme)
COVERS = {
    "migravia": ("MIGRAVIA · IMMIGRATION SERVICES", ["Immigration,", "tracked."],
                 "Visa, KITAS and KITAP cases with WhatsApp intake and a client portal.",
                 "migravia.id", "dark", "Migravia: immigration-services platform. Cover with the live website."),
    "sensify": ("SENSIFY · AI STOREFRONT", ["Your brand's", "own storefront."],
                "AI-assisted shopping on an owned website, beside the marketplace.",
                "sensify.id", "deep", "Sensify: AI-powered storefront. Cover with the AI shopping assistant."),
    "griyaplast": ("GRIYA PLAST · SURABAYA", ["Durable plastic,", "17+ colors."],
                   "Product catalog and WhatsApp ordering for a plastic housewares maker.",
                   "griyaplast.shop", "light", "Griya Plast: plastic housewares website. Cover with the live website."),
}


def _size():
    widest = max(tw(l, "d", 1) for c in COVERS.values() for l in c[1])
    return round(min(25, TW / widest), 1)


def _img(key):
    with open(os.path.join(HERE, "shots", key + ".jpg"), "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()


def _cover(key):
    eyebrow, lines, sub, url, theme, label = COVERS[key]
    size = _size()
    light = theme == "light"
    fg = NAVY if light else ICE
    hi = ICE if light else EMBER
    subc = NAVY if light else BODY
    eyc = NAVY if light else GLACIER

    if theme == "dark":
        bg = f'<rect width="{W}" height="{H}" fill="{NAVY}"/><circle cx="760" cy="30" r="260" fill="url(#g1)"/><circle cx="0" cy="360" r="200" fill="url(#g2)"/>'
    elif theme == "deep":
        bg = f'<rect width="{W}" height="{H}" fill="{NAVY_D}"/><circle cx="60" cy="380" r="260" fill="url(#g1)"/><circle cx="780" cy="0" r="260" fill="url(#g2)"/>'
    else:
        bg = f'<rect width="{W}" height="{H}" fill="url(#gl)"/><circle cx="740" cy="40" r="220" fill="{ICE}" fill-opacity=".18"/>'
    defs = (
        f'<clipPath id="cv"><rect width="{W}" height="{H}" rx="20"/></clipPath>'
        f'<clipPath id="fr"><rect x="{FX}" y="{FY + BAR:.1f}" width="{FW}" height="{FH}" rx="0"/></clipPath>'
        f'<clipPath id="fo"><rect x="{FX}" y="{FY:.1f}" width="{FW}" height="{BAR + FH}" rx="12"/></clipPath>'
        f'<radialGradient id="g1"><stop offset="0" stop-color="{EMBER}" stop-opacity=".5"/><stop offset="1" stop-color="{EMBER}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="g2"><stop offset="0" stop-color="{GLACIER}" stop-opacity=".45"/><stop offset="1" stop-color="{GLACIER}" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="gl" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9DBBD1"/><stop offset="1" stop-color="{GLACIER}"/></linearGradient>'
        f'<filter id="sh" x="-20%" y="-20%" width="140%" height="150%"><feGaussianBlur stdDeviation="14"/></filter>'
    )
    b = [f'<g clip-path="url(#cv)">{bg}']

    # ---- text column, vertically centred
    lh = round(size * 1.28)
    sub_lines = wrap(sub, "s", 13.5, TW)[:3]
    block = 12 + 26 + len(lines) * lh + 10 + len(sub_lines) * 20 + 22 + 34
    y = (H - block) / 2 + 10
    b.append(T(TX, y, eyebrow, "mb", 9.5, eyc, ls=1.8))
    y += 26 + size * 0.78
    for i, ln in enumerate(lines):
        b.append(T(TX, y, ln, "d", size, fg if i == 0 else hi, cls="fadeup", extra=f'style="animation-delay:{.1 + i * .15:.2f}s"'))
        y += lh
    y += 2
    for ln in sub_lines:
        b.append(T(TX, y, ln, "s", 13.5, subc))
        y += 20
    y += 14
    bw = tw(f"Visit {url}", "sb", 12.5) + 56
    b.append(f'<rect x="{TX}" y="{y:.1f}" width="{bw:.0f}" height="34" rx="17" fill="{EMBER}"/>')
    b.append(T(TX + 20, y + 21.5, f"Visit {url}", "sb", 12.5, NAVY))
    ax, ay = TX + bw - 30, y + 11.5
    b.append(f'<path d="M{ax} {ay + 9}L{ax + 9} {ay}M{ax + 2} {ay}H{ax + 9}V{ay + 7}" fill="none" stroke="{NAVY}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>')

    # ---- browser frame with the real screenshot
    barc = "#E3ECF2" if light else NAVY_D
    urlc = NAVY if light else GLACIER
    f = [f'<rect x="{FX}" y="{FY + 16:.1f}" width="{FW}" height="{BAR + FH}" rx="12" fill="#000" fill-opacity="{.28 if light else .55}" filter="url(#sh)"/>']
    f.append(f'<g clip-path="url(#fo)"><rect x="{FX}" y="{FY:.1f}" width="{FW}" height="{BAR + FH}" fill="{barc}"/>')
    for i, c in enumerate(("#FE7F2D", "#6594B1", "#8FA9B8")):
        f.append(f'<circle cx="{FX + 16 + i * 13}" cy="{FY + BAR / 2:.1f}" r="3.6" fill="{c}"/>')
    pw = 170
    f.append(f'<rect x="{FX + FW / 2 - pw / 2:.0f}" y="{FY + 5:.1f}" width="{pw}" height="16" rx="8" fill="{NAVY}" fill-opacity="{.1 if light else .55}"/>')
    f.append(T(FX + FW / 2, FY + 16.2, url, "m", 8.5, urlc, "middle"))
    f.append(f'<image x="{FX}" y="{FY + BAR:.1f}" width="{FW}" height="{FH}" preserveAspectRatio="xMidYMid slice" xlink:href="{_img(key)}" clip-path="url(#fr)"/></g>')
    f.append(f'<rect x="{FX + .5}" y="{FY + .5:.1f}" width="{FW - 1}" height="{BAR + FH - 1}" rx="12" fill="none" stroke="{ICE}" stroke-opacity="{.5 if light else .22}"/>')
    b.append(f'<g class="floaty" style="animation-duration:7s">{"".join(f)}</g></g>')
    b.append(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="20" fill="none" stroke="{GLACIER}" stroke-opacity=".4"/>')
    return svg(W, H, "".join(b), label, defs=defs, attrs='xmlns:xlink="http://www.w3.org/1999/xlink"')


def migravia():
    return _cover("migravia")


def sensify():
    return _cover("sensify")


def griyaplast():
    return _cover("griyaplast")
