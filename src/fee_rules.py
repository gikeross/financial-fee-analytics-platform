from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

@dataclass(frozen=True)
class FeeRule:
    fixed_fee: float
    variable_rate: float
    minimum_fee: float
    maximum_fee: float

RULES = {
    "Card Payments": FeeRule(0.20, 0.0040, 0.20, 45.00),
    "Wire Transfer": FeeRule(1.50, 0.0015, 1.50, 75.00),
    "FX Conversion": FeeRule(0.00, 0.0035, 0.50, 250.00),
    "Securities": FeeRule(2.00, 0.0020, 2.00, 300.00),
    "Custody": FeeRule(0.50, 0.0008, 0.50, 150.00),
}

def money(value) -> float:
    return float(Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

def expected_fee(product, amount):
    if product not in RULES:
        raise ValueError(f"Unknown product: {product}")
    if amount < 0:
        raise ValueError("amount must be non-negative")
    r = RULES[product]
    raw = Decimal(str(r.fixed_fee)) + Decimal(str(amount)) * Decimal(str(r.variable_rate))
    bounded = max(Decimal(str(r.minimum_fee)), min(raw, Decimal(str(r.maximum_fee))))
    return money(bounded)

def fee_leakage(expected, charged):
    return money(max(Decimal(str(expected)) - Decimal(str(charged)), Decimal("0")))

def reconciled(expected, charged, tolerance=0.05):
    return abs(Decimal(str(expected)) - Decimal(str(charged))) <= Decimal(str(tolerance))
