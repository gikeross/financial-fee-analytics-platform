from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "assets" / "dashboard"

def euro(x, _=None):
    return f"€{x/1000:.0f}K" if abs(x) >= 1000 else f"€{x:,.0f}"

def main():
    clients = pd.read_csv(RAW / "clients.csv")
    tx = pd.read_csv(RAW / "transactions.csv", parse_dates=["transaction_date"])
    df = tx.merge(clients, on="client_id", how="left")
    df["month"] = df["transaction_date"].dt.to_period("M").astype(str)
    OUT.mkdir(parents=True, exist_ok=True)

    monthly = df.groupby("month", as_index=False).agg(
        gross_fees=("charged_fee", "sum"), expected_fees=("expected_fee", "sum"),
        reconciliation_rate=("is_reconciled", "mean"))
    product = df.groupby("product", as_index=False).agg(gross_fees=("charged_fee", "sum"))

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(monthly["month"], monthly["gross_fees"], marker="o", label="Gross Fees")
    ax.plot(monthly["month"], monthly["expected_fees"], marker="o", label="Expected Fees")
    ax.set_title("Executive Overview — Monthly Fee Revenue")
    ax.yaxis.set_major_formatter(FuncFormatter(euro)); ax.tick_params(axis="x", rotation=45); ax.legend(); fig.tight_layout()
    fig.savefig(OUT / "01-executive-overview.png", dpi=160); plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 6))
    p = product.sort_values("gross_fees")
    ax.barh(p["product"], p["gross_fees"]); ax.xaxis.set_major_formatter(FuncFormatter(euro))
    ax.set_title("Product Performance — Gross Fees by Product"); fig.tight_layout()
    fig.savefig(OUT / "02-product-performance.png", dpi=160); plt.close(fig)

    exc = df.loc[~df["is_reconciled"]].groupby("product", as_index=False).agg(exception_count=("transaction_id", "count")).sort_values("exception_count")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(exc["product"], exc["exception_count"]); ax.set_title("Fee Exceptions — Count by Product"); fig.tight_layout()
    fig.savefig(OUT / "03-fee-exceptions.png", dpi=160); plt.close(fig)

    print(f"Generated dashboard previews in {OUT}")

if __name__ == "__main__":
    main()
