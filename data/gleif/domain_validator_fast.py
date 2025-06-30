#!/usr/bin/env python3
"""
Multithreaded domain validator  (Python 3.8-compatible)

Input : gleif_domains_COPY.csv
Output: gleif_domains_pass.csv / gleif_domains_fail.csv
"""

import concurrent.futures as cf
import dns.resolver, jellyfish, os, pandas as pd, re, requests, sys, time, tldextract
from bs4 import BeautifulSoup
from typing import Tuple
from threading import Lock

# ── CONFIG ──────────────────────────────────────────────────────────────────
INFILE      = "gleif_domains_COPY.csv"   # work on the copy, not the original
PASS_CSV    = "gleif_domains_pass.csv"
FAIL_CSV    = "gleif_domains_fail.csv"
WORKERS     = 50
DNS_TIMEOUT = 1     # seconds
HTTP_TIMEOUT= 2
PROGRESS_EVERY = 1_000

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15)"}
SUFFIX_RE = re.compile(r"\b(ag|gmbh|sa|nv|srl|spa|sp\s*z\s*o\s*o|ltd|plc|sas|oy|ab|bv|as)\b", re.I)

# ── helpers ─────────────────────────────────────────────────────────────────
def core_token(txt: str) -> str:
    clean = SUFFIX_RE.sub("", txt or "")
    clean = re.sub(r"[^A-Za-z]", " ", clean).lower().strip()
    return clean.split()[0] if clean else ""

def dns_ok(domain: str) -> bool:
    try:
        dns.resolver.resolve(domain, "MX", lifetime=DNS_TIMEOUT); return True
    except Exception:
        try:
            dns.resolver.resolve(domain, "A", lifetime=DNS_TIMEOUT); return True
        except Exception:
            return False

def title_ok(domain: str, token: str) -> bool:
    try:
        html = requests.get(f"https://{domain}", headers=UA, timeout=HTTP_TIMEOUT).text[:8000]
        t = BeautifulSoup(html, "html.parser").title
        return token in t.text.lower() if t else False
    except Exception:
        return False

def accept(row: dict) -> Tuple[bool, dict]:   # <-- old-style typing
    token = core_token(row["name"])
    if not token:
        return False, row
    label   = tldextract.extract(row["domain"]).domain.lower()
    cb_name = core_token(row.get("cb_name", row["name"]))
    sim     = max(
        jellyfish.jaro_winkler_similarity(token, label),
        jellyfish.jaro_winkler_similarity(token, cb_name),
    )
    if sim < 0.85:
        return False, row
    if not dns_ok(row["domain"]):
        return False, row
    if not title_ok(row["domain"], token):
        return False, row
    return True, row

# ── threaded driver ─────────────────────────────────────────────────────────
def main() -> None:
    if not os.path.exists(INFILE):
        sys.exit(f"ERROR: {INFILE} not found")

    df = pd.read_csv(INFILE)
    good, bad = [], []
    counter, lock = 0, Lock()

    def worker(r):
        nonlocal counter
        ok, row = accept(r)
        with lock:
            counter += 1
            if counter % PROGRESS_EVERY == 0:
                print(f"{time.strftime('%H:%M:%S')}  processed {counter:,}", flush=True)
        return ok, row

    with cf.ThreadPoolExecutor(max_workers=WORKERS) as exe:
        for ok, row in exe.map(worker, df.to_dict("records")):
            (good if ok else bad).append(row)

    pd.DataFrame(good).to_csv(PASS_CSV, index=False)
    pd.DataFrame(bad ).to_csv(FAIL_CSV , index=False)
    print(f"✔ kept {len(good):,}  |  rejected {len(bad):,}")

if __name__ == "__main__":
    main()
