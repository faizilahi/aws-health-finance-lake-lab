# S3 prefix conventions

| Prefix | Producer | Consumer |
|--------|----------|----------|
| `raw/claims/service_date=.../` | nightly extract pod | Glue crawler / Athena raw |
| `raw/remits/service_date=.../` | remittance feed | curated builder |
| `curated/iceberg_style/claims_fact/service_date=.../` | lake job | Athena analysts |
| `athena-results/` | Athena service | analysts (read) |

Object names stay `part-000.*` so both Glue and local DuckDB stand-ins can glob predictably.
