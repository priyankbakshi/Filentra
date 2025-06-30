#!/usr/bin/env python3
"""
Filter validated domains by head-count (>= 200 employees).

Usage
-----
python headcount_filter.py [--no-cb] [--workers 40]

Input  : gleif_domains_v2.csv   (name, domain, country)
Output : gleif_domains_hc.csv   (adds employees column)
"""

import argparse, concurrent.futures as cf, os, re, requests, sys, time
import pandas as pd
from collections import deque
from threading import Lock

# ── CLI ──────────────────────────────────────────────────────────────────────
ap = argparse.ArgumentParser()
ap.add_argument("--no-cb", action="store_true", help="skip Crunchbase")
ap.add_argument("--workers", type=int, default=40, help="thread pool size")
args = ap.parse_args()

# ── Globals ─────────────────────────────────────────────────────────────────
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15)"}
BING_KEY = os.getenv("BING_KEY")           # optional

CB_FAIL_WINDOW = deque(maxlen=3)           # track last 3 CB results
CB_DISABLED    = args.no_cb                # flag turns True if CB hard-fails
CB_LOCK        = Lock()                    # protect shared flag

# ── Helpers ─────────────────────────────────────────────────────────────────
def cb_headcount(name: str) -> int | None:
    """Return max employees from Crunchbase autocomplete."""
    if CB_DISABLED:
        return None
    token = name.split()[0][:50]
    try:
        r = requests.get(
            f"https://www.crunchbase.com/v3.1/autocomplete?query={token}",
            timeout=5)
        r.raise_for_status()
        hi = next((e.get("num_employees_max") for e in r.json().get("entities", [])
                   if e.get("num_employees_max")), None)
    except Exception:
        hi = None
    # auto-disable logic
    with CB_LOCK:
        CB_FAIL_WINDOW.append(bool(hi))
        if not any(CB_FAIL_WINDOW):        # three misses in a row
            globals()["CB_DISABLED"] = True
    return hi

def li_headcount(slug: str) -> int | None:
    """Parse 'xx,xxx employees' from public LinkedIn page."""
    url = f"https://www.linkedin.com/company/{slug}"
    try:
        html = requests.get(url, headers=UA, timeout=6).text
        m = re.search(r'([0-9]{1,3}(?:,[0-9]{3})*)\+?\s+employees', html)
        if m:
            return int(m.group(1).replace(",", ""))
    except Exception:
        pass
    return None

def bing_headcount(name: str) -> int | None:
    """Scrape snippet via Bing Web Search free API (needs BING_KEY)."""
    if not BING_KEY:
        return None
    q = f'"{name}" site:linkedin.com/company "employees"'
    url = f"https://api.bing.microsoft.com/v7.0/search"
    try:
        r = requests.get(url, headers={"Ocp-Apim-Subscription-Key": BING_KEY},
                         params={"q": q, "count": 5}, timeout=6)
        r.raise_for_status()
        for v in r.json().get("webPages", {}).get("value", []):
            m = re.search(r'([0-9]{1,3}(?:,[0-9]{3})*)\+?\s+employees', v["snippet"])
            if m:
                return int(m.group(1).replace(",", ""))
    except Exception:
        pass
    return None

def resolve_emp(row):
    name, dom = row["name"], row["domain"]
    emp = None
    if not CB_DISABLED:
        emp = cb_headcount(name)
    if emp is None:
        emp = li_headcount(dom.split(".")[0])
    if emp is None and BING_KEY:
        emp = bing_headcount(name)
    return emp or 0   # fallback 0

# ── Main ────────────────────────────────────────────────────────────────────
def main():
    src = "gleif_domains_v2.csv"
    dst = "gleif_domains_hc.csv"
    if not os.path.exists(src):
        sys.exit(f"ERROR: {src} not found")

    df = pd.read_csv(src)
    print(f"Processing {len(df):,} domains  •  workers={args.workers}")

    with cf.ThreadPoolExecutor(max_workers=args.workers) as exe:
        df["employees"] = list(exe.map(resolve_emp, df.to_dict("records")))

    kept = df[df["employees"] >= 200]
    kept.to_csv(dst, index=False)
    print(f"✔  kept {len(kept):,} ≥200-employee companies  →  {dst}")

if __name__ == "__main__":
    main()
