import os
from abc import ABC, abstractmethod

class PhotoResizerBase(ABC):
    def __init__(self):
        self.REPORTS_FOLDER_NAME = "Otomoto Logs"
        # self.reports_creator = ReportsCreator()

    @abstractmethod
    def upload_file_to_s3(self, file_path, rows_to_skip=None, rows_to_read=None):
        pass

    @abstractmethod
    def generate_public_urls(self, path_to_save_photos: str, product_id: str):
        pass

    @abstractmethod
    def get_formatted_urls(self, list_urls):
        pass

    def _get_files_in_folder(self, folder_path):
        file_list = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_list.append(os.path.join(root, file))
        sorted_file_list = sorted(file_list, key=lambda x: os.path.basename(x))
        return sorted_file_list
