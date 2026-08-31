DROP VIEW IF EXISTS analytics.stg_clients CASCADE;
CREATE VIEW analytics.stg_clients AS
SELECT client_id, TRIM(client_segment) AS client_segment, TRIM(country) AS country, TRIM(risk_tier) AS risk_tier
FROM analytics.raw_clients;

DROP VIEW IF EXISTS analytics.stg_transactions CASCADE;
CREATE VIEW analytics.stg_transactions AS
SELECT transaction_id, transaction_date::date, client_id, TRIM(product) AS product, TRIM(channel) AS channel,
       transaction_amount::numeric(18,2), expected_fee::numeric(18,2), charged_fee::numeric(18,2),
       fee_leakage::numeric(18,2), is_reconciled::boolean, exception_priority
FROM analytics.raw_transactions;
