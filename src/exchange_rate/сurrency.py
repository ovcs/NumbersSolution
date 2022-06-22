from datetime import date, time
from decimal import Decimal


class CurrencyExchange:
    exchange_date: date
    exchange_time: time
    currency_id: str
    url: str
    value: Decimal

    def __init__(self, cfg):
        self.currency_id = cfg.currency_id
        self.url = cfg.url
        self.exchange_date = cfg.exchange_date
        self.exchange_time = cfg.exchange_time
        self.value = Decimal('1')
