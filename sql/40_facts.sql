DROP TABLE IF EXISTS analytics.fact_transactions CASCADE;
CREATE TABLE analytics.fact_transactions AS
SELECT t.transaction_id,
       t.transaction_date AS date_key,
       dc.client_key,
       dco.country_key,
       dp.product_key,
       dch.channel_key,
       t.transaction_amount,
       t.expected_fee,
       t.charged_fee,
       t.fee_leakage,
       t.is_reconciled,
       t.exception_priority
FROM analytics.int_transactions_enriched t
JOIN analytics.dim_client dc ON t.client_id = dc.client_id
JOIN analytics.dim_country dco ON t.country = dco.country
JOIN analytics.dim_product dp ON t.product = dp.product
JOIN analytics.dim_channel dch ON t.channel = dch.channel;
ALTER TABLE analytics.fact_transactions ADD PRIMARY KEY (transaction_id);

DROP TABLE IF EXISTS analytics.fact_fee_exceptions CASCADE;
CREATE TABLE analytics.fact_fee_exceptions AS
SELECT * FROM analytics.fact_transactions WHERE NOT is_reconciled;
