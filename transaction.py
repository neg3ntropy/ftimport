from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class Transaction:
    datetime: datetime
    isin: str
    quantity: int
    price: Decimal
