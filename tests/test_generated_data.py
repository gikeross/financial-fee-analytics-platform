from src.generate_data import generate_transactions

def test_unique():
    _, tx = generate_transactions(2000, 7)
    assert tx.transaction_id.is_unique

def test_refs():
    clients, tx = generate_transactions(2000, 7)
    assert set(tx.client_id).issubset(set(clients.client_id))

def test_non_negative():
    _, tx = generate_transactions(2000, 7)
    assert (tx[["transaction_amount","expected_fee","charged_fee","fee_leakage"]] >= 0).all().all()

def test_exceptions():
    _, tx = generate_transactions(5000, 7)
    assert (~tx.is_reconciled).any()
