#!/usr/bin/env python3
"""
Threaded fallback resolver with live progress.

Reads : gleif_domains_fail.csv
Writes: fallback_hits.csv

• 50 worker threads  (I/O-bound)
• DNS   timeout 1 s
• HTTP  timeout 2 s
• Progress print every 1 000 rows
"""

import concurrent.futures as cf, dns.resolver, jellyfish, pandas as pd, re
import requests, tldextract, time
from threading import Lock

# ── CONFIG ──────────────────────────────────────────────────────────────────
WORKERS      = 50
DNS_TIMEOUT  = 1      # seconds
HTTP_TIMEOUT = 2
PROGRESS_EVERY = 1_000

UA = {"User-Agent": "Mozilla/5.0"}
SUF = re.compile(r'\b(ag|gmbh|sa|nv|srl|spa|sp\s*z\s*o\s*o|ltd|plc|sas|oy|ab|bv|as)\b', re.I)

# ── helper funcs ────────────────────────────────────────────────────────────
def core(txt: str) -> str:
    return re.sub(r'[^a-z]', ' ', SUF.sub('', txt.lower())).split()[0]

def dns_ok(domain: str) -> bool:
    try:
        dns.resolver.resolve(domain, "MX", lifetime=DNS_TIMEOUT); return True
    except Exception:
        try: dns.resolver.resolve(domain, "A", lifetime=DNS_TIMEOUT); return True
        except Exception: return False

def sim_ok(tok, dom_label, alt_name) -> bool:
    return max(
        jellyfish.jaro_winkler_similarity(tok, dom_label),
        jellyfish.jaro_winkler_similarity(tok, alt_name),
    ) >= 0.85

def cb_domain(token):
    try:
        j = requests.get(
            f"https://www.crunchbase.com/v3.1/autocomplete?query={token}",
            timeout=HTTP_TIMEOUT).json()
        for hit in j.get("entities", []):
            if hit.get("domain"):
                return hit["domain"].lower(), core(hit.get("name", ""))
    except Exception:
        pass
    return None, None

def li_domain(token):
    try:
        html = requests.get(
            f"https://www.linkedin.com/company/{token}",
            headers=UA, timeout=HTTP_TIMEOUT).text[:12000]
        m = re.search(
            r'data-tracking-control-name="org-top-card-primary-link[^"]+" href="https://([^"]+)"',
            html)
        if m:
            return m.group(1).lower(), token
    except Exception:
        pass
    return None, None

# ── threaded worker ─────────────────────────────────────────────────────────
def rescue(row):
    tok = core(row["name"])
    for fn in (cb_domain, li_domain):
        dom, alt = fn(tok)
        if dom and dns_ok(dom) and sim_ok(tok, tldextract.extract(dom).domain, alt):
            row["domain"], row["cb_name"] = dom, alt
            return row
    return None

# ── main driver ─────────────────────────────────────────────────────────────
def main():
    bad = pd.read_csv("gleif_domains_fail.csv")
    hits, scanned = [], 0
    lock = Lock()

    def wrapper(r):
        nonlocal scanned
        res = rescue(r)
        with lock:
            scanned += 1
            if scanned % PROGRESS_EVERY == 0:
                print(f"{time.strftime('%H:%M:%S')}  rescued {len(hits):,} / scanned {scanned:,}", flush=True)
        if res:
            hits.append(res)

    with cf.ThreadPoolExecutor(max_workers=WORKERS) as exe:
        exe.map(wrapper, bad.to_dict("records"))

    pd.DataFrame(hits).to_csv("fallback_hits.csv", index=False)
    print(f"✔ rescued {len(hits):,} domains  (scanned {scanned:,})")

if __name__ == "__main__":
    main()
