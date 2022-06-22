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
        self.time_update_sec = cfg.Main.TIME_UPDATE_SEC
        self.curr_datetime = cfg.Main.CURRENT_DATETIME
        self.document_id = cfg.Google.DOCUMENT_ID

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
