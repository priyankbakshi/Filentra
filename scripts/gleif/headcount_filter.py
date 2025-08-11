#!/usr/bin/env python3
import argparse, concurrent.futures as cf, os, re, requests, sys, time
import pandas as pd, urllib.parse as up
from threading import Lock

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15)"}
CB_TO, LI_TO, DDG_TO = 4, 6, 6
MIN_EMP = 100            # raise to 200 after first scrape

ap = argparse.ArgumentParser()
ap.add_argument("--workers", type=int, default=40)
args = ap.parse_args()

slug_re = re.compile(r"linkedin\.com/company/([^/?#\"']+)", re.I)

def li_headcount(slug):
    try:
        html = requests.get(f"https://www.linkedin.com/company/{slug}",
                            headers=UA, timeout=LI_TO).text
        m = re.search(r'([0-9,]+)\+?\s+employees', html)
        if m:
            return int(m.group(1).replace(",", ""))
    except Exception:
        pass
    return None

def slug_from_cb(name):
    try:
        j = requests.get(f"https://www.crunchbase.com/v3.1/autocomplete?query={name.split()[0][:50]}",
                         timeout=CB_TO).json()
        for e in j.get("entities", []):
            s = e.get("permalink", "")
            if s.startswith("/company/"):
                return s.split("/", 2)[2]
    except Exception:
        pass
    return None

def slug_from_ddg(name):
    q = up.quote_plus(f"{name} linkedin")
    try:
        html = requests.get(f"https://duckduckgo.com/html/?q={q}", headers=UA, timeout=DDG_TO).text
        m = slug_re.search(html)
        if m:
            return m.group(1)
    except Exception:
        pass
    return None

def resolve_emp(row):
    name, dom = row["name"], row["domain"]
    for slug in (
        dom.split(".")[0],
        slug_from_cb(name),
        slug_from_ddg(name),
    ):
        if slug:
            emp = li_headcount(slug)
            if emp: return emp
    return 0

def main():
    src, dst = "gleif_domains_v2.csv", "gleif_domains_hc.csv"
    if not os.path.exists(src):
        sys.exit("gleif_domains_v2.csv not found")
    df = pd.read_csv(src)
    processed = kept = 0; lock = Lock()

    def wrapped(r):
        nonlocal processed, kept
        e = resolve_emp(r)
        with lock:
            processed += 1
            if e >= MIN_EMP: kept += 1
            if processed % 1_000 == 0:
                print(f"{time.strftime('%H:%M:%S')}  processed {processed:,} | kept {kept:,}", flush=True)
        return e

    with cf.ThreadPoolExecutor(max_workers=args.workers) as exe:
        df["employees"] = list(exe.map(wrapped, df.to_dict("records")))
    df = df[df["employees"] >= MIN_EMP]
    df.to_csv(dst, index=False)
    print(f"✔ kept {len(df):,} rows  →  {dst}")

if __name__ == "__main__":
    main()
