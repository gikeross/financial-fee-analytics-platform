from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/"data"/"raw"; OUT=ROOT/"outputs"; ASSETS=ROOT/"assets"

def main():
    clients=pd.read_csv(RAW/"clients.csv")
    tx=pd.read_csv(RAW/"transactions.csv",parse_dates=["transaction_date"])
    df=tx.merge(clients,on="client_id",how="left")
    df["month_start"]=df.transaction_date.dt.to_period("M").dt.to_timestamp()
    OUT.mkdir(exist_ok=True); ASSETS.mkdir(exist_ok=True)

    monthly=df.groupby("month_start",as_index=False).agg(
        transaction_count=("transaction_id","count"),
        gross_fees=("charged_fee","sum"),
        expected_fees=("expected_fee","sum"),
        fee_leakage=("fee_leakage","sum"),
        reconciliation_rate=("is_reconciled","mean"),
        exception_count=("is_reconciled",lambda s:(~s).sum())
    )
    monthly["leakage_pct"]=monthly.fee_leakage/monthly.expected_fees
    monthly["mom_revenue_change"]=monthly.gross_fees.pct_change()
    monthly.to_csv(OUT/"monthly_fee_kpis.csv",index=False)

    product=df.groupby("product",as_index=False).agg(
        transaction_count=("transaction_id","count"),
        transaction_value=("transaction_amount","sum"),
        gross_fees=("charged_fee","sum"),
        expected_fees=("expected_fee","sum"),
        fee_leakage=("fee_leakage","sum"),
        reconciliation_rate=("is_reconciled","mean")
    ).sort_values("gross_fees",ascending=False)
    product["leakage_pct"]=product.fee_leakage/product.expected_fees
    product.to_csv(OUT/"product_performance.csv",index=False)

    seg=df.groupby("client_segment",as_index=False).agg(
        transaction_count=("transaction_id","count"),
        gross_fees=("charged_fee","sum"),
        fee_leakage=("fee_leakage","sum"),
        reconciliation_rate=("is_reconciled","mean")
    ).sort_values("gross_fees",ascending=False)
    seg.to_csv(OUT/"segment_performance.csv",index=False)

    df.loc[~df.is_reconciled].sort_values("fee_leakage",ascending=False).head(100).to_csv(
        OUT/"top_fee_exceptions.csv",index=False
    )

    summary=pd.DataFrame({
        "metric":["transactions","gross_fees","expected_fees","fee_leakage","leakage_pct","reconciliation_rate","exception_count"],
        "value":[len(df),df.charged_fee.sum(),df.expected_fee.sum(),df.fee_leakage.sum(),
                 df.fee_leakage.sum()/df.expected_fee.sum(),df.is_reconciled.mean(),(~df.is_reconciled).sum()]
    })
    summary.to_csv(OUT/"executive_summary.csv",index=False)

    fig,ax=plt.subplots(figsize=(9,5))
    ax.plot(monthly.month_start,monthly.gross_fees,marker="o",label="Gross fees")
    ax.plot(monthly.month_start,monthly.expected_fees,marker="o",label="Expected fees")
    ax.set_title("Monthly fee revenue: charged vs expected"); ax.set_ylabel("Fee revenue"); ax.legend()
    fig.autofmt_xdate(); fig.tight_layout()
    fig.savefig(ASSETS/"monthly-fee-revenue.png",dpi=160); plt.close(fig)

    fig,ax=plt.subplots(figsize=(8,5))
    ax.bar(product["product"], product["fee_leakage"])
    ax.set_title("Fee leakage by product"); ax.set_ylabel("Fee leakage")
    ax.tick_params(axis="x",rotation=25); fig.tight_layout()
    fig.savefig(ASSETS/"fee-leakage-by-product.png",dpi=160); plt.close(fig)

    print(summary.to_string(index=False))

if __name__=="__main__":
    main()
