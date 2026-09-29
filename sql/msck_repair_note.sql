-- After new service_date prefixes land under the S3 location:
MSCK REPAIR TABLE hf_raw.claims;
MSCK REPAIR TABLE hf_curated.claims_fact;

-- Prefer partition projection / Glue crawler in production; MSCK is the interview fallback.
