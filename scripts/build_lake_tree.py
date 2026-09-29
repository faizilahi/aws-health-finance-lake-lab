"""Build curated parquet partitions from raw CSV drops (local S3 stand-in)."""
from __future__ import annotations

from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
LAKE = ROOT / "lake"
con = duckdb.connect()

raw_claims = list((LAKE / "raw" / "claims").glob("service_date=*"))
print(f"raw_partitions={len(raw_claims)}")

for part in sorted(raw_claims):
    sd = part.name.split("=", 1)[1]
    csv_path = part / "part-000.csv"
    remit_path = LAKE / "raw" / "remits" / f"service_date={sd}" / "part-000.csv"
    out = LAKE / "curated" / "iceberg_style" / "claims_fact" / f"service_date={sd}"
    out.mkdir(parents=True, exist_ok=True)
    if remit_path.exists():
        con.execute(
            f"""
            COPY (
              SELECT c.*, r.paid_amount, r.remit_id
              FROM read_csv_auto('{csv_path.as_posix()}') c
              INNER JOIN read_csv_auto('{remit_path.as_posix()}') r
                ON c.claim_line_id = r.claim_line_id
            ) TO '{(out / 'part-000.parquet').as_posix()}' (FORMAT PARQUET)
            """
        )
    else:
        con.execute(
            f"""
            COPY (
              SELECT *, CAST(NULL AS DOUBLE) AS paid_amount, CAST(NULL AS VARCHAR) AS remit_id
              FROM read_csv_auto('{csv_path.as_posix()}')
            ) TO '{(out / 'part-000.parquet').as_posix()}' (FORMAT PARQUET)
            """
        )
    print("curated", sd)
