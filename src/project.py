import time
import logging
import sys

from database_ctrl.database import DataBase
from exchange_rate.сurrency import CurrencyExchange
from google_doc_loader.google_api import GoogleAPI
from google_doc_loader.g_sheets import GSheets
from datetime import datetime, date
from decimal import Decimal


class Project:
    def __init__(self, cfg):
        self.time_update_sec: int = cfg.Main.TIME_UPDATE_SEC
        self.curr_datetime: datetime = cfg.Main.CURRENT_DATETIME
        self.document_id: str = cfg.Google.DOCUMENT_ID

        self.gAPI = GoogleAPI(cfg.Google)
        self.currency = CurrencyExchange(cfg.CurrExc)
        self.db = DataBase(cfg.DataBase)
        # self.tb = TeleBot(cfg.TeleBot)

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.setFormatter(formatter)

        self.logger.addHandler(stdout_handler)

    def check_connect(self):
        try:
            self.gAPI.authorize_from('service_account')
            self.currency.have_update(self.curr_datetime)
            self.db.connect()
            # self.tb.connect()
            self.logger.info("Connection Success")
        except Exception:
            self.logger.info(f"Connection Fault. {Exception.args}")
            exit()

    def start(self):
        self.db.create_table_if_not_exist()
        self.db.load_current_keys()
        # If new table, take start index
        if self.db.keys == ():
            self.db.keys = (2,)
        else:
            self.db.update_column_currency(self.currency.value)
        self.gsheet = GSheets(self.gAPI.service, spreadsheet_id=self.document_id)

    def main(self):
        if self.curr_datetime.date() != datetime.now().date():
            self.curr_datetime = datetime.now()
            if self.currency.have_update(self.curr_datetime):
                self.db.update_column_currency(self.currency.value)
            # проверяем контрагентов на просрочку
            ## загружаем с бд данные с датами
            ## if delivery_date > now: # отправляем запрос телеграм боту
        gkeys = tuple(int(i) for i in self.gsheet.load_values(range='A:A',
                                                              major_dimension='COLUMNS',
                                                              start_with=1))
        if self.db.keys != gkeys:
            deleted_rows = self.db.check_update(gkeys)
            g_table = self.__create_gvalue_list(self.db.keys)
            self.db.add(g_table)
            self.db.delete(deleted_rows)
            self.db.keys = gkeys

    def __create_gvalue_list(self, last_row):
        gval = []
        gs_rows = self.gsheet.load_values(range=f'A{last_row[0][-1]}:D')
        for row in gs_rows:
            price = Decimal(row[2])
            delivery_date = datetime.strptime(row[3], "%d.%m.%Y").date()
            gval.append((int(row[0]), row[1], price, price * self.currency.value, delivery_date))
        return gval

