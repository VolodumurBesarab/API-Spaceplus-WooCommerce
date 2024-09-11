import os
import cv2
import boto3
from photo_resizer_base import S3LinkGeneratorBase

S3_BUCKET_NAME = "prod-spaceplus-resized-photo"
S3 = boto3.client("s3")

class PhotoResizerCv(S3LinkGeneratorBase):
    def upload_file_to_s3(self, file_path, rows_to_skip=None, rows_to_read=None):
        # Якщо не потрібно змінювати кількість рядків для завантаження
        if rows_to_skip is None and rows_to_read is None:
            file_name = os.path.basename(file_path)
        else:
            base_name, extension = os.path.splitext(file_path)
            new_file_path = f"{base_name} {rows_to_skip + 1}-{rows_to_skip + rows_to_read}{extension}"
            file_name = os.path.basename(new_file_path)
        S3.upload_file(file_path, S3_BUCKET_NAME, file_name)

    def resize_image(self, file_path, new_size=(800, 600)):
        """Зміна розміру зображення за допомогою OpenCV"""
        # Завантажуємо зображення з файлу
        image = cv2.imread(file_path)
        if image is None:
            print(f"Error loading image: {file_path}")
            return None

        # Зміна розміру
        resized_image = cv2.resize(image, new_size)

        # Зберігаємо нове зображення у той самий файл
        cv2.imwrite(file_path, resized_image)

    def _get_list_and_upload_photos(self, path_to_save_photos: str, product_id: str):
        file_list = self._get_files_in_folder(path_to_save_photos)

        for file_path in file_list:
            file_name = os.path.basename(file_path)

            # Змінюємо розмір перед завантаженням
            self.resize_image(file_path)

            S3.upload_file(file_path, S3_BUCKET_NAME, file_name)
            try:
                S3.head_object(Bucket=S3_BUCKET_NAME, Key=file_name)
                print(f"File {file_name} uploaded to S3.")
            except Exception as e:
                print(f"File {file_name} failed to upload to S3. Error: {e}")

        return file_list

    def generate_public_urls(self, path_to_save_photos: str, product_id: str):
        file_list = self._get_list_and_upload_photos(path_to_save_photos=path_to_save_photos,
                                                     product_id=product_id)

        public_urls = []
        for file_path in file_list:
            s3_object_key = os.path.basename(file_path)
            url_with_params = S3.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": S3_BUCKET_NAME, "Key": s3_object_key},
                ExpiresIn=3600
            )
            url, params = url_with_params.split('?', 1)
            public_urls.append(url)
            print(f"Created {s3_object_key} url: {url}")

        if public_urls:
            return public_urls
        else:
            return None

    def get_formatted_urls(self, list_urls):
        return [{"src": url} for url in list_urls]

# gen = S3LinkGeneratorCv()
# gen.resize_image(file_path=r"C:\Users\Meskalitos\Desktop\Test\testASD.jpg", new_size=[800, 600])
