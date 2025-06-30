#!/usr/bin/env python3
"""
Validate Clearbit-guessed domains:

  • similarity ≥ 0.85 between legal-name token and (a) domain label or (b) Clearbit’s name
  • DNS resolves (MX or A)
  • <title> of the homepage contains the main token

Outputs:
    gleif_domains_pass.csv   – domains that pass all tests
    gleif_domains_fail.csv   – rejects (for fallback resolver)

Expected input columns in gleif_domains.csv:
    lei , name , domain , country , [optional] cb_name
"""

import pandas as pd, re, requests, dns.resolver, tldextract, jellyfish
from bs4 import BeautifulSoup

# ── constants ────────────────────────────────────────────────────────────────
SUFFIX_RE = re.compile(
    r'\b(ag|gmbh|sa|nv|srl|spa|sp\s*z\s*o\s*o|ltd|plc|sas|oy|ab|bv|as)\b',
    re.I,
)
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15)"}

# ── helper functions ─────────────────────────────────────────────────────────
def core_token(txt: str) -> str:
    """First significant word after stripping corp suffixes & symbols."""
    clean = SUFFIX_RE.sub("", txt or "")
    clean = re.sub(r"[^A-Za-z]", " ", clean).lower().strip()
    return clean.split()[0] if clean else ""

def dns_ok(domain: str) -> bool:
    try:
        dns.resolver.resolve(domain, "MX", lifetime=3)
        return True
    except Exception:
        try:
            dns.resolver.resolve(domain, "A", lifetime=3)
            return True
        except Exception:
            return False

def title_ok(domain: str, token: str) -> bool:
    try:
        html = requests.get(f"https://{domain}", headers=UA, timeout=4).text[:8000]
        title = BeautifulSoup(html, "html.parser").title
        return token in title.text.lower() if title else False
    except Exception:
        return False

def accept(row) -> bool:
    token   = core_token(row["name"])
    if not token:
        return False

    # similarity vs domain label
    label   = tldextract.extract(row["domain"]).domain.lower()
    sim_dom = jellyfish.jaro_winkler(token, label)

    # similarity vs Clearbit’s canonical name (if present)
    cb_name = core_token(row.get("cb_name", row["name"]))
    sim_cb  = jellyfish.jaro_winkler(token, cb_name)

    if max(sim_dom, sim_cb) < 0.85:
        return False

    return dns_ok(row["domain"]) and title_ok(row["domain"], token)

# ── main ─────────────────────────────────────────────────────────────────────
def main() -> None:
    df = pd.read_csv("gleif_domains.csv")  # must have lei,name,domain,country [+ cb_name]

    # guarantee cb_name exists even if Clearbit didn’t supply it
    if "cb_name" not in df.columns:
        df["cb_name"] = df["name"]

    good, bad = [], []
    for _, row in df.iterrows():
        (good if accept(row) else bad).append(row)

    pd.DataFrame(good).to_csv("gleif_domains_pass.csv", index=False)
    pd.DataFrame(bad ).to_csv("gleif_domains_fail.csv", index=False)
    print(f"✔ kept {len(good):,}  |  rejected {len(bad):,}")

if __name__ == "__main__":
    main()
