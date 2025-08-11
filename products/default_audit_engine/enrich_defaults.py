#!/usr/bin/env python3
"""
Filentra – CBAM Default-Enrichment & Validation
"""

import argparse
import json
import sys
import yaml
from pathlib import Path
import pandas as pd

# ---------- CLI ------------------------------------------------------------
cli = argparse.ArgumentParser()
cli.add_argument("--input", required=True, help="Path to importer_data.xlsx")
cli.add_argument("--out",   required=True, help="Destination enriched CSV")
cli.add_argument("--raw",   required=True, help="Destination raw CSV copy")
cli.add_argument(
    "--json",
    default="eu_cbam_default_values.json",
    help="EU default-factor JSON (default: %(default)s)",
)
args = cli.parse_args()

XLS_IN  = Path(args.input)
RAW_OUT = Path(args.raw)
ENRICHED = Path(args.out)
JSON_IN  = Path(args.json)

# ---------- load EU factors ------------------------------------------------
try:
    factors: dict = json.loads(JSON_IN.read_text())
except FileNotFoundError:
    sys.exit(f"❌ EU default-factor file not found: {JSON_IN}")

CBAM_SET = set(factors.keys())  # exhaustive 8-digit keys straight from JSON

SPECIAL_FACTORS = {
    "73089000": "7308",  # roll up to 4-digit heading
    "76071100": "7607",  # roll up to 4-digit heading
    "27160000": None,    # electricity – no default factors
}

# ---------- load complexity map -------------------------------------------
MAP_FILE = Path(__file__).with_name("cn_code_complexity_map.yaml")
raw_map = yaml.safe_load(MAP_FILE.read_text())
CN_MAP = {str(k): v for k, v in raw_map.items()}
if "default" not in CN_MAP:
    CN_MAP["default"] = "complex"


def is_simple(cn: str) -> bool:
    cn = str(cn)                    
    root4 = cn[:4]
    return CN_MAP.get(root4, CN_MAP["default"]) == "simple"


# ---------- helper: is CBAM good? -----------------------------------------
def is_cbam(cn: str) -> bool:
    cn = str(cn)                    
    d = ''.join(filter(str.isdigit, cn))
    return d in CBAM_SET or d in SPECIAL_FACTORS


# ---------- helper: fetch default factor ----------------------------------
def factor(cn: str, kind: str):
    cn = str(cn)
    d = "".join(filter(str.isdigit, cn))

    # 1) exact 8-digit hit
    entry = factors.get(d)
    if entry and kind in entry:
        return float(entry[kind])

    # 2) metal outliers – roll up to first 8-digit key under the heading
    if d in ("73089000", "76071100"):
        heading = SPECIAL_FACTORS[d]  # "7308" or "7607"
        try:
            hdr_entry = next(
                factors[k] for k in factors.keys() if k.startswith(heading)
            )
            return float(hdr_entry[kind])
        except StopIteration:
            return None   # should never happen if EU file is complete

    # 3) electricity – no factors
    if d == "27160000":
        return None

    # 4) everything else → no factor
    return None

# ---------- ingest workbook -----------------------------------------------
df = pd.read_excel(XLS_IN, sheet_name="AuditInput").fillna("")
df.to_csv(RAW_OUT, index=False)           # immutable trace-copy

# ---------- column sanity --------------------------------------------------
required = {
    "cn_code","mass_tonnes",
    "declared_direct","declared_indirect",
    "used_default_direct","used_default_indirect",
}
miss = required - set(df.columns)
if miss:
    sys.exit(f"❌ Missing columns: {', '.join(miss)}")

# Y/N flags check
for col in ("used_default_direct","used_default_indirect"):
    bad = df[col].apply(lambda v: str(v).upper() not in ("Y","N"))
    if bad.any():
        sys.exit(f"❌ Column {col} must contain only Y/N flags.")

# ---------- CBAM-goods validation -----------------------------------------
non_cbam = df[~df.cn_code.apply(is_cbam)]
if not non_cbam.empty:
    sys.exit(
        f"❌ These CN codes are NOT CBAM goods: "
        f"{', '.join(non_cbam.cn_code.astype(str))}"
    )

# ---------- block defaults on simple goods (2601 / 7601) ------------------
simple_used_default = (
    df.loc[df.cn_code.apply(is_simple), ["used_default_direct", "used_default_indirect"]]
      .applymap(lambda x: str(x).upper() == "Y")   # → True/False matrix
      .any(axis=None)                              # → single bool
)

if simple_used_default:
    sys.exit("❌ Simple goods (2601/7601) cannot use defaults – fix flags.")

# ---------- compute default_* ---------------------------------------------
def calc(row, kind):
    if row[f"used_default_{kind}"].upper() == "Y":
        f = factor(row.cn_code, kind)
        if f is None:
            raise ValueError(
                f"No EU default factor for CN {row.cn_code} ({kind}). "
                "Set flag to 'N' or provide supplier data."
            )
        return f * float(row.mass_tonnes)
    return 0.0

df["default_direct"]   = df.apply(lambda r: calc(r,"direct"), axis=1)
df["default_indirect"] = df.apply(lambda r: calc(r,"indirect"), axis=1)

# ---------- export ---------------------------------------------------------
df[["cn_code","declared_direct","declared_indirect",
    "default_direct","default_indirect"]].to_csv(ENRICHED, index=False)

print(f"✅  Raw      → {RAW_OUT}")
print(f"✅  Enriched → {ENRICHED}")
