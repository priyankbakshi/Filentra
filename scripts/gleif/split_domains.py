#!/usr/bin/env python3
import pandas as pd, pathlib, sys

if len(sys.argv) < 2:
    print("Usage: split_domains.py <csv_file>")
    sys.exit(1)

src = pathlib.Path(sys.argv[1]).resolve()
out_dir = src.parent / "batches"
out_dir.mkdir(exist_ok=True)

for i, chunk in enumerate(pd.read_csv(src, chunksize=25)):
    chunk.to_csv(out_dir / f"batch_{i:04}.csv", index=False)

print(f"✔ wrote {i+1} batch files to {out_dir}")

