-- Partition prune: only service_date in [2025-08-01, 2025-08-03]
SELECT
    payer,
    COUNT(*) AS claim_lines,
    ROUND(SUM(allowed_amount), 2) AS allowed_amount,
    ROUND(SUM(paid_amount), 2) AS paid_amount
FROM hf_curated.claims_fact
WHERE service_date BETWEEN DATE '2025-08-01' AND DATE '2025-08-03'
GROUP BY payer
ORDER BY paid_amount DESC;
