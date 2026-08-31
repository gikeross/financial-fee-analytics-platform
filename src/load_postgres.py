from pathlib import Path
import os
import pandas as pd
from sqlalchemy import create_engine, URL

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"

def main():
    clients = pd.read_csv(RAW / "clients.csv")
    tx = pd.read_csv(RAW / "transactions.csv")
    url = URL.create(
        "postgresql+psycopg",
        username=os.getenv("POSTGRES_USER", "analytics"),
        password=os.getenv("POSTGRES_PASSWORD", "analytics"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", "5432")),
        database=os.getenv("POSTGRES_DB", "fee_analytics"),
    )
    engine = create_engine(url, pool_pre_ping=True)
    with engine.begin() as conn:
        conn.exec_driver_sql("CREATE SCHEMA IF NOT EXISTS analytics")
        clients.to_sql("raw_clients", conn, schema="analytics", if_exists="replace", index=False)
        tx.to_sql("raw_transactions", conn, schema="analytics", if_exists="replace", index=False)
    print(f"Loaded {len(clients):,} clients and {len(tx):,} transactions.")

if __name__ == "__main__":
    main()
