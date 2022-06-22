import os

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials as cu
from google.oauth2.service_account import Credentials as cs
from googleapiclient.errors import HttpError


class GoogleAPI:
    service = None

    def __init__(self, cfg):
        self.CREDENTIALS_SERVICE_PATH = cfg.CREDENTIALS_SERVICE_PATH
        self.CREDENTIALS_USER_PATH = cfg.CREDENTIALS_USER_PATH
        self.CREDENTIALS_SECRET_FILE_PATH = cfg.CREDENTIALS_SECRET_FILE_PATH
        self.SCOPES = cfg.SCOPES

    def authorize_from(self, account):
        credentials = None
        if account == 'user':
            if os.path.exists(self.CREDENTIALS_USER_PATH):
                credentials = cu.from_authorized_user_file(self.CREDENTIALS_USER_PATH, self.SCOPES)
            if not credentials or not credentials.valid:
                if credentials and credentials.expired and credentials.refresh_token:
                    credentials.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(self.CREDENTIALS_SECRET_FILE_PATH, self.SCOPES)
                    credentials = flow.run_local_server(port=0)
                with open(self.CREDENTIALS_USER_PATH, 'w') as token:
                    token.write(credentials.to_json())
        elif account == 'service_account':
            credentials = cs.from_service_account_file(self.CREDENTIALS_SERVICE_PATH, scopes=self.SCOPES)

        try:
            self.service = build('sheets', 'v4', credentials=credentials)
        except HttpError as err:
            print(err)
