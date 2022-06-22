import requests
import bs4
import logging

from datetime import date, time,  timedelta, datetime
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
        self.logger = logging.getLogger(__name__)

    def send_request(self):
        response = requests.get(self.url, headers={'Connection': 'close'})
        if response.status_code == 200:
            return response
        else:
            raise Exception(f'Error currency update, http status code {response.status_code}')

    def parse_value_from_xml(self):
        try:
            resp = self.send_request()
            soup = bs4.BeautifulSoup(resp.text, 'xml')
            self.value = Decimal(
                soup.find(ID=self.currency_id)
                    .find('Value')
                    .get_text()
                    .replace(',', '.')).quantize(Decimal("1.00"))
        except Exception:
            self.logger.error(f'Error currency update, error parce currency value {Exception.args}')

    def have_update(self, now: datetime):
        if datetime.combine((self.exchange_date + timedelta(days=1)), self.exchange_time) < now:
            self.parse_value_from_xml()
            self.exchange_date = now.date()
