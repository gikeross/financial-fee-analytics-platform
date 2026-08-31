# Power BI DAX Measures

Create these measures in a dedicated `_Measures` table.

```DAX
Gross Fees = SUM ( fact_transactions[charged_fee] )
Expected Fees = SUM ( fact_transactions[expected_fee] )
Fee Leakage = SUM ( fact_transactions[fee_leakage] )
Leakage % = DIVIDE ( [Fee Leakage], [Expected Fees], 0 )
Transaction Count = DISTINCTCOUNT ( fact_transactions[transaction_id] )
Reconciled Transactions = CALCULATE ( [Transaction Count], fact_transactions[is_reconciled] = TRUE () )
Exception Count = CALCULATE ( [Transaction Count], fact_transactions[is_reconciled] = FALSE () )
Reconciliation Rate = DIVIDE ( [Reconciled Transactions], [Transaction Count], 0 )
Average Fee / Transaction = DIVIDE ( [Gross Fees], [Transaction Count], 0 )
Gross Fees Previous Month = CALCULATE ( [Gross Fees], DATEADD ( dim_date[date_key], -1, MONTH ) )
MoM Revenue Change = DIVIDE ( [Gross Fees] - [Gross Fees Previous Month], [Gross Fees Previous Month], 0 )
High-Risk Exceptions = CALCULATE ( [Transaction Count], fact_transactions[exception_priority] = "High" )
Revenue at Risk = CALCULATE ( [Fee Leakage], fact_transactions[exception_priority] IN { "High", "Medium" } )
```

Recommended formatting: currency measures `€#,##0.00`, percentages `0.00%`, counts `#,##0`.
