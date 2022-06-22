class DataBase:
    host: tuple
    queries: dict
    keys: tuple

    def __init__(self, cfg):
        self.host = cfg.queries
        self.queries = cfg.queries
        self.keys = cfg.keys
