"""Animated analytics dashboard. Every number is computed from the GitHub data in assets/data.json
or from the roles listed in the README; nothing is estimated or invented."""
import datetime as dt
import math

import data as D
from hero import heading
from svgkit import EMBER, GLACIER, ICE, NAVY, NAVY_D, NAVY_L, T, svg, tw

W = 800
PX = 20            # outer padding inside the panel
CARD = f'fill="{ICE}" fill-opacity=".045" stroke="{ICE}" stroke-opacity=".11"'
LEVEL_FILL = [(ICE, .07), (GLACIER, .38), (GLACIER, .8), (EMBER, .6), (EMBER, 1)]


def _spark(vals, x, y, w, h, delay=0.4):
    top, low = max(vals), min(vals)
    span = (top - low) or 1
    pts = [(x + i * w / (len(vals) - 1), y + h - (v - low) / span * h) for i, v in enumerate(vals)]
    d = "M" + " L".join(f"{px:.1f} {py:.1f}" for px, py in pts)
    area = d + f" L{x + w:.1f} {y + h} L{x} {y + h}Z"
    return (f'<path d="{area}" fill="{EMBER}" fill-opacity=".12"/>'
            f'<path d="{d}" pathLength="1" fill="none" stroke="{EMBER}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" '
            f'class="draw" style="animation-delay:{delay}s"/>')


def _tri(x, y, up, c):
    return f'<path d="M{x} {y + (0 if up else -7)} l4 {-7 if up else 7} l4 {7 if up else -7}z" fill="{c}"/>'


