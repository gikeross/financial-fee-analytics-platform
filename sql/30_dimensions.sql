DROP TABLE IF EXISTS analytics.dim_date CASCADE;
CREATE TABLE analytics.dim_date AS
SELECT DISTINCT transaction_date AS date_key,
       EXTRACT(YEAR FROM transaction_date)::int AS year,
       EXTRACT(MONTH FROM transaction_date)::int AS month,
       TO_CHAR(transaction_date, 'Mon') AS month_name,
       DATE_TRUNC('month', transaction_date)::date AS month_start
FROM analytics.stg_transactions;
ALTER TABLE analytics.dim_date ADD PRIMARY KEY (date_key);

DROP TABLE IF EXISTS analytics.dim_client CASCADE;
CREATE TABLE analytics.dim_client AS
SELECT ROW_NUMBER() OVER (ORDER BY client_id)::int AS client_key,
       client_id, client_segment, risk_tier
FROM analytics.stg_clients;
ALTER TABLE analytics.dim_client ADD PRIMARY KEY (client_key);
CREATE UNIQUE INDEX ON analytics.dim_client (client_id);

DROP TABLE IF EXISTS analytics.dim_country CASCADE;
CREATE TABLE analytics.dim_country AS
SELECT ROW_NUMBER() OVER (ORDER BY country)::int AS country_key, country
FROM (SELECT DISTINCT country FROM analytics.stg_clients) x;
ALTER TABLE analytics.dim_country ADD PRIMARY KEY (country_key);

DROP TABLE IF EXISTS analytics.dim_product CASCADE;
CREATE TABLE analytics.dim_product AS
SELECT ROW_NUMBER() OVER (ORDER BY product)::int AS product_key, product
FROM (SELECT DISTINCT product FROM analytics.stg_transactions) x;
ALTER TABLE analytics.dim_product ADD PRIMARY KEY (product_key);

DROP TABLE IF EXISTS analytics.dim_channel CASCADE;
CREATE TABLE analytics.dim_channel AS
SELECT ROW_NUMBER() OVER (ORDER BY channel)::int AS channel_key, channel
FROM (SELECT DISTINCT channel FROM analytics.stg_transactions) x;
ALTER TABLE analytics.dim_channel ADD PRIMARY KEY (channel_key);
