# Financial Fee Analytics Platform

End-to-end financial analytics engineering portfolio project using **synthetic data only**.

## What it demonstrates
Python data generation, PostgreSQL ingestion, layered SQL transformations, dimensional modelling, KPI marts, automated data-quality tests, CI and BI-ready outputs.

## Business questions
- What fee revenue was expected versus charged?
- Where is revenue leakage concentrated?
- Which products and segments drive revenue?
- What is the reconciliation rate?
- Which fee exceptions require investigation?

## Reproduce
```bash
pip install -r requirements.txt
python src/generate_data.py --rows 100000 --seed 42
python src/generate_outputs.py
python src/export_powerbi.py
python src/generate_dashboard.py
pytest -q
```

## Architecture
Synthetic generator → raw CSV/PostgreSQL → staging → intermediate → star schema → marts → Power BI.

## Core model
Dimensions: `dim_date`, `dim_client`, `dim_country`, `dim_product`, `dim_channel`.
Facts: `fact_transactions`, `fact_fee_exceptions`.
Marts: monthly KPIs and product performance.

## Outputs
`outputs/executive_summary.csv`, `monthly_fee_kpis.csv`, `product_performance.csv`, `segment_performance.csv`, `top_fee_exceptions.csv`.

Charts are generated in `assets/`.

## Next phase
Build a Power BI semantic model and three report pages: Executive Overview, Product Performance, Fee Exceptions.

## Power BI Layer

The project generates a BI-ready star-schema export under `data/powerbi/` with `python src/export_powerbi.py`, a reusable DAX measure library, model relationship instructions, a theme, and a complete three-page dashboard specification.

See [`powerbi/README.md`](powerbi/README.md).

### BI-ready tables

```text
data/powerbi/
├── dim_date.csv
├── dim_client.csv
├── dim_country.csv
├── dim_product.csv
├── dim_channel.csv
├── fact_transactions.csv
└── fact_fee_exceptions.csv
```

The generated Power BI CSVs are intentionally excluded from Git and recreated locally with `python src/export_powerbi.py`, keeping the repository lightweight and reproducible.

## Dashboard Preview

The project generates three dashboard preview pages from the deterministic 100,000-transaction dataset with `python src/generate_dashboard.py`. Generated PNGs are intentionally excluded from Git and can be recreated locally.

### Generated pages

- Executive Overview
- Product Performance
- Fee Exceptions

These previews use the same KPI definitions and star-schema fields documented in the Power BI layer. The final `.pbix` should reproduce this business structure while using native Power BI interactions, slicers, drill-through and DAX.
