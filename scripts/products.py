"""Three designed product covers (Migravia, Sensify, Griyaplast). Each is its own SVG so the README
can wrap it in a link. The covers are illustrations in the palette, not screenshots."""
from svgkit import EMBER, GLACIER, ICE, NAVY, NAVY_D, NAVY_L, T, svg, tw, wrap

CW, CH, ART = 360, 486, 232
BODY = "#C9D8E2"


def _arrow(x, y, c=EMBER):
    return f'<path d="M{x} {y + 9}L{x + 9} {y}M{x + 2} {y}H{x + 9}V{y + 7}" fill="none" stroke="{c}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'


def _card(art, defs, name, accent, desc, tags, link, label):
    b = [f'<g clip-path="url(#cc)"><g clip-path="url(#ca)">{art}</g></g>']
    b.append(f'<rect x=".5" y=".5" width="{CW - 1}" height="{CH - 1}" rx="20" fill="none" stroke="{GLACIER}" stroke-opacity=".38"/>')
    b.append(f'<rect x="28" y="{ART + 26}" width="5" height="24" rx="2.5" fill="{accent}"/>')
    b.append(T(44, ART + 45, name, "d", 20, ICE))
    y = ART + 76
    for ln in wrap(desc, "s", 13, 304)[:4]:
        b.append(T(28, y, ln, "s", 13, BODY))
        y += 19
    x = 28
    ty = ART + 150 if len(wrap(desc, "s", 13, 304)) >= 3 else ART + 130
    ty = max(ty, y + 8)
    for t in tags:
        w = tw(t, "m", 9.5, 0.4) + 20
        b.append(f'<rect x="{x}" y="{ty}" width="{w:.0f}" height="22" rx="11" fill="{ICE}" fill-opacity=".06" stroke="{GLACIER}" stroke-opacity=".45"/>')
        b.append(T(x + 10, ty + 15, t, "m", 9.5, GLACIER, ls=0.4))
        x += w + 7
    b.append(f'<rect x="28" y="{CH - 58}" width="{CW - 56}" height="1" fill="{ICE}" fill-opacity=".14"/>')
    b.append(T(28, CH - 28, link, "sb", 13.5, EMBER))
    b.append(_arrow(CW - 40, CH - 39))
    d = (f'<clipPath id="cc"><rect width="{CW}" height="{CH}" rx="20"/></clipPath><clipPath id="ca"><rect width="{CW}" height="{ART}"/></clipPath>'
         f'<rect id="bgcard" width="0" height="0"/>' + defs)
    body = f'<rect width="{CW}" height="{CH}" rx="20" fill="{NAVY}"/>' + "".join(b)
    return svg(CW, CH, body, label, defs=d)


