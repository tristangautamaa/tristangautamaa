"""About, tech stack, remaining projects, experience and footer."""
import data as D
from hero import L, R, W, heading
from svgkit import EMBER, GLACIER, ICE, NAVY, T, icon, svg, tw, wrap


# ------------------------------------------------------------------ about
def whoami():
    head, y = heading("01", "ABOUT", "About", "Jakarta, Indonesia")
    b = [head]
    y += 10
    lines = [
        "Student at Multimedia Nusantara University in Jakarta.",
        "Data analyst intern who also builds websites, apps and internal tools for real businesses.",
        "On the side: student research on geospatial machine learning for energy access in Indonesia.",
    ]
    for i, t in enumerate(lines):
        b.append(T(L, y + i * 26, t, "s", 15.5, "fg"))
    y += 26 * 3 + 6
    b.append(f'<rect x="{L}" y="{y}" width="{R - L}" height="1" class="slm"/>')
    y += 32
    rows = [("FOCUS", "data analysis · web and full-stack development · AI-integrated products"),
            ("BASE", "Jakarta, Indonesia")]
    for i, (k, v) in enumerate(rows):
        yy = y + i * 28
        b.append(T(L, yy, k, "mb", 10, "mu", ls=2.4))
        b.append(T(L + 110, yy, v, "s", 14, "fg"))
    h = int(y + len(rows) * 28 + 4)
    return svg(W, h, "\n".join(b), "About Tristan: student in Jakarta, data analyst intern, builder of websites, apps and internal tools")


# ------------------------------------------------------------------ stack
STACK = [
    ("LANGUAGES", [("java", "Java"), ("python", "Python"), ("typescript", "TypeScript"), ("javascript", "JavaScript"), ("php", "PHP"),
                   ("cplusplus", "C++"), ("dart", "Dart"), ("html5", "HTML"), ("css3", "CSS")]),
    ("FRAMEWORKS & LIBRARIES", [("react", "React"), ("nextjs", "Next.js"), ("flutter", "Flutter"), ("fastapi", "FastAPI"), ("laravel", "Laravel"),
                                ("nodejs", "Node.js"), ("tailwindcss", "Tailwind"), ("vite", "Vite"), ("threejs", "Three.js")]),
    ("DATA & ML", [("pandas", "pandas"), ("numpy", "NumPy"), ("scikitlearn", "scikit-learn"), ("jupyter", "Jupyter"), ("streamlit", "Streamlit")]),
    ("TOOLS & PLATFORMS", [("git", "Git"), ("github", "GitHub"), ("docker", "Docker"), ("vercel", "Vercel"), ("firebase", "Firebase"), ("supabase", "Supabase")]),
]


def stack():
    head, hy = heading("04", "STACK", "Tech stack", "What I build with")
    top = hy - 8
    pitch, tile = 76, 58
    PH = 28 + len(STACK) * 118 + 4
    b = [f'<g transform="translate(0 {top})">',
         f'<rect x=".5" y=".5" width="{W - 1}" height="{PH - 1}" rx="18" fill="{NAVY}" stroke="{GLACIER}" stroke-opacity=".4"/>']
    n = 0
    for gi, (grp, items) in enumerate(STACK):
        y0 = 28 + gi * 118
        b.append(T(28, y0 + 4, grp, "mb", 10, EMBER, ls=2.5))
        gw = tw(grp, "mb", 10, 2.5)
        b.append(f'<rect x="{28 + gw + 14:.0f}" y="{y0 + 0}" width="{W - 56 - gw - 14:.0f}" height="1" fill="{ICE}" fill-opacity=".12"/>')
        for i, (key, name) in enumerate(items):
            x = 28 + i * pitch
            y = y0 + 20
            b.append(f'<g class="pop" style="animation-delay:{0.05 * n:.2f}s">'
                     f'<rect x="{x}" y="{y}" width="{tile}" height="{tile}" rx="14" fill="{ICE}" fill-opacity=".06" stroke="{ICE}" stroke-opacity=".13"/>'
                     f'{icon(key, x + 12, y + 12, 34)}{T(x + tile / 2, y + tile + 16, name, "m", 9, GLACIER, "middle")}</g>')
            n += 1
    b.append("</g>")
    labels = ", ".join(n_ for _, items in STACK for _, n_ in items)
    return svg(W, top + PH, head + "".join(b), f"Tech stack: {labels}")


