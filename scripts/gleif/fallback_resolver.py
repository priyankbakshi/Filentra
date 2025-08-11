#!/usr/bin/env python3
import pandas as pd, requests, re, time, random, dns.resolver, tldextract, jellyfish
from bs4 import BeautifulSoup

SUFFIX = re.compile(r'\b(ag|gmbh|sa|nv|srl|spa|sp\s*z\s*o\s*o|ltd|plc|sas|oy|ab|bv|as)\b', re.I)
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15)"}

def core_token(txt):
    clean = SUFFIX.sub("", txt or "")
    clean = re.sub(r"[^A-Za-z]", " ", clean).lower().strip()
    return clean.split()[0] if clean else ""

def dns_ok(dom):
    try:
        dns.resolver.resolve(dom, "MX", lifetime=3); return True
    except Exception:
        try: dns.resolver.resolve(dom, "A", lifetime=3); return True
        except Exception: return False

def title_ok(dom, tok):
    try:
        html = requests.get(f"https://{dom}", headers=UA, timeout=4).text[:8000]
        t = BeautifulSoup(html, "html.parser").title
        return tok in t.text.lower() if t else False
    except Exception: return False

def sim_ok(tok, dom_label, alt):
    return max(
        jellyfish.jaro_winkler_similarity(tok, dom_label),
        jellyfish.jaro_winkler_similarity(tok, alt),
    ) >= 0.85

def cb_domain(tok):
    url=f"https://www.crunchbase.com/v3.1/autocomplete?query={tok}"
    try:
        j=requests.get(url,timeout=5).json()
        for h in j.get("entities",[]):
            d=h.get("domain"); alt=h.get("name","")
            if d: return d.lower(),alt
    except Exception: pass
    return None,None

def li_domain(tok):
    url=f"https://www.linkedin.com/company/{tok}"
    try:
        html=requests.get(url,headers=UA,timeout=6).text[:12000]
        m=re.search(r'data-tracking-control-name="org-top-card-primary-link[^"]+" href="https://([^"]+)"',html)
        if m: return m.group(1).lower(),tok
    except Exception: pass
    return None,None

def main():
    bad=pd.read_csv("gleif_domains_fail.csv")
    out=[]
    for _,r in bad.iterrows():
        tok=core_token(r["name"])
        dom,alt=cb_domain(tok)
        if dom and dns_ok(dom) and title_ok(dom,tok) and sim_ok(tok,tldextract.extract(dom).domain,alt):
            r["domain"],r["cb_name"]=dom,alt; out.append(r); continue
        dom,alt=li_domain(tok)
        if dom and dns_ok(dom) and title_ok(dom,tok) and sim_ok(tok,tldextract.extract(dom).domain,alt):
            r["domain"],r["cb_name"]=dom,alt; out.append(r)
        time.sleep(random.uniform(0.2,0.4))
    pd.DataFrame(out).to_csv("fallback_hits.csv",index=False)
    print(f"✔ rescued {len(out):,} domains")

if __name__=="__main__":
    main()
