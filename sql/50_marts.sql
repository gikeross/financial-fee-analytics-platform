DROP VIEW IF EXISTS analytics.mart_monthly_fee_kpis CASCADE;
CREATE VIEW analytics.mart_monthly_fee_kpis AS
SELECT d.month_start,
       COUNT(*) AS transaction_count,
       SUM(f.charged_fee) AS gross_fees,
       SUM(f.expected_fee) AS expected_fees,
       SUM(f.fee_leakage) AS fee_leakage,
       SUM(f.fee_leakage) / NULLIF(SUM(f.expected_fee), 0) AS leakage_pct,
       AVG(CASE WHEN f.is_reconciled THEN 1.0 ELSE 0.0 END) AS reconciliation_rate,
       COUNT(*) FILTER (WHERE NOT f.is_reconciled) AS exception_count
FROM analytics.fact_transactions f
JOIN analytics.dim_date d USING (date_key)
GROUP BY d.month_start;

DROP VIEW IF EXISTS analytics.mart_product_performance CASCADE;
CREATE VIEW analytics.mart_product_performance AS
SELECT p.product,
       COUNT(*) AS transaction_count,
       SUM(f.transaction_amount) AS transaction_value,
       SUM(f.charged_fee) AS gross_fees,
       SUM(f.expected_fee) AS expected_fees,
       SUM(f.fee_leakage) AS fee_leakage,
       AVG(CASE WHEN f.is_reconciled THEN 1.0 ELSE 0.0 END) AS reconciliation_rate
FROM analytics.fact_transactions f
JOIN analytics.dim_product p USING (product_key)
GROUP BY p.product;