# ------------------------------------------------------------------ projects
PROJECTS = [
    ("SEAPORT — VENDOR EKSPEDISI KLG", "INTERNAL",
     "Internal freight-tariff portal: imports vendor RFQ spreadsheets, matches them to master data, keeps monthly rates with full revision history and compares vendors lane by lane.",
     "NEXT.JS · REACT · TAILWIND · RADIX UI · SHEETJS"),
    ("NAWARX", "INTERNAL",
     "Billboard (OOH) intelligence tool: a price database, a price calculator and a negotiation advisor that benchmarks quotes against deal history and maps nearby sites and vendors.",
     "VITE · TYPESCRIPT · LEAFLET · SUPABASE · PYTHON"),
    ("GISEU", "",
     "Editorial fashion site in a quiet-luxury, modern-Japanese-minimal style: one continuous smooth-scrolling page with a fullscreen rolling-text navigation.",
     "VITE · REACT · TYPESCRIPT · FRAMER MOTION · GSAP · LENIS"),
    ("ZEAT APP", "",
     "Food-ordering app with menu, cart, pickup and delivery tracking, an admin dashboard and a chatbot.",
     "FLUTTER · DART · FIREBASE"),
    ("ZERO-EAT", "",
     "Laravel web app with user registration, login, profiles and a product catalog.",
     "LARAVEL · PHP · BLADE · TAILWIND"),
]


def projects():
    head, y = heading("05", "PROJECTS", "More projects", "Internal tools and earlier builds")
    b = [head]
    y += 8
    for i, (title, tag, desc, tags) in enumerate(PROJECTS, 1):
        b.append(T(L, y + 14, f"{i:02d}", "mb", 11, "ac", ls=1))
        b.append(T(L + 34, y + 15, title, "d", 13, "fg"))
        if tag:
            tw_ = tw(tag, "mb", 9, 2) + 18
            b.append(f'<rect x="{R - tw_:.0f}" y="{y + 2}" width="{tw_:.0f}" height="20" rx="10" class="slm" fill="none"/>')
            b.append(T(R - tw_ / 2, y + 16, tag, "mb", 9, "mu", "middle", ls=2))
        yy = y + 40
        for ln in wrap(desc, "s", 13.5, R - L - 34):
            b.append(T(L + 34, yy, ln, "s", 13.5, "fg"))
            yy += 20
        b.append(T(L + 34, yy + 6, tags, "m", 9.5, "mu", ls=.8))
        y = yy + 24
        b.append(f'<rect x="{L}" y="{y}" width="{R - L}" height="1" class="slm"/>')
        y += 24
    return svg(W, int(y - 14), "\n".join(b), "More projects: Seaport, NawarX, GISEU, ZEAT app and Zero-EAT")


# ------------------------------------------------------------------ experience
EXPERIENCE = [
    ("FEB 2026 — FEB 2027", "Data Analyst Intern", "Kawan Lama Group", "Operations officer Feb–Apr 2026, data analyst from May 2026."),
    ("MAY 2026 — NOW", "Business Development Representative", "Sensify", "Part-time. AI-powered storefronts for growing brands."),
    ("EDUCATION", "Student", "Multimedia Nusantara University", "Jakarta, Indonesia."),
]


def experience():
    head, y = heading("06", "EXPERIENCE", "Experience", "Where I work and study")
    b = [head]
    y += 14
    for i, (per, role, org, sub) in enumerate(EXPERIENCE):
        b.append(T(L, y + 14, per, "mb", 10, "mu", ls=1.5))
        b.append(T(L + 200, y + 15, role, "sb", 16, "fg"))
        b.append(T(L + 200, y + 37, f"{org} — {sub}", "s", 13.5, "mu"))
        y += 66
        if i < len(EXPERIENCE) - 1:
            b.append(f'<rect x="{L}" y="{y - 14}" width="{R - L}" height="1" class="slm"/>')
    return svg(W, int(y - 6), "\n".join(b), "Experience: data analyst intern at Kawan Lama Group, business development at Sensify, student at Multimedia Nusantara University")


# ------------------------------------------------------------------ footer
def footer():
    b = [f'<rect x="{L}" y="8" width="{R - L}" height="1.5" class="slm"/>',
         f'<circle cx="{L + 8}" cy="40" r="4" class="acf pulse"/>',
         T(L + 24, 44, "tristangautama.xyz", "sb", 13.5, "fg"),
         T(R, 44, f"Jakarta, Indonesia · © {D.SNAPSHOT.year}", "m", 11, "mu", "end")]
    return svg(W, 64, "\n".join(b), "tristangautama.xyz, Jakarta, Indonesia")
