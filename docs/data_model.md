# Data Model

`fact_transactions` has one row per transaction.

Dimensions:
- `dim_date`
- `dim_client`
- `dim_country`
- `dim_product`
- `dim_channel`

`fact_fee_exceptions` contains non-reconciled transactions for investigation workflows.

The model is designed as a clean star schema for BI consumption, with business-facing measures kept separate from raw ingestion fields.
