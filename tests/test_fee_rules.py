import pytest
from src.fee_rules import expected_fee, fee_leakage, reconciled

def test_wire_fee(): assert expected_fee("Wire Transfer",10)==1.52
def test_cap(): assert expected_fee("Securities",1_000_000)==300.0
def test_leakage(): assert fee_leakage(10,8.5)==1.5
def test_no_negative_leakage(): assert fee_leakage(10,12)==0
def test_reconciled(): assert reconciled(10,9.97)
def test_unknown():
    with pytest.raises(ValueError): expected_fee("Unknown",100)
