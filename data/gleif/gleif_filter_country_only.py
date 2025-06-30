#!/usr/bin/env python3
from pathlib import Path
from lxml import etree
import pandas as pd

XML_SRC  = Path("gleif_20250628.xml")
CSV_DEST = Path("gleif_country_filtered.csv")

TARGET_ISO = {"de", "fr", "it", "nl", "es", "pl"}
NS = {"lei": "http://www.gleif.org/data/schema/leidata/2016"}

def extract(rec, xpath):
    return rec.findtext(xpath, namespaces=NS) or ""

def main():
    rows = []
    ctx = etree.iterparse(
        str(XML_SRC),
        events=("end",),
        tag="{http://www.gleif.org/data/schema/leidata/2016}LEIRecord",
    )
    for _, rec in ctx:
        country = extract(rec, ".//lei:LegalAddress/lei:Country").lower()
        if country not in TARGET_ISO:
            rec.clear(); continue
        lei  = extract(rec, ".//lei:LEI")
        name = extract(rec, ".//lei:LegalName")
        rows.append((lei, name, country))
        rec.clear()

    print(f"✔  {len(rows)} records from target countries")
    pd.DataFrame(rows, columns=["lei","name","country"]).to_csv(CSV_DEST, index=False)
    print(f"CSV written → {CSV_DEST.resolve()}")

if __name__ == "__main__":
    main()
