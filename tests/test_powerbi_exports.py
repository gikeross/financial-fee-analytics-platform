from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
BI = ROOT / "data" / "powerbi"

def test_powerbi_tables_exist():
    expected = {"dim_date.csv","dim_client.csv","dim_country.csv","dim_product.csv","dim_channel.csv","fact_transactions.csv","fact_fee_exceptions.csv"}
    assert expected.issubset({p.name for p in BI.glob("*.csv")})

def test_fact_foreign_keys_are_complete():
    fact = pd.read_csv(BI / "fact_transactions.csv")
    for column in ["client_key","country_key","product_key","channel_key","date_key"]:
        assert fact[column].notna().all()

def test_exception_fact_is_subset():
    fact = pd.read_csv(BI / "fact_transactions.csv")
    exceptions = pd.read_csv(BI / "fact_fee_exceptions.csv")
    expected_ids = set(fact.loc[~fact["is_reconciled"], "transaction_id"])
    assert set(exceptions["transaction_id"]) == expected_ids
