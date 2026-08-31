-- Each query should return zero rows.

SELECT transaction_id, COUNT(*)
FROM analytics.fact_transactions
GROUP BY transaction_id
HAVING COUNT(*) > 1;

SELECT *
FROM analytics.fact_transactions
WHERE transaction_amount < 0
   OR expected_fee < 0
   OR charged_fee < 0
   OR fee_leakage < 0;

SELECT *
FROM analytics.fact_transactions
WHERE ABS(fee_leakage - GREATEST(expected_fee - charged_fee, 0)) > 0.01;

SELECT *
FROM analytics.fact_transactions
WHERE client_key IS NULL
   OR country_key IS NULL
   OR product_key IS NULL
   OR channel_key IS NULL
   OR date_key IS NULL;
