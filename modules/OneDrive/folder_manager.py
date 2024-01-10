import requests

from modules.OneDrive.auth_client import AuthClient


class FolderManager:
    def __init__(self):
        self.onedrive_auth_client = AuthClient()
        self.headers = self.onedrive_auth_client.get_default_header()
        pass

    def get_root_folder_json(self, one_drive_url):
        result = requests.get(url=one_drive_url, headers=self.headers)
        print(result.json())
        return result.json()
