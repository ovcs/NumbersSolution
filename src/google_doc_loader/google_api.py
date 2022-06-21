class GoogleAPI:
    service = None

    def __init__(self, cfg):
        self.CREDENTIALS_SERVICE_PATH = cfg.CREDENTIALS_SERVICE_PATH
        self.CREDENTIALS_USER_PATH = cfg.CREDENTIALS_USER_PATH
        self.CREDENTIALS_SECRET_FILE_PATH = cfg.CREDENTIALS_SECRET_FILE_PATH
        self.SCOPES = cfg.SCOPES


