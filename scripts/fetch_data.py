#!/usr/bin/env python3
"""Refreshes assets/data.json from the GitHub API (standard library only).

Needs a token in GH_TOKEN (or GITHUB_TOKEN). Usage: fetch_data.py [DATAFILE]

Safety net: GitHub only shows *private* contributions to the account owner (or to anyone, if the
profile setting "Include private contributions on my profile" is on). If the token cannot see
them, the yearly totals would suddenly drop, so the script refuses to overwrite the file and
exits non-zero instead of publishing misleadingly low numbers.
"""
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "assets", "data.json")
API = "https://api.github.com"
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
LEVELS = {"NONE": "0", "FIRST_QUARTILE": "1", "SECOND_QUARTILE": "2", "THIRD_QUARTILE": "3", "FOURTH_QUARTILE": "4"}
LANG_ALIASES = {"Jupyter Notebook": "Jupyter"}
TOP_LANGS = 8
MAX_DROP = 0.8  # a yearly total may not fall below 80% of what is already stored


def _request(url, payload=None):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "profile-telemetry"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    body = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=body, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"::error::{url} -> HTTP {e.code}: {e.read().decode()[:300]}")


def rest(path):
    return _request(API + path)


def graphql(query, variables=None):
    out = _request(API + "/graphql", {"query": query, "variables": variables or {}})
    if out.get("errors"):
        raise SystemExit(f"::error::GraphQL: {json.dumps(out['errors'])[:400]}")
    return out["data"]


def iso(d, end=False):
    return d.strftime("%Y-%m-%dT23:59:59Z" if end else "%Y-%m-%dT00:00:00Z")


def fetch_calendar(login, today):
    """Trailing 365 days: counts + levels, oldest first (GitHub caps one query at a year)."""
    start = today - dt.timedelta(days=364)
    q = """query($login:String!,$from:DateTime!,$to:DateTime!){
      viewer{login}
      user(login:$login){createdAt
        contributionsCollection(from:$from,to:$to){restrictedContributionsCount
          contributionCalendar{weeks{contributionDays{date contributionCount contributionLevel}}}}}}"""
    d = graphql(q, {"login": login, "from": iso(start), "to": iso(today, True)})
    days = {}
    for w in d["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]:
        for day in w["contributionDays"]:
            days[day["date"]] = (day["contributionCount"], LEVELS.get(day["contributionLevel"], "0"))
    counts, levels = [], []
    for i in range(365):
        c, lv = days.get((start + dt.timedelta(days=i)).isoformat(), (0, "0"))
        counts.append(c)
        levels.append(lv)
    private = d["viewer"]["login"].lower() == login.lower() or d["user"]["contributionsCollection"]["restrictedContributionsCount"] > 0
    created = int(d["user"]["createdAt"][:4])
    return start, counts, "".join(levels), private, created


def fetch_years(login, first_year, today):
    parts = []
    for y in range(first_year, today.year + 1):
        to = today if y == today.year else dt.date(y, 12, 31)
        parts.append(f'y{y}:contributionsCollection(from:"{iso(dt.date(y, 1, 1))}",to:"{iso(to, True)}")'
                     "{contributionCalendar{totalContributions}}")
    d = graphql("query($login:String!){user(login:$login){" + " ".join(parts) + "}}", {"login": login})
    return {k[1:]: v["contributionCalendar"]["totalContributions"] for k, v in d["user"].items()}


def fetch_languages(login):
    totals = {}
    page = 1
    repos = []
    while True:
        chunk = rest(f"/users/{login}/repos?type=owner&per_page=100&page={page}")
        repos += chunk
        if len(chunk) < 100:
            break
        page += 1
    for r in repos:
        if r.get("fork") or r.get("private"):
            continue
        for lang, n in rest(f"/repos/{r['full_name']}/languages").items():
            lang = LANG_ALIASES.get(lang, lang)
            totals[lang] = totals.get(lang, 0) + n
    grand = sum(totals.values()) or 1
    top = sorted(totals.items(), key=lambda kv: -kv[1])[:TOP_LANGS]
    return [[k, round(100 * v / grand, 1)] for k, v in top]


def check_not_regressing(old_years, new_years):
    bad = [f"{y}: {old_years[y]} -> {new_years.get(y, 0)}" for y in old_years
           if new_years.get(y, 0) < MAX_DROP * old_years[y]]
    if bad:
        raise SystemExit(
            "::error::Refusing to overwrite telemetry: yearly totals dropped (" + "; ".join(bad) + "). "
            "The token probably cannot see private contributions. Add a repo secret STATS_TOKEN "
            "(a personal access token from the account owner) or turn on 'Include private "
            "contributions on my profile', then re-run the workflow.")


def main():
    with open(DATA_FILE, encoding="utf-8") as f:
        old = json.load(f)
    login = old["login"]
    today = dt.datetime.now(dt.timezone.utc).date()

    start, counts, levels, private, created = fetch_calendar(login, today)
    years = fetch_years(login, created, today)
    check_not_regressing(old["years"], years)

    new = {
        "generated": today.isoformat(),
        "login": login,
        "public_repos": rest(f"/users/{login}")["public_repos"],
        "includes_private": private,
        "window": {"start": start.isoformat(), "counts": counts, "levels": levels},
        "years": years,
        "languages": fetch_languages(login),
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(new, f, separators=(",", ":"))
    print(f"ok: {sum(counts)} contributions in window, years={years}, private={private}")


if __name__ == "__main__":
    main()
