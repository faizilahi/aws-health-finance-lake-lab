# Open Health-Finance Lake on S3: Glue Catalog Tables, Athena Partition Pruning, and a Worked Query

Faiz Elahi — [LinkedIn](https://www.linkedin.com/in/faizilahi) — [pendataco.com](https://pendataco.com) — [GitHub](https://github.com/faizilahi)

Claim and remittance objects under `lake/` are generated.

## S3 layout (local stand-in under `lake/`)

```
s3://hf-open-lake-prod/
  raw/claims/service_date=YYYY-MM-DD/part-*.csv
  raw/remits/service_date=YYYY-MM-DD/part-*.csv
  curated/iceberg_style/claims_fact/service_date=YYYY-MM-DD/*.parquet
  scripts/
  athena-results/
```

This repo mirrors that prefix tree under `lake/` so every path in the Glue JSON and Athena SQL is real on disk.

## Glue-style catalog

`catalog/glue_tables.json` declares two external tables:

- `hf_raw.claims` — CSV SerDe, partitioned by `service_date`
- `hf_curated.claims_fact` — Parquet, partitioned by `service_date`

`catalog/glue_tables.sql` is the equivalent DDL you would run in Athena/`glue create-table`.

## Athena query that prunes partitions

`sql/athena_paid_by_payer_pruned.sql` filters `service_date BETWEEN date '2025-08-01' AND date '2025-08-03'`. The local DuckDB runner prints **files read** vs **files skipped** to show partition pruning — the teaching stand-in for Athena's partition projection / MSCK behavior.

## Worked query with row counts

| Step | Rows |
|------|------|
| Raw claims in window (3 days) | printed by runner |
| After remit inner join | printed by runner |
| Final payer aggregate | printed by runner |

## IAM note

The query role `athena-hf-analyst` needs:

- `s3:GetObject` + `s3:ListBucket` on `arn:aws:s3:::hf-open-lake-prod/curated/*` and the Athena results bucket
- `glue:GetTable`, `glue:GetPartitions` on database `hf_curated`
- **No** `s3:PutObject` on `raw/` — analysts read curated only

See `docs/iam_athena_analyst.md`.

## Run

```powershell
cd aws-health-finance-lake-lab
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/build_lake_tree.py
python src/run_athena_standin.py
```
