import os

import boto3

# from modules.reports_creator import ReportsCreator

S3_BUCKET_NAME = "prod-spaceplus-resized-photo"
S3 = boto3.client("s3")


class S3LinkGenerator:
    def __init__(self):
        # self.reports_creator = ReportsCreator()
        self.REPORTS_FOLDER_NAME = "Otomoto Logs"

    def _get_files_in_folder(self, folder_path):
        file_list = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_list.append(os.path.join(root, file))
        # file_names = [os.path.basename(file_path) for file_path in file_list]
        sorted_file_list = sorted(file_list, key=lambda x: os.path.basename(x))
        return sorted_file_list  # , file_names

    def upload_file_to_s3(self, file_path, rows_to_skip=None, rows_to_read=None):
        # file_name = f"{os.path.basename(file_path)} {rows_to_skip}-{rows_to_skip + rows_to_read}"
        # S3.upload_file(file_path, S3_BUCKET_NAME, file_name)
        if rows_to_skip is None and rows_to_read is None:
            file_name = os.path.basename(file_path)
        else:
            base_name, extension = os.path.splitext(file_path)
            new_file_path = f"{base_name} {rows_to_skip + 1}-{rows_to_skip + rows_to_read}{extension}"
            file_name = os.path.basename(new_file_path)
        S3.upload_file(file_path, S3_BUCKET_NAME, file_name)
        pass

    def _get_list_and_upload_photos(self, path_to_save_photos: str, product_id: str):
        # s3_object_key = None
        file_list = self._get_files_in_folder(path_to_save_photos)
        s3 = boto3.client("s3")

        for file_path in file_list:
            file_name = os.path.basename(file_path)
            s3.upload_file(file_path, S3_BUCKET_NAME, file_name)
            try:
                s3.head_object(Bucket=S3_BUCKET_NAME, Key=file_name)
                print(f"File {file_name} downloaded to S3.")
                # self.reports_creator.create_logs(folder_name=self.REPORTS_FOLDER_NAME,
                #                                  in_storage_id=product_id,
                #                                  massage=f"File {file_name} downloaded to S3.")
            except Exception as e:
                print(f"File {file_name} do not downloaded to S3. Error:{e}")
                # self.reports_creator.create_logs(folder_name=self.REPORTS_FOLDER_NAME,
                #                                  in_storage_id=product_id,
                #                                  massage=f"File {file_name} do not downloaded to S3. Error:{e}")

        return file_list

    def _del_photos(self):
        pass

    def generate_public_urls(self, path_to_save_photos: str, product_id: str):
        file_list = self._get_list_and_upload_photos(path_to_save_photos=path_to_save_photos,
                                                     product_id=product_id)

        public_urls = []

        for file_path in file_list:
            s3_object_key = os.path.basename(file_path)
            url_with_params = S3.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": S3_BUCKET_NAME,
                        "Key": s3_object_key},
                ExpiresIn=3600  # Тут ви можете вказати термін дії посилання в секундах (наприклад, 1 година)
            )
            url, params = url_with_params.split('?', 1)

            public_urls.append(url)
            print(f"Created {s3_object_key} url: {url}")
            # self.reports_creator.create_logs(in_storage_id=product_id,
            #                                  folder_name=self.REPORTS_FOLDER_NAME,
            #                                  massage=f"Created {s3_object_key} url: {url}")
        if public_urls:
            return public_urls
        else:
            return None

    def get_formatted_urls(self, list_urls):
        return [{"src": url} for url in list_urls]
