import uuid
from decimal import Decimal


def generate_order_number():
    return f'GC-{uuid.uuid4().hex[:12].upper()}'


def calculate_tax(subtotal: Decimal, tax_rate: float) -> Decimal:
    return (subtotal * Decimal(str(tax_rate / 100))).quantize(Decimal('0.01'))


def apply_percentage_discount(amount: Decimal, percentage: Decimal) -> Decimal:
    return (amount * percentage / Decimal('100')).quantize(Decimal('0.01'))