def dashboard():
    out = []
    # ---- heading (adaptive colours, sits above the navy panel)
    head, hy = heading("03", "DASHBOARD", "Activity dashboard", "Refreshed weekly from GitHub")
    top = hy - 8
    PH = 580
    b = [f'<g transform="translate(0 {top})">']
    b.append(f'<rect x=".5" y=".5" width="{W - 1}" height="{PH - 1}" rx="18" fill="{NAVY}" stroke="{GLACIER}" stroke-opacity=".4"/>')

    # ---- top bar
    for i, c in enumerate((EMBER, GLACIER, ICE)):
        b.append(f'<circle cx="{30 + i * 15}" cy="27" r="4" fill="{c}" fill-opacity="{1 if i < 2 else .4}"/>')
    b.append(T(86, 31, "tristan.analytics", "mb", 11.5, ICE))
    b.append(T(86 + tw("tristan.analytics", "mb", 11.5) + 10, 31, "/ overview / last 12 months", "m", 10.5, GLACIER))
    live = f"snapshot {D.SNAPSHOT.isoformat()}"
    lw = tw(live, "m", 10) + 84
    b.append(f'<rect x="{W - PX - lw:.0f}" y="13" width="{lw:.0f}" height="26" rx="13" fill="{ICE}" fill-opacity=".06" stroke="{ICE}" stroke-opacity=".16"/>')
    b.append(f'<circle cx="{W - PX - lw + 15:.0f}" cy="26" r="3.5" fill="{EMBER}" class="pulse"/>')
    b.append(T(W - PX - lw + 26, 30, "SYNCED", "mb", 9, EMBER, ls=1.5))
    b.append(T(W - PX - lw + 76, 30, live, "m", 10, GLACIER))
    b.append(f'<rect x="0" y="52" width="{W}" height="1" fill="{ICE}" fill-opacity=".1"/>')

    # ---- KPI row
    kw, kg, ky, kh = (W - 2 * PX - 3 * 12) / 4, 12, 68, 96
    wk = D.weekly()
    mon_act = [m[2] for m in D.MONTHS]
    kpis = [
        ("CONTRIBUTIONS · 12M", f"{D.TOTAL:,}", wk, D.DELTA),
        ("ACTIVE DAYS", f"{D.ACTIVE}", mon_act, None),
        ("LONGEST STREAK", f"{D.LONGEST}", None, None),
        (f"PEAK MONTH · {D.PEAK_LABEL}", f"{D.PEAK[1]:,}", [m[1] for m in D.MONTHS], None),
    ]
    for i, (lab, val, spark, delta) in enumerate(kpis):
        x = PX + i * (kw + kg)
        b.append(f'<g class="fadeup" style="animation-delay:{0.1 + i * 0.1:.1f}s"><rect x="{x:.1f}" y="{ky}" width="{kw:.1f}" height="{kh}" rx="12" {CARD}/>')
        b.append(T(x + 14, ky + 24, lab, "m", 8.5, GLACIER, ls=1.3))
        b.append(T(x + 14, ky + 56, val, "d", 26, ICE))
        if spark:
            b.append(_spark(spark, x + 14, ky + 66, kw - 28, 18, 0.5 + i * 0.1))
        if i == 1:
            b.append(T(x + kw - 14, ky + 56, f"{round(100 * D.ACTIVE / len(D.COUNTS))}% of days", "m", 9, GLACIER, "end"))
        if i == 0 and delta is not None:
            up = delta >= 0
            txt = f"{abs(delta)}%"
            b.append(_tri(x + kw - 14 - tw(txt, "mb", 9) - 12, ky + 56, up, EMBER if up else GLACIER))
            b.append(T(x + kw - 14, ky + 56, txt, "mb", 9, EMBER if up else GLACIER, "end"))
        if i == 2:
            b.append(T(x + kw - 14, ky + 56, "days in a row", "m", 9, GLACIER, "end"))
            # streak squares: last-30-day activity strip
            recent = D.COUNTS[-30:]
            for j, c in enumerate(recent):
                col, op = (EMBER, 1) if c else (ICE, .1)
                b.append(f'<rect x="{x + 14 + j * ((kw - 28) / 30):.1f}" y="{ky + 70}" width="{(kw - 28) / 30 - 2:.1f}" height="14" rx="2" fill="{col}" fill-opacity="{op}" class="pop" style="animation-delay:{0.6 + j * 0.02:.2f}s"/>')
        b.append("</g>")

    # ---- monthly chart
    cy, ch = 180, 204
    cwid = 500
    b.append(f'<rect x="{PX}" y="{cy}" width="{cwid}" height="{ch}" rx="14" {CARD}/>')
    b.append(T(PX + 18, cy + 28, "CONTRIBUTIONS / MONTH", "mb", 10, ICE, ls=2))
    b.append(T(PX + cwid - 18, cy + 28, "ends are partial months", "m", 9, GLACIER, "end"))
    months = D.MONTHS
    mx = max(m[1] for m in months) or 1
    ax0, ax1, base = PX + 28, PX + cwid - 18, cy + ch - 34
    n = len(months)
    slot = (ax1 - ax0) / n
    bw = slot * 0.58
    for g in (0.25, 0.5, 0.75, 1.0):
        gy = base - 112 * g
        b.append(f'<rect x="{ax0}" y="{gy:.1f}" width="{ax1 - ax0:.0f}" height="1" fill="{ICE}" fill-opacity=".07"/>')
    for i, (lab, tot, act, partial, yr) in enumerate(months):
        h = max(3, 112 * tot / mx)
        x = ax0 + i * slot + (slot - bw) / 2
        peak = tot == mx
        fo = 1 if peak else (.3 if partial else .6)
        b.append(f'<rect x="{x:.1f}" y="{base - h:.1f}" width="{bw:.1f}" height="{h:.1f}" rx="3.5" fill="{EMBER if peak else GLACIER}" fill-opacity="{fo}" '
                 f'class="rise" style="animation-delay:{0.3 + i * 0.07:.2f}s"/>')
        b.append(T(x + bw / 2, base - h - 6, f"{tot:,}", "mb", 8.5, ICE if tot > 0 else GLACIER, "middle"))
        b.append(T(x + bw / 2, base + 16, lab, "m", 8.5, GLACIER, "middle", ls=.5))
    b.append(f'<rect x="{ax0}" y="{base + 3}" width="{ax1 - ax0:.0f}" height="1" fill="{ICE}" fill-opacity=".2"/>')

    # ---- language donut (public repos, by code size)
    dx, dw = PX + cwid + 12, W - 2 * PX - cwid - 12
    b.append(f'<rect x="{dx}" y="{cy}" width="{dw}" height="{ch}" rx="14" {CARD}/>')
    b.append(T(dx + 16, cy + 28, "LANGUAGES · PUBLIC CODE", "mb", 10, ICE, ls=2))
    shown = D.LANGS[:7]
    rest = max(0.0, 100 - sum(p for _, p in shown))
    if rest > 0.5:
        shown = shown + [("Other", rest)]
    cols = [EMBER, GLACIER, ICE, "#FF9A57", "#4F7C99", "#A9C1D3", "#FFB784", "#6E8697"]
    cxd, cyd, r = dx + 62, cy + 112, 44
    circ = 2 * math.pi * r
    tot = sum(p for _, p in shown)
    ang = 0.0
    b.append(f'<circle cx="{cxd}" cy="{cyd}" r="{r}" fill="none" stroke="{ICE}" stroke-opacity=".07" stroke-width="16"/>')
    for i, (nm, p) in enumerate(shown):
        seg = circ * p / tot
        vis = max(seg - 2.2, 0.1)
        b.append(f'<circle cx="{cxd}" cy="{cyd}" r="{r}" fill="none" stroke="{cols[i]}" stroke-width="16" stroke-dasharray="{vis:.1f} {circ:.1f}" '
                 f'transform="rotate({ang - 90:.1f} {cxd} {cyd})" class="ring" style="--len:{vis:.1f};animation-delay:{0.4 + i * 0.12:.2f}s"/>')
        ang += 360 * p / tot
    b.append(T(cxd, cyd + 4, f"{D.PUBLIC_REPOS}", "d", 17, ICE, "middle"))
    b.append(T(cxd, cyd + 18, "repos", "m", 8.5, GLACIER, "middle"))
    for i, (nm, p) in enumerate(shown):
        ly = cy + 54 + i * 18.5
        b.append(f'<circle cx="{dx + 126}" cy="{ly - 3.5}" r="4" fill="{cols[i]}"/>')
        b.append(T(dx + 136, ly, nm if len(nm) < 11 else nm[:10] + ".", "sb", 10.5, ICE))
        b.append(T(dx + dw - 14, ly, f"{p:.0f}%", "m", 9.5, GLACIER, "end"))

    # ---- heatmap
    hy_, hh = 396, 150
    b.append(f'<rect x="{PX}" y="{hy_}" width="{cwid}" height="{hh}" rx="14" {CARD}/>')
    b.append(T(PX + 18, hy_ + 28, "DAILY ACTIVITY", "mb", 10, ICE, ls=2))
    pitch, cell = 8.5, 7
    start_dow = (D.WIN_START.weekday() + 1) % 7
    gx0, gy0 = PX + 18, hy_ + 62
    last_label = -9
    for i, ch_ in enumerate(D.LEVELS):
        col, row = (i + start_dow) // 7, (i + start_dow) % 7
        f, o = LEVEL_FILL[int(ch_)]
        b.append(f'<rect x="{gx0 + col * pitch:.1f}" y="{gy0 + row * pitch:.1f}" width="{cell}" height="{cell}" rx="1.6" fill="{f}" fill-opacity="{o}" '
                 f'class="pop" style="animation-delay:{0.2 + col * 0.018:.2f}s"/>')
    marks = [(0, D.WIN_START.month)]
    for i, d_ in enumerate(D.DAYS):
        if d_.day == 1:
            marks.append(((i + start_dow) // 7, d_.month))
    for col, mo in marks:
        if col - last_label >= 3:
            b.append(T(gx0 + col * pitch, hy_ + 52, D.MONTH_ABBR[mo - 1], "m", 8, GLACIER, ls=.6))
            last_label = col
    ly = hy_ + hh - 18
    b.append(T(PX + 18, ly + 7, f"{D.ACTIVE} active days", "m", 8.5, GLACIER))
    lx = PX + cwid - 18 - 5 * 13 - 70
    b.append(T(lx, ly + 7, "LESS", "m", 8, GLACIER, "end", ls=1))
    for k, (f, o) in enumerate(LEVEL_FILL):
        b.append(f'<rect x="{lx + 8 + k * 13}" y="{ly - 1}" width="9" height="9" rx="2" fill="{f}" fill-opacity="{o}"/>')
    b.append(T(lx + 8 + 5 * 13 + 4, ly + 7, "MORE", "m", 8, GLACIER, ls=1))

    # ---- weekday bars
    b.append(f'<rect x="{dx}" y="{hy_}" width="{dw}" height="{hh}" rx="14" {CARD}/>')
    b.append(T(dx + 16, hy_ + 28, "BY WEEKDAY", "mb", 10, ICE, ls=2))
    wd = D.weekday_totals()
    wmax = max(wd) or 1
    names = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
    top_i = wd.index(wmax)
    for i, v in enumerate(wd):
        yy = hy_ + 48 + i * 14.6
        w_ = max(2, (dw - 32 - 64) * v / wmax)
        b.append(T(dx + 16, yy + 8, names[i], "m", 8.5, GLACIER, ls=.8))
        b.append(f'<rect x="{dx + 52}" y="{yy:.1f}" width="{w_:.1f}" height="9" rx="4.5" fill="{EMBER if i == top_i else GLACIER}" fill-opacity="{1 if i == top_i else .6}" '
                 f'class="grow" style="animation-delay:{0.3 + i * 0.07:.2f}s"/>')
        b.append(T(dx + dw - 14, yy + 8, f"{v:,}", "m", 8.5, ICE, "end"))

    src = "Source: GitHub contribution calendar" + (", including private repositories" if D.INCLUDES_PRIVATE else "") + ". Counts only. Trend badge: last 90 days vs the 90 before."
    b.append(T(PX, PH - 11, src, "m", 8.5, GLACIER))
    b.append("</g>")
    body = f'<g>{head}</g>' + "".join(b)
    return svg(W, top + PH, body, f"Activity dashboard: {D.TOTAL:,} GitHub contributions in the last 12 months across {D.ACTIVE} active days, monthly trend, language mix, daily heatmap and weekday pattern")
