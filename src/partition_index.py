"""Inventory local lake partitions the way Glue GetPartitions would."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAKE = ROOT / "lake"


def list_partitions(table_root: Path, key: str = "service_date") -> list[dict]:
    out = []
    if not table_root.exists():
        return out
    for part in sorted(table_root.glob(f"{key}=*")):
        files = [p.name for p in part.iterdir() if p.is_file()]
        out.append(
            {
                "values": [part.name.split("=", 1)[1]],
                "location": str(part).replace(str(LAKE), "s3://hf-open-lake-prod"),
                "files": files,
                "file_count": len(files),
            }
        )
    return out


def main() -> None:
    raw = list_partitions(LAKE / "raw" / "claims")
    curated = list_partitions(LAKE / "curated" / "iceberg_style" / "claims_fact")
    payload = {"hf_raw.claims": raw, "hf_curated.claims_fact": curated}
    out = ROOT / "catalog" / "partitions_inventory.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps({k: len(v) for k, v in payload.items()}, indent=2))


if __name__ == "__main__":
    main()
