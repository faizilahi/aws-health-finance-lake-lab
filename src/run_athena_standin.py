"""DuckDB stand-in for Athena: partition pruning demo + worked row counts."""
from __future__ import annotations

from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
CURATED = ROOT / "lake" / "curated" / "iceberg_style" / "claims_fact"


def main() -> None:
    all_parts = sorted(CURATED.glob("service_date=*"))
    window = {"2025-08-01", "2025-08-02", "2025-08-03"}
    selected = [p for p in all_parts if p.name.split("=", 1)[1] in window]
    skipped = [p for p in all_parts if p not in selected]

    print(f"partition_files_total={len(all_parts)}")
    print(f"partition_files_read={len(selected)} -> {[p.name for p in selected]}")
    print(f"partition_files_skipped={len(skipped)} -> {[p.name for p in skipped]}")

    con = duckdb.connect()
    # Register only pruned partitions (Athena would push the predicate to Glue partitions)
    files = [str(p / "part-000.parquet") for p in selected]
    if not files:
        raise SystemExit("Run scripts/build_lake_tree.py first")

    con.execute(
        f"""
        CREATE OR REPLACE VIEW claims_fact AS
        SELECT *,
               regexp_extract(filename, 'service_date=([0-9-]+)', 1) AS service_date
        FROM read_parquet({files}, filename=true)
        """
    )

    raw_count = con.execute("SELECT COUNT(*) FROM claims_fact").fetchone()[0]
    joined_paid = con.execute(
        "SELECT COUNT(*) FROM claims_fact WHERE paid_amount IS NOT NULL"
    ).fetchone()[0]
    print(f"worked_raw_claims_in_window={raw_count}")
    print(f"worked_rows_with_remit={joined_paid}")

    result = con.execute(
        """
        SELECT payer,
               COUNT(*) AS claim_lines,
               ROUND(SUM(allowed_amount), 2) AS allowed_amount,
               ROUND(SUM(paid_amount), 2) AS paid_amount
        FROM claims_fact
        WHERE CAST(service_date AS DATE) BETWEEN DATE '2025-08-01' AND DATE '2025-08-03'
        GROUP BY payer
        ORDER BY paid_amount DESC
        """
    ).fetchall()
    print("worked_payer_aggregate:")
    for row in result:
        print(" ", row)
    print(f"worked_aggregate_groups={len(result)}")


if __name__ == "__main__":
    main()
