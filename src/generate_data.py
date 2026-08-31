import argparse
from pathlib import Path
import numpy as np
import pandas as pd
try:
    from src.fee_rules import RULES, expected_fee, fee_leakage, reconciled
except ModuleNotFoundError:
    from fee_rules import RULES, expected_fee, fee_leakage, reconciled

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PRODUCTS = list(RULES)
COUNTRIES = ["Portugal","France","Italy","Spain","Germany","Belgium"]
CHANNELS = ["Online","Branch","API","Mobile","Operations"]
SEGMENTS = ["Retail","SME","Corporate","Institutional"]

def generate_clients(rng, n_clients=500):
    return pd.DataFrame({
        "client_id": [f"C{i:05d}" for i in range(1,n_clients+1)],
        "client_segment": rng.choice(SEGMENTS,n_clients,p=[.45,.25,.22,.08]),
        "country": rng.choice(COUNTRIES,n_clients),
        "risk_tier": rng.choice(["Low","Medium","High"],n_clients,p=[.55,.35,.10]),
    })

def generate_transactions(rows=100000, seed=42):
    rng = np.random.default_rng(seed)
    clients = generate_clients(rng)
    products = rng.choice(PRODUCTS,rows,p=[.35,.20,.16,.17,.12])
    amounts = np.round(rng.lognormal(7.5,1.2,rows),2)
    expected = np.array([expected_fee(p,a) for p,a in zip(products,amounts)])
    variance = np.zeros(rows)
    mask = rng.random(rows) < .085
    variance[mask] = rng.normal(-.18,.45,mask.sum())
    charged = np.maximum(np.round(expected+variance,2),0)
    tx = pd.DataFrame({
        "transaction_id":[f"T{i:09d}" for i in range(1,rows+1)],
        "transaction_date": pd.to_datetime("2025-01-01") + pd.to_timedelta(rng.integers(0,365,rows),unit="D"),
        "client_id": rng.choice(clients["client_id"],rows),
        "product": products,
        "channel": rng.choice(CHANNELS,rows,p=[.30,.13,.17,.25,.15]),
        "transaction_amount": amounts,
        "expected_fee": expected,
        "charged_fee": charged,
    })
    tx["fee_leakage"]=[fee_leakage(e,c) for e,c in zip(tx.expected_fee,tx.charged_fee)]
    tx["is_reconciled"]=[reconciled(e,c) for e,c in zip(tx.expected_fee,tx.charged_fee)]
    tx["exception_priority"]=np.select(
        [(~tx.is_reconciled)&(tx.fee_leakage>=5),(~tx.is_reconciled)&(tx.fee_leakage>=1),(~tx.is_reconciled)],
        ["High","Medium","Low"], default="None"
    )
    return clients, tx

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--rows",type=int,default=100000)
    ap.add_argument("--seed",type=int,default=42)
    a=ap.parse_args()
    RAW_DIR.mkdir(parents=True,exist_ok=True)
    clients,tx=generate_transactions(a.rows,a.seed)
    clients.to_csv(RAW_DIR/"clients.csv",index=False)
    tx.to_csv(RAW_DIR/"transactions.csv",index=False)
    print(f"transactions={len(tx):,}")
    print(f"gross_fees={tx.charged_fee.sum():,.2f}")
    print(f"expected_fees={tx.expected_fee.sum():,.2f}")
    print(f"fee_leakage={tx.fee_leakage.sum():,.2f}")
    print(f"reconciliation_rate={tx.is_reconciled.mean():.2%}")

if __name__=="__main__":
    main()
