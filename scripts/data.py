"""Loads assets/data.json and derives every number the SVGs show. Nothing here is invented:
all values come from the GitHub data that scripts/fetch_data.py stores."""
import datetime as dt
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "assets", "data.json")

with open(DATA_FILE, encoding="utf-8") as _f:
    DATA = json.load(_f)

SNAPSHOT = dt.date.fromisoformat(DATA["generated"])
WIN_START = dt.date.fromisoformat(DATA["window"]["start"])
COUNTS = [int(c) for c in DATA["window"]["counts"]]
DAYS = [WIN_START + dt.timedelta(days=i) for i in range(len(COUNTS))]
MONTH_ABBR = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
LANGS = [(n, float(p)) for n, p in DATA["languages"]]
PUBLIC_REPOS = int(DATA["public_repos"])
INCLUDES_PRIVATE = bool(DATA.get("includes_private"))


def _levels():
    lv = DATA["window"].get("levels")
    if lv and len(lv) == len(COUNTS):
        return lv
    nz = sorted(c for c in COUNTS if c)
    if not nz:
        return "0" * len(COUNTS)
    q = [nz[int(len(nz) * f)] for f in (0.25, 0.5, 0.75)]
    return "".join("0" if c == 0 else "1" if c <= q[0] else "2" if c <= q[1] else "3" if c <= q[2] else "4" for c in COUNTS)


LEVELS = _levels()
TOTAL = sum(COUNTS)
ACTIVE = sum(1 for c in COUNTS if c)


def months():
    """[(label, total, active_days, is_partial)] in chronological order."""
    out = {}
    for d, c in zip(DAYS, COUNTS):
        k = (d.year, d.month)
        t = out.setdefault(k, [0, 0, 0])
        t[0] += c
        t[1] += 1 if c else 0
        t[2] += 1
    res = []
    for (y, m), (tot, act, n) in out.items():
        full = (dt.date(y + (m == 12), m % 12 + 1, 1) - dt.date(y, m, 1)).days
        res.append((MONTH_ABBR[m - 1], tot, act, n < full, y))
    return res


MONTHS = months()
PEAK = max(MONTHS, key=lambda m: m[1])
PEAK_LABEL = f"{PEAK[0]} {PEAK[4]}"


def weekly():
    """Contribution totals per 7-day block (oldest first)."""
    return [sum(COUNTS[i:i + 7]) for i in range(0, len(COUNTS), 7)]


def weekday_totals():
    """Sunday-first totals."""
    t = [0] * 7
    for d, c in zip(DAYS, COUNTS):
        t[(d.weekday() + 1) % 7] += c
    return t


def streaks():
    best = cur = 0
    for c in COUNTS:
        cur = cur + 1 if c else 0
        best = max(best, cur)
    now = 0
    for c in reversed(COUNTS):
        if c:
            now += 1
        else:
            break
    return best, now


LONGEST, CURRENT = streaks()


def delta_90():
    """Last 90 days vs the 90 days before, as a percentage (None if no baseline)."""
    last, prev = sum(COUNTS[-90:]), sum(COUNTS[-180:-90])
    return None if prev == 0 else round(100 * (last - prev) / prev)


DELTA = delta_90()