# ------------------------------------------------------------------ Migravia
def migravia():
    defs = (f'<linearGradient id="mA" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{NAVY_L}"/><stop offset="1" stop-color="{NAVY_D}"/></linearGradient>'
            f'<radialGradient id="mE"><stop offset="0" stop-color="{EMBER}" stop-opacity=".55"/><stop offset="1" stop-color="{EMBER}" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="mP" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8FB1C9"/><stop offset="1" stop-color="{GLACIER}"/></linearGradient>')
    a = [f'<rect width="{CW}" height="{ART}" fill="url(#mA)"/><circle cx="330" cy="20" r="170" fill="url(#mE)"/>']
    a.append(T(28, 40, "MIGRAVIA", "d", 14, ICE))
    a.append(T(28, 58, "VISA · KITAS · KITAP", "mb", 9, GLACIER, ls=2))
    a.append(T(28, 100, "Immigration,", "d", 19, ICE))
    a.append(T(28, 128, "tracked.", "d", 19, EMBER))
    # permit card behind
    a.append(f'<g transform="rotate(-8 276 112)" class="floaty"><rect x="216" y="62" width="126" height="86" rx="11" fill="url(#mP)"/>'
             f'<circle cx="240" cy="92" r="13" fill="{EMBER}"/><circle cx="240" cy="92" r="6.5" fill="none" stroke="{NAVY}" stroke-width="1.6"/>'
             f'<rect x="260" y="82" width="66" height="6" rx="3" fill="{NAVY}" fill-opacity=".55"/><rect x="260" y="96" width="46" height="6" rx="3" fill="{NAVY}" fill-opacity=".35"/>'
             f'<rect x="228" y="124" width="100" height="5" rx="2.5" fill="{NAVY}" fill-opacity=".3"/>{T(228, 116, "KITAS", "mb", 8.5, NAVY, ls=2)}</g>')
    # renewal chips
    for i, d in enumerate(("90d", "60d", "30d")):
        x = 236 + i * 38
        a.append(f'<g class="fadeup" style="animation-delay:{0.3 + i * 0.15}s"><rect x="{x}" y="20" width="32" height="20" rx="10" fill="none" stroke="{EMBER}" stroke-opacity="{.45 + i * .25}"/>'
                 f'{T(x + 16, 34, d, "mb", 9, EMBER, "middle")}</g>')
    # tracker card
    a.append(f'<rect x="24" y="150" width="256" height="66" rx="12" fill="{ICE}" fill-opacity=".97"/>')
    a.append(T(40, 170, "CASE STATUS", "mb", 8.5, GLACIER, ls=1.6))
    a.append(f'<rect x="206" y="157" width="62" height="18" rx="9" fill="{EMBER}" fill-opacity=".18"/><circle cx="216" cy="166" r="3" fill="{EMBER}" class="pulse"/>')
    a.append(T(223, 169.5, "ON TRACK", "mb", 8, "#B4520E", ls=.6))
    a.append(f'<rect x="40" y="196" width="224" height="4" rx="2" fill="{NAVY}" fill-opacity=".14"/>')
    a.append(f'<rect x="40" y="196" width="150" height="4" rx="2" fill="{EMBER}" class="sweep"/>')
    for i in range(5):
        x = 40 + i * 56
        on = i < 3
        a.append(f'<circle cx="{x}" cy="198" r="5.5" fill="{EMBER if on else ICE}" stroke="{EMBER if on else GLACIER}" stroke-width="1.6"/>')
    return _card("".join(a), defs, "MIGRAVIA", EMBER,
                 "Immigration-services platform for visa, KITAS and KITAP cases in Indonesia: WhatsApp-first intake, itemised quotes, and a client portal with case tracking and renewal alerts.",
                 ["React", "Vite", "TypeScript", "WhatsApp"], "Visit migravia.id", "Migravia cover: immigration case tracker illustration")


# ------------------------------------------------------------------ Sensify
def sensify():
    defs = (f'<radialGradient id="sE"><stop offset="0" stop-color="{EMBER}" stop-opacity=".6"/><stop offset="1" stop-color="{EMBER}" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="sG"><stop offset="0" stop-color="{GLACIER}" stop-opacity=".45"/><stop offset="1" stop-color="{GLACIER}" stop-opacity="0"/></radialGradient>')
    a = [f'<rect width="{CW}" height="{ART}" fill="{NAVY_D}"/><circle cx="40" cy="250" r="200" fill="url(#sE)"/><circle cx="340" cy="0" r="170" fill="url(#sG)"/>']
    a.append(T(28, 40, "SENSIFY", "d", 14, ICE))
    a.append(T(28, 58, "AI-POWERED STOREFRONT", "mb", 9, GLACIER, ls=2))
    a.append(T(28, 100, "Your brand's", "d", 19, ICE))
    a.append(T(28, 128, "own storefront.", "d", 19, EMBER))
    # browser mock
    a.append(f'<rect x="28" y="140" width="230" height="84" rx="12" fill="{ICE}" fill-opacity=".07" stroke="{ICE}" stroke-opacity=".2"/>')
    for i in range(3):
        a.append(f'<circle cx="{42 + i * 11}" cy="152" r="2.6" fill="{ICE}" fill-opacity=".45"/>')
    a.append(f'<rect x="40" y="162" width="108" height="28" rx="7" fill="{EMBER}"/>')
    a.append(f'<rect x="48" y="170" width="58" height="5" rx="2.5" fill="{NAVY}" fill-opacity=".7"/><rect x="48" y="179" width="36" height="4" rx="2" fill="{NAVY}" fill-opacity=".45"/>')
    for i in range(3):
        a.append(f'<rect x="{40 + i * 38}" y="196" width="32" height="20" rx="6" fill="{GLACIER}" fill-opacity="{.35 + i * .15}" class="pop" style="animation-delay:{0.2 + i * .15}s"/>')
    # chat bubble
    a.append('<g class="floaty" style="animation-duration:4.2s">')
    a.append(f'<rect x="198" y="138" width="148" height="46" rx="14" fill="{ICE}"/><path d="M216 184l-8 10 19-10z" fill="{ICE}"/>')
    a.append(f'<circle cx="218" cy="153" r="9" fill="{EMBER}"/><path d="M218 147l1.7 4.3 4.3 1.7-4.3 1.7-1.7 4.3-1.7-4.3-4.3-1.7 4.3-1.7z" fill="{NAVY}"/>')
    a.append(T(234, 151, "Looking for a gift?", "sb", 10.5, NAVY))
    for i in range(3):
        a.append(f'<circle cx="{236 + i * 9}" cy="168" r="2.6" fill="{GLACIER}" class="dt" style="animation-delay:{i * .2}s"/>')
    a.append("</g>")
    a.append(f'<rect x="290" y="198" width="48" height="26" rx="13" fill="{EMBER}"/>{T(314, 215, "Buy", "sb", 11.5, NAVY, "middle")}')
    return _card("".join(a), defs, "SENSIFY", GLACIER,
                 "AI-powered storefront for Indonesian brands: an owned official website beside the marketplace, with AI-assisted shopping, checkout paths and a cinematic interactive homepage.",
                 ["React", "Vite", "Three.js", "Tailwind"], "Visit sensify.id", "Sensify cover: AI storefront and shopping assistant illustration")


