DROP VIEW IF EXISTS analytics.int_transactions_enriched CASCADE;
CREATE VIEW analytics.int_transactions_enriched AS
SELECT t.*, c.client_segment, c.country, c.risk_tier,
       DATE_TRUNC('month', t.transaction_date)::date AS month_start,
       CASE WHEN t.expected_fee = 0 THEN 0 ELSE t.fee_leakage / t.expected_fee END AS leakage_rate
FROM analytics.stg_transactions t
JOIN analytics.stg_clients c USING (client_id);
