# IAM — athena-hf-analyst

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ReadCuratedLake",
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:ListBucket"],
      "Resource": [
        "arn:aws:s3:::hf-open-lake-prod",
        "arn:aws:s3:::hf-open-lake-prod/curated/*",
        "arn:aws:s3:::hf-athena-results",
        "arn:aws:s3:::hf-athena-results/*"
      ]
    },
    {
      "Sid": "GlueCatalogRead",
      "Effect": "Allow",
      "Action": ["glue:GetDatabase", "glue:GetTable", "glue:GetPartitions", "glue:GetPartition"],
      "Resource": [
        "arn:aws:glue:*:*:catalog",
        "arn:aws:glue:*:*:database/hf_curated",
        "arn:aws:glue:*:*:table/hf_curated/*"
      ]
    },
    {
      "Sid": "AthenaRun",
      "Effect": "Allow",
      "Action": ["athena:StartQueryExecution", "athena:GetQueryExecution", "athena:GetQueryResults"],
      "Resource": "*"
    }
  ]
}
```

Deny (or simply omit) write actions on `raw/` so a compromised analyst session cannot poison source drops.
