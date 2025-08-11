#!/usr/bin/env python3
import pandas as pd, requests, re, concurrent.futures, dns.resolver, socket, pathlib, json, time

SRC  = pathlib.Path("gleif_country_filtered.csv")
DEST = pathlib.Path("gleif_domains.csv")
ISO2 = {"de":".de","fr":".fr","it":".it","nl":".nl","es":".es","pl":".pl"}

def clearbit_domain(name):
    q = name.split()[0][:50]      # keep query short
    url = f"https://autocomplete.clearbit.com/v1/companies/suggest?query={q}"
    try:
        r = requests.get(url, timeout=4)
        if r.ok:
            data = r.json()
            if data:
                return data[0]["domain"]
    except Exception:
        pass
    return None

def brute_domain(name, cc_tld):
    slug = re.sub(r'[^a-z0-9]', '', name.lower().split()[0])
    for tld in (".com", cc_tld):
        dom = f"{slug}{tld}"
        try:
            dns.resolver.resolve(dom, "A", lifetime=2)
            return dom
        except Exception:
            continue
    return None

def resolver(row):
    name, country = row["name"], row["country"]
    dom = clearbit_domain(name)
    if not dom:
        dom = brute_domain(name, ISO2.get(country, ""))
    return row["lei"], name, dom, country

def main():
    df   = pd.read_csv(SRC, usecols=["lei","name","country"]).head(120000)  # cap tonight
    with concurrent.futures.ThreadPoolExecutor(max_workers=40) as exe:
        out = list(exe.map(resolver, df.to_dict("records")))
    seen, rows = set(), []
    for lei, name, dom, country in out:
        if dom and dom not in seen:
            rows.append((lei, name, dom, country))
            seen.add(dom)
    pd.DataFrame(rows, columns=["lei","name","domain","country"]).to_csv(DEST, index=False)
    print("✔ domains:", len(rows))

if __name__ == "__main__":
    main()
