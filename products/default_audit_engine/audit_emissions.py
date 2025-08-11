#!/usr/bin/env python3
"""
Filentra CBAM Fallback-Audit Engine  –  v2025-07-11
---------------------------------------------------
Input : importer_enriched.csv   (must have default_* columns)
Output: audited_results.xlsx (or .csv) with Green/Red flags
"""
from pathlib import Path
import pandas as pd, yaml, sys

MAP_FILE = Path("cn_code_complexity_map.yaml")
REQUIRED = {
    "cn_code",
    "declared_direct", "declared_indirect",
    "default_direct",  "default_indirect",
}

# ---------------- helpers --------------------------------------------------
try:
    raw_map = yaml.safe_load(MAP_FILE.read_text())
    CN_MAP = {str(k): v for k, v in raw_map.items()}
except yaml.YAMLError:
    # If someone swaps to JSON, keep it working
    import json
    raw_map = json.loads(MAP_FILE.read_text())
    CN_MAP = {str(k): v for k, v in raw_map.items()}

if "default" not in CN_MAP:
    CN_MAP["default"] = "complex"

def normalise(cn):                      # 4-digit root
    d = "".join(filter(str.isdigit, str(cn)))
    if len(d) not in (4, 6, 8):
        raise ValueError(f"CN code ‘{cn}’ must be 4, 6 or 8 digits.")
    return d[:4]

def complexity(root):                   # 'simple' / 'complex'
    return CN_MAP.get(root, CN_MAP["default"])

def ratio(row):
    tot = row.declared_direct + row.declared_indirect
    if tot == 0:
        # No declared emissions AND no defaults → ratio = 0
        if row.default_direct + row.default_indirect == 0:
            return 0.0
        # Defaults present but no declared total (invalid data) → error
        raise ZeroDivisionError(f"Declared emissions = 0 but defaults > 0 for {row.cn_code}")
    return (row.default_direct + row.default_indirect) / tot


def flag(row):
    if row.complexity == "simple":
        return "Red" if row.fallback_ratio > 0 else "Green"
    return "Red" if row.fallback_ratio > 0.20 else "Green"
# ---------------------------------------------------------------------------

def audit(inp: Path, out: Path):
    df = pd.read_csv(inp) if inp.suffix == ".csv" else pd.read_excel(inp)
    miss = REQUIRED - set(df.columns)
    if miss:
        sys.exit(f"Missing cols: {', '.join(miss)}")

    df["cn_root_4d"]  = df.cn_code.apply(normalise)
    df["complexity"]  = df.cn_root_4d.apply(complexity)
    df["fallback_ratio"] = df.apply(ratio, axis=1)
    df["fallback_ratio_%"] = (df.fallback_ratio*100).round(1)
    df["Flag"] = df.apply(flag, axis=1)

    if out.suffix == ".csv":
        df.to_csv(out, index=False)
    else:
        df.to_excel(out, index=False)
    print(f"✅ QC file written → {out}")

if __name__ == "__main__":
    import argparse, textwrap
    p = argparse.ArgumentParser(description="CBAM fallback-cap audit")
    p.add_argument("inp",  help="importer_enriched.csv/.xlsx")
    p.add_argument("-o", "--out", required=True,
                   help="audited_results.xlsx or .csv")
    a = p.parse_args()
    audit(Path(a.inp), Path(a.out))
