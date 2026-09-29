-- Athena / Glue DDL (paths map to lake/ locally)
CREATE DATABASE IF NOT EXISTS hf_raw;
CREATE DATABASE IF NOT EXISTS hf_curated;

CREATE EXTERNAL TABLE hf_raw.claims (
  claim_line_id  string,
  payer          string,
  allowed_amount double,
  member_token   string
)
PARTITIONED BY (service_date date)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 's3://hf-open-lake-prod/raw/claims/'
TBLPROPERTIES ('skip.header.line.count'='1');

CREATE EXTERNAL TABLE hf_curated.claims_fact (
  claim_line_id  string,
  payer          string,
  allowed_amount double,
  paid_amount    double,
  member_token   string
)
PARTITIONED BY (service_date date)
STORED AS PARQUET
LOCATION 's3://hf-open-lake-prod/curated/iceberg_style/claims_fact/';
