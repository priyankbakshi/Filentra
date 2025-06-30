#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stream-filter GLEIF LEI-CDF XML → CSV of EU importers.
Keeps records where
  • country  ∈ TARGET_ISO, and
  • NACE Rev.2 code ∈ TARGET_NACE (first 4 digits)
Outputs gleif_filtered.csv in the same directory.
"""

from pathlib import Path
from lxml import etree
import pandas as pd

# ── PATHS ──────────────────────────────────────────────────────────────────────
XML_SRC  = Path("gleif_20250628.xml")      # your renamed XML file
CSV_DEST = Path("gleif_filtered.csv")

# ── FILTER CRITERIA ───────────────────────────────────────────────────────────
TARGET_ISO  = {"de", "fr", "it", "nl", "es", "pl"}      # top-6 Member States
TARGET_NACE = {"2410", "2420", "4672", "4677"}          # steel, aluminium, traders

NS = {"lei": "http://www.gleif.org/data/schema/leidata/2016"}

def extract(rec, xpath):
    """Helper: return text or empty string."""
    return rec.findtext(xpath, namespaces=NS) or ""

def main() -> None:
    rows = []
    # NOTE: str(XML_SRC)  ← lxml requires a plain string, not Path
    ctx = etree.iterparse(
        str(XML_SRC),
        events=("end",),
        tag="{http://www.gleif.org/data/schema/leidata/2016}LEIRecord",
    )

    for _, rec in ctx:
        country = extract(rec, ".//lei:LegalAddress/lei:Country").lower()
        if country not in TARGET_ISO:
            rec.clear(); continue

        nace = extract(rec, ".//lei:Nace2Code")[:4]
        if nace not in TARGET_NACE:
            rec.clear(); continue

        lei  = extract(rec, ".//lei:LEI")
        name = extract(rec, ".//lei:LegalName")
        rows.append((lei, name, country, nace))
        rec.clear()                       # free memory immediately

    print(f"✔  {len(rows)} matches after country+NACE filter")

    pd.DataFrame(rows, columns=["lei", "name", "country", "nace"])\
      .to_csv(CSV_DEST, index=False)
    print(f"CSV written → {CSV_DEST.resolve()}")

if __name__ == "__main__":
    main()
