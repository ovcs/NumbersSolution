import psycopg2

from project import logger
from psycopg2 import Error
from psycopg2.extras import execute_values


class DataBase:
    host: tuple
    queries: dict
    keys: tuple

    def __init__(self, cfg):
        self.host = cfg.queries
        self.queries = cfg.queries
        self.keys = cfg.keys

    def query(self, sql, type=None, value=None):
        connection = None
        cursor = None
        record = None
        try:
            connection = psycopg2.connect(user=self.host[0],
                                          password=self.host[1],
                                          host=self.host[2],
                                          port=self.host[3],
                                          database=self.host[4])
            cursor = connection.cursor()

            if value is None:
                cursor.execute(sql)
            elif len(value) == 1:
                cursor.execute(sql, value)
            else:
                execute_values(cursor, sql, value)

            if type == 'select':
                record = tuple([i[0] for i in cursor.fetchall()])
            elif type == 'count':
                record = cursor.rowcount

            connection.commit()

        except (Exception, Error) as e:
            logger.error(f"Error exception PostgreSQL: {e}")
        finally:
            if connection:
                cursor.close()
                connection.close()
            return record

    def connect(self):
        return self.query(self.queries['connect'], type='send') is not None

    def create_table_if_not_exist(self):
        self.query(self.queries['create_new_table_if_not_exist'])

    def insert(self, values):
        self.query(self.queries['insert'], type='send', value=values)

    def delete_row(self, id_rows):
        self.query(self.queries['delete'], type='send', value=(id_rows,))

    def update_column_currency(self, value):
        self.query(self.queries['update_currency'], type='send', value=(value,))

    def select(self, value):
        return tuple(self.query(self.queries['select'].format(value), type='select'))

    def add(self, changed_rows):
        self.insert(changed_rows)
