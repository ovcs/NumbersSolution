import os
from datetime import datetime, date, timedelta, time


class SetUp:
    class Main:
        TIME_UPDATE_SEC = 30
        CURRENT_DATETIME = datetime.now()

    class Google:
        CREDENTIALS_SECRET_FILE_PATH = os.path.abspath(r'config/client_secret.json')
        CREDENTIALS_USER_PATH = os.path.abspath(r'config/token.json')
        CREDENTIALS_SERVICE_PATH = os.path.abspath(r'config/credentials.json')
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        DOCUMENT_ID = '1ll20AkAfvxnWuPPaAWw1d0iZncQZYtch33LQZtgfeGU'

    class CurrExc:
        currency_id = 'R01235'
        url = "http://www.cbr.ru/scripts/XML_daily.asp"
        exchange_time = time(11, 30)
        exchange_date = date.today() - timedelta(days=2)

    class DataBase:
        user = ""
        password = ""
        host = "127.0.0.1"
        port = "5432"
        database_name = ""
        host = (user, password, host, port, database_name)
        queries = {
            "connect": "SELECT version();",
            "select": "SELECT {0} FROM order_list;",

            "create_new_table_if_not_exist": """CREATE TABLE IF NOT EXISTS order_list   
            (order_id                  integer       NOT NULL,
            order_list_id       text                  NOT NULL,
            price_usd           numeric(10,2)                   NOT NULL,
            price_rub           numeric(10,2)                   NOT NULL,
            order_delivery_date date               NOT NULL);""",

            "insert": """ INSERT INTO order_list (order_id, order_list_id, price_usd, price_rub, order_delivery_date)
                                                         VALUES %s;""",
            "delete": "DELETE from order_list WHERE order_id = %s;",
            "update_currency": "UPDATE order_list SET price_rub=price_usd*%s::DECIMAL(10,2);"
        }

    class TeleBot:
        token = ""

# file_handler = logging.FileHandler('logs.log')
# file_handler.setLevel(logging.DEBUG)
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)
