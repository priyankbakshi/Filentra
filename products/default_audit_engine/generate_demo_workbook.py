#!/usr/bin/env python3
"""
Generates a realistic demo workbook hitting every edge-case:
  1. Simple good with illegal defaults  (Red)
  2. Simple good, flags 'N', but numbers ≈ default (manual review)
  3. Complex good, 18 % fallback (Green)
  4. Complex good, 25 % fallback (Red)
  5. Simple good, no defaults (Green)
  6. Metal outlier (73089000) with heading-based defaults, >20 % (Red)
"""
import json, math
from pathlib import Path
from openpyxl import Workbook
from openpyxl.worksheet.datavalidation import DataValidation

ROOT  = Path(__file__).resolve().parent
JSON  = ROOT / "eu_cbam_default_values.json"
OUT   = ROOT / "clients" / "demo" / "importer_data_demo.xlsx"
OUT.parent.mkdir(parents=True, exist_ok=True)

factors = json.loads(JSON.read_text())

def f(cn8_or_heading, kind):
    """Return default factor even if we pass a 4-digit heading."""
    cn = cn8_or_heading
    if len(cn) == 4:                               # heading → find first 8-digit key
        cn = next(k for k in factors if k.startswith(cn))
    return factors[cn][kind]

wb, ws = Workbook(), None
ws = wb.active; ws.title = "AuditInput"
ws.append(["cn_code","mass_tonnes","declared_direct","declared_indirect",
           "used_default_direct","used_default_indirect"])

rows = []

# 1  Simple – defaults illegal
mass=40
d_def = f("26011200","direct")*mass
rows.append(["26011200",mass,d_def,0,"Y","N"])

# 2  Simple – suspicious ‘N’
mass=30
d_def = f("26011200","direct")*mass*1.01
rows.append(["26011200",mass,d_def,0,"N","N"])

# 3  Complex – 18 %
mass=25
ddef=f("72081000","direct")*mass
idef=f("72081000","indirect")*mass
supplier_extra=(ddef+idef)*0.35       # ~18 % ratio
rows.append(["72081000",mass,ddef+supplier_extra,idef,"Y","Y"])

# 4  Complex – 25 %
mass=20
ddef=f("72081000","direct")*mass
idef=f("72081000","indirect")*mass
supplier_extra=(ddef+idef)*0.15
rows.append(["72081000",mass,ddef+supplier_extra,idef,"Y","Y"])

# 5  Simple – no defaults
rows.append(["76012040",18,0,0,"N","N"])

# 6  Outlier 73089000 – >20 %
mass = 22
ddef = f("7308", "direct") * mass        # note we still call with "7308"
rows.append(["73089000", mass, ddef * 1.4, 0, "Y", "N"])

for r in rows:
    ws.append([round(x,3) if isinstance(x,float) else x for x in r])

dv = DataValidation(type="list", formula1='"Y,N"', allow_blank=False)
dv.add("E2:E1000"); dv.add("F2:F1000"); ws.add_data_validation(dv)
wb.save(OUT)
print(f"✅ Demo workbook written → {OUT}")