# ------------------------------------------------------------------ Griyaplast
SWATCHES = ["#233D4D", "#2E4C5F", "#FE7F2D", "#FF9A57", "#FFB784", "#EAF1F6", "#C9D8E2", "#A9C1D3", "#6594B1",
            "#4F7C99", "#3F6580", "#F6C9A6", "#D9692A", "#8FA9B8", "#1F5C73", "#F2E3D5", "#B9532A"]


def _crate(x, y, w, h, fill, slot):
    s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="{fill}"/>',
         f'<rect x="{x - 4}" y="{y}" width="{w + 8}" height="9" rx="4.5" fill="{fill}"/>']
    rows, cols = 3, 5
    cw, gh = (w - 24) / cols, 8
    for r in range(rows):
        for c in range(cols):
            s.append(f'<rect x="{x + 12 + c * cw + 2:.1f}" y="{y + 20 + r * 16}" width="{cw - 4:.1f}" height="{gh}" rx="4" fill="{slot}" fill-opacity=".55"/>')
    return "".join(s)


def griyaplast():
    defs = (f'<linearGradient id="gA" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9DBBD1"/><stop offset="1" stop-color="{GLACIER}"/></linearGradient>')
    a = [f'<rect width="{CW}" height="{ART}" fill="url(#gA)"/>']
    a.append(f'<circle cx="320" cy="40" r="120" fill="{ICE}" fill-opacity=".14"/>')
    a.append(T(28, 40, "GRIYA PLAST", "d", 14, NAVY))
    a.append(T(28, 58, "SURABAYA · SINCE 2000", "mb", 9, NAVY, ls=2, extra='fill-opacity=".75"'))
    a.append(T(28, 100, "Thick, durable,", "d", 19, NAVY))
    a.append(T(28, 128, "17+ colors.", "d", 19, ICE))
    # stacked crates
    a.append(f'<g class="floaty" style="animation-duration:6s">{_crate(206, 70, 112, 70, EMBER, NAVY)}</g>')
    a.append(f'<g class="floaty" style="animation-duration:5.4s;animation-delay:.6s">{_crate(176, 126, 132, 66, NAVY, GLACIER)}</g>')
    a.append(f'<g class="floaty" style="animation-duration:6.6s;animation-delay:1s">{_crate(238, 148, 96, 48, ICE, GLACIER)}</g>')
    # swatches
    for i, c in enumerate(SWATCHES):
        a.append(f'<circle cx="{34 + i * 17.6:.1f}" cy="214" r="6.4" fill="{c}" stroke="{NAVY}" stroke-opacity=".4" class="pop" style="animation-delay:{0.1 + i * 0.05:.2f}s"/>')
    return _card("".join(a), defs, "GRIYAPLAST", ICE,
                 "Website for a plastic household-goods manufacturer in Surabaya: a product catalog across 36+ lines, WhatsApp ordering for retail and wholesale, and a shipping-cost estimator.",
                 ["Next.js", "TypeScript", "WhatsApp"], "Visit griyaplast.shop", "Griya Plast cover: stacked plastic crates and colour swatches illustration")
