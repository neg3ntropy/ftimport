import csv
from datetime import datetime
from decimal import Decimal

from transaction import Transaction


def _load_transactions(filename: str):
    with open(filename, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        next(csvreader, None)
        for row in csvreader:
            [
                date,
                time,
                _name,
                isin,
                _exchange,
                quantity,
                _currency,
                price,
                _currency,
                _value,
                _home_currency,
                _home_value,
                _rate,
                _home_currency,
                _fee,
                _home_currency,
                _total_value,
                _order_id
            ] = row
            transaction = Transaction(
                datetime=datetime.strptime(f'{date}T{time}', '%d-%m-%YT%H:%M'), # TODO internationalization
                isin=isin,
                quantity=int(quantity),
                price=Decimal(price)
            )
            yield transaction

def load_transactions(filename: str):
    return reversed(list(_load_transactions(filename)))
