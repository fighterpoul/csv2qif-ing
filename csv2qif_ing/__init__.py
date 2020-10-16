import csv
from csv2qif.core import Transaction
import datetime

__mapping = {
    'date': 0,
    'price': 8,
    'recipient': 2,
    'desc': 3,
}


class dialect(csv.Dialect):
    delimiter = ';'
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = csv.QUOTE_MINIMAL


def row_converter(csv_row) -> Transaction:
    return Transaction(
        date=__get_date(csv_row),
        price=__get_price(csv_row),
        recipient=csv_row[__mapping['recipient']],
        desc=csv_row[__mapping['desc']]
    )


def row_filter(csv_row) -> bool:
    try:
        __get_price(csv_row)
        __get_date(csv_row)
    except (IndexError, ValueError):
        return False
    else:
        return True


def __get_price(csv_row):
    price = str(csv_row[__mapping['price']])
    if not price:
        blocked_index = 10
        price = str(csv_row[blocked_index])
    return float(price.replace(',', '.'))


def __get_date(csv_row) -> datetime.datetime:
    return datetime.datetime.strptime(csv_row[__mapping['date']], '%Y-%m-%d')

