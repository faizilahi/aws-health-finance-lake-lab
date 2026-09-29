-- Worked join used to build curated claims_fact (Athena dialect)
SELECT
    c.claim_line_id,
    c.payer,
    c.allowed_amount,
    c.member_token,
    r.paid_amount,
    r.remit_id,
    c.service_date
FROM hf_raw.claims c
INNER JOIN hf_raw.remits r
    ON c.claim_line_id = r.claim_line_id
   AND c.service_date = r.service_date
WHERE c.service_date BETWEEN DATE '2025-08-01' AND DATE '2025-08-03';
