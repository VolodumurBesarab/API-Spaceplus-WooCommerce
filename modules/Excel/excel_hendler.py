import os

import pandas as pd
import requests
from pandas import DataFrame

from modules.OneDrive.auth_client import AuthClient
from modules.OneDrive.folder_manager import FolderManager


class ExcelHandler:
    def __init__(self):
        self.onedrive_auth_client = AuthClient()
        self.folder_manager = FolderManager()

        self.endpoint = self.onedrive_auth_client.get_endpoint()
        self.headers = self.onedrive_auth_client.get_default_header()

    def get_exel_file(self, name: str):
        one_drive_url = self.endpoint + "drive/root:/Holland/" + name
        exel_file = self.folder_manager.get_root_folder_json(one_drive_url=one_drive_url)
        file_content = None

        if exel_file:
            file_url = exel_file['@microsoft.graph.downloadUrl']

            response = requests.get(url=file_url)

            if response.status_code == 200:
                file_content = response.content
                print("excel file download successful")
            else:
                print(f"{name} is not found in Onedrive")
        return file_content

    def get_file_path(self, file_name) -> str:
        save_path = "/tmp/" + file_name
        return save_path

    def create_file_on_data(self, file_content, file_name):
        save_path = self.get_file_path(file_name=file_name)
        with open(save_path, 'wb') as file:
            file.write(file_content)


