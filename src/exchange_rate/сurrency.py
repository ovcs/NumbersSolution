import requests

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

    def send_request(self):
        response = requests.get(self.url, headers={'Connection': 'close'})
        if response.status_code == 200:
            return response
        else:
            raise Exception(f'Error currency update, http status code {response.status_code}')
