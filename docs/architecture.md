# Architecture

Synthetic data generator → raw CSV/PostgreSQL → staging views → enriched intermediate model → dimensional star schema → KPI marts → Power BI.

The design deliberately separates ingestion, transformation, modelling, quality validation, and presentation so the business logic can later migrate to dbt or Microsoft Fabric without changing the analytical definitions.
