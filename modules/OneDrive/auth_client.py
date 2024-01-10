import json
import os
import threading

from msal import ConfidentialClientApplication


class AuthClient:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(AuthClient, cls).__new__(cls)
                    cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if not self.__initialized:
            secrets_file_path = r'D:\API-Spaceplus-WooCommerce\secrets.json'
            if os.path.exists(secrets_file_path):
                with open(secrets_file_path) as secrets:
                    self.secrets = json.load(secrets)

                self.application_id = self.secrets.get("VLAD_APPLICATION_ID")
                self.client_secret = self.secrets.get("VLAD_CLIENT_SECRET")
                self.authority_url = self.secrets.get("authority_url")

            else:
                self.application_id = os.environ["VLAD_APPLICATION_ID"]
                self.client_secret = os.environ["VLAD_CLIENT_SECRET"]
                self.authority_url = os.environ["authority_url"]

            self.default_scope = ['https://graph.microsoft.com/.default']
            self.base_url = "https://graph.microsoft.com/v1.0/"
            self.endpoint = self.base_url + "users/andrzej.besarab@spacelpus.onmicrosoft.com/"

            self.client = None
            self.access_token = None

    def get_access_token_default_scopes(self) -> str:
        if not self.access_token:
            self.client = ConfidentialClientApplication(
                client_id=self.application_id,
                client_credential=self.client_secret,
                authority=self.authority_url
            )
            token_result = self.client.acquire_token_silent(self.default_scope, account=None)
            # If the token is available in cache, save it to a variable
            if token_result:
                access_token = 'Bearer ' + token_result['access_token']
                print('Access token was loaded from cache')

            # If the token is not available in cache, acquire a new one from Azure AD and save it to a variable
            if not token_result:
                token_result = self.client.acquire_token_for_client(scopes=self.default_scope)
                self.access_token = 'Bearer ' + token_result['access_token']
                print('New access token was acquired from Azure AD')
            return self.access_token
        return self.access_token

    def get_endpoint(self) -> str:
        return self.endpoint

    def get_default_header(self):
        return {'Authorization': self.get_access_token_default_scopes()}
