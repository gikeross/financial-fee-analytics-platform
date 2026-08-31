from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "powerbi"

def main():
    clients = pd.read_csv(RAW / "clients.csv")
    tx = pd.read_csv(RAW / "transactions.csv", parse_dates=["transaction_date"])
    OUT.mkdir(parents=True, exist_ok=True)

    dim_date = pd.DataFrame({"date_key": pd.date_range(tx["transaction_date"].min(), tx["transaction_date"].max(), freq="D")})
    dim_date["year"] = dim_date["date_key"].dt.year
    dim_date["quarter"] = "Q" + dim_date["date_key"].dt.quarter.astype(str)
    dim_date["month_number"] = dim_date["date_key"].dt.month
    dim_date["month_name"] = dim_date["date_key"].dt.strftime("%b")
    dim_date["year_month"] = dim_date["date_key"].dt.strftime("%Y-%m")
    dim_date["month_start"] = dim_date["date_key"].values.astype("datetime64[M]")
    dim_date.to_csv(OUT / "dim_date.csv", index=False)

    dim_client = clients[["client_id", "client_segment", "risk_tier"]].drop_duplicates().copy()
    dim_client.insert(0, "client_key", np.arange(1, len(dim_client) + 1))
    dim_client.to_csv(OUT / "dim_client.csv", index=False)

    dim_country = clients[["country"]].drop_duplicates().sort_values("country").reset_index(drop=True)
    dim_country.insert(0, "country_key", np.arange(1, len(dim_country) + 1))
    dim_country.to_csv(OUT / "dim_country.csv", index=False)

    dim_product = tx[["product"]].drop_duplicates().sort_values("product").reset_index(drop=True)
    dim_product.insert(0, "product_key", np.arange(1, len(dim_product) + 1))
    dim_product.to_csv(OUT / "dim_product.csv", index=False)

    dim_channel = tx[["channel"]].drop_duplicates().sort_values("channel").reset_index(drop=True)
    dim_channel.insert(0, "channel_key", np.arange(1, len(dim_channel) + 1))
    dim_channel.to_csv(OUT / "dim_channel.csv", index=False)

    fact = tx.copy()
    fact["date_key"] = fact["transaction_date"].dt.date.astype(str)
    fact = fact.merge(dim_client[["client_key", "client_id"]], on="client_id", how="left")
    fact = fact.merge(clients[["client_id", "country"]], on="client_id", how="left")
    fact = fact.merge(dim_country, on="country", how="left")
    fact = fact.merge(dim_product, on="product", how="left")
    fact = fact.merge(dim_channel, on="channel", how="left")

    fact_transactions = fact[[
        "transaction_id", "date_key", "client_key", "country_key", "product_key", "channel_key",
        "transaction_amount", "expected_fee", "charged_fee", "fee_leakage",
        "is_reconciled", "exception_priority"
    ]].copy()
    fact_transactions.to_csv(OUT / "fact_transactions.csv", index=False)
    fact_transactions.loc[~fact_transactions["is_reconciled"]].to_csv(OUT / "fact_fee_exceptions.csv", index=False)

    print(f"Exported {len(fact_transactions):,} Power BI fact rows to {OUT}")

if __name__ == "__main__":
    main()
