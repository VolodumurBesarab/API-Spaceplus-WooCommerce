import os
import requests

from modules.OneDrive.auth_client import AuthClient
# from modules.reports_creator import ReportsCreator

NL_FOLDER_ID = "01GK3VGRXOWQGPB72LHVB2WIIN642U4NKK"
STOCK_PHOTOS_ID = "01GK3VGRXIBVXNE7ZPRBFI67KLJQLR6ZFG"


class PhotoDownloader:
    """
    This download photos from one drive
    """
    def __init__(self):
        self.auth_client = AuthClient()
        # self.reports_creator = ReportsCreator()
        self.reports_folder_name = "Otomoto Logs"
        self.endpoint = self.auth_client.get_endpoint()
        self.access_token = self.auth_client.get_access_token_default_scopes()
        self.headers = self.auth_client.get_default_header()

    def get_stock_photos_folder_id(self):
        url = os.path.join(self.endpoint, "drive/root:/Holland/stock-photos/")
        response = requests.get(url=url, headers=self.headers)
        response_data = response.json()
        return response_data['id']

    def find_folder_by_name(self, parent_folder_id, folder_name):
        url = os.path.join(self.endpoint, f"drive/items/{parent_folder_id}/children?$filter=name eq '{folder_name}'")
        response = requests.get(url=url, headers=self.headers)
        response_data = response.json()
        if 'value' in response_data and len(response_data['value']) > 0:
            return response_data['value'][0]['id']
        else:
            return None

    def download_files_from_folder(self, folder_id, folder_name) -> str:
        list_to_download = []
        # project_folder = os.getcwd()
        tmp = "/tmp/"
        if not os.path.exists(tmp + "Photos"):
            os.mkdir(tmp + "Photos")
            print("Photos in tmp created")
        photos_path = tmp + "Photos"
        path_to_save_photos = os.path.join(photos_path, folder_name)
        if not os.path.exists(path_to_save_photos):
            os.mkdir(path_to_save_photos)
        url = os.path.join(self.endpoint, f"drive/items/{folder_id}/children")
        response = requests.get(url=url, headers=self.headers)
        response_data = response.json()
        if 'value' in response_data:
            for item in response_data['value']:
                file_id = item['id']
                file_name = item['name']
                list_to_download.append((file_id, file_name))

        for photo_id, name in list_to_download:
            url = os.path.join(self.endpoint, f"drive/items/{photo_id}/content")
            response = requests.get(url=url, headers=self.headers)
            if response.status_code == 200:
                # file_path = os.path.join(project_folder, "Data", "Photos", name)
                file_path = os.path.join(path_to_save_photos, name)
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                    print(f"{name} download successful")
                # self.reports_creator.create_logs(in_storage_id=folder_name,
                #                                  massage=f"{name} download successful",
                #                                  folder_name=self.reports_folder_name)
            else:
                print(f"{name} not downloaded")
                # self.reports_creator.create_logs(in_storage_id=folder_name,
                #                                  massage=f"{name} not downloaded",
                #                                  folder_name=self.reports_folder_name)
        return path_to_save_photos

    def get_photos_public_url(self, folder_name: str):
        response = requests.get(url=self.endpoint + f"drive/items/{NL_FOLDER_ID}/children",
                                headers=self.headers)
        photo_id_list = []
        if response.status_code == 200:
            nl_folder_contents = response.json()
            searched_folder_id = None

            # Знайти папку 'CP06C' у списку вмісту папки 'root/NL'
            for item in nl_folder_contents['value']:
                if item['name'] == folder_name and item['folder']:
                    searched_folder_id = item['id']
                    break

            if searched_folder_id:
                # Отримати вміст папки 'CP06C'
                response_cp06c = requests.get(
                    self.endpoint + f"drive/items/{searched_folder_id}/children",
                    headers=self.headers
                )
                if response_cp06c.status_code == 200:
                    cp06c_folder_contents = response_cp06c.json()
                    for item in cp06c_folder_contents['value']:
                        if item['file']:
                            photo_id_list.append(item['id'])
                else:
                    print(f"Сталася помилка при отриманні вмісту папки CP06C: {response_cp06c.text}")
            else:
                print("Папка CP06C не знайдена у папці root/NL")
        else:
            print(f"Сталася помилка при отриманні вмісту папки root/NL: {response.text}")

        # print(photo_id_list)

        create_link_payload = {
            "type": "view",
            "scope": "anonymous",
            "retainInheritedPermissions": False
        }
        post_headers = {
            'Authorization': self.access_token,
            'Content-Type': 'application/json'
        }

        # create_link_url = self.endpoint + f"drive/items/{photo_id_list[0]}/createLink"
        # create_link_response = requests.post(url=create_link_url, headers=post_headers, json=create_link_payload)
        #
        # if create_link_response.status_code == 200:
        #     create_link_response_json = create_link_response.json()
        #     created_link = create_link_response_json["link"]["webUrl"]

        for item_id in photo_id_list:
            create_link_url = self.endpoint + f"drive/items/{item_id}/createLink"

            create_link_response = requests.post(url=create_link_url, headers=post_headers, json=create_link_payload)

            if create_link_response.status_code == 200:
                create_link_response_json = create_link_response.json()
                created_link = create_link_response_json["link"]["webUrl"]
                print(created_link)

    def download_products_photos(self, product_id) -> str:
        parent_folder_id = self.get_stock_photos_folder_id()
        folder_id = self.find_folder_by_name(parent_folder_id=parent_folder_id,
                                             folder_name=str(product_id))
        path_to_save_photos: str = self.download_files_from_folder(folder_id=folder_id,
                                                                   folder_name=str(product_id))
        print(path_to_save_photos)
        return path_to_save_photos
