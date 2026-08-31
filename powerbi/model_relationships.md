# Power BI Model Relationships

Use a single-direction star schema:

| Dimension | Key | Fact | Key | Cardinality |
| --- | --- | --- | --- | --- |
| dim_date | date_key | fact_transactions | date_key | 1:* |
| dim_client | client_key | fact_transactions | client_key | 1:* |
| dim_country | country_key | fact_transactions | country_key | 1:* |
| dim_product | product_key | fact_transactions | product_key | 1:* |
| dim_channel | channel_key | fact_transactions | channel_key | 1:* |

Mark `dim_date` as the date table, sort month names by month number, hide surrogate keys from report view, and keep cross-filter direction single unless a specific visual requires otherwise.
