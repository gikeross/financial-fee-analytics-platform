# Power BI Layer

Generate the BI-ready CSV star schema with:

```bash
python src/generate_data.py --rows 100000 --seed 42
python src/export_powerbi.py
```

Then import the files from `data/powerbi/` into Power BI Desktop, create the relationships in `model_relationships.md`, add the measures from `dax_measures.md`, and build the three report pages described in `dashboard_build_guide.md`.

The CSV path makes the project easy to reproduce without a live database. A production-style implementation can instead connect Power BI directly to the PostgreSQL marts.
