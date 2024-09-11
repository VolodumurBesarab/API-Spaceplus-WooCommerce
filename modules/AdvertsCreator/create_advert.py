import os

from modules.OneDrive.photo_downloader import PhotoDownloader
# from modules.Photos.photo_resizer_pil import PhotoResizer
from modules.GenerateLink.generate_links_s3bucket import S3LinkGenerator
from modules.Photos.photo_resizer_cv import PhotoResizerCv
# from dotenv import load_dotenv

# load_dotenv()

import requests

SHIPPING_DICT = {"1": "small",
                 "2": "middle",
                 "3": "boxsmall",
                 "4": "boxbig"
                 }

NEW_USED_DICT = {"new": "nowy",
                 "used": "używany"
                 }

PARTS_CATEGORY_DICT = {"Bagażniki dachowe > Bez relingów": [{"id": 51}, {"id": 60}],
                       "Bagażniki dachowe > Na relingi": [{"id": 51}, {"id": 61}],
                       "Boksy dachowe": [{"id": 51}, {"id": 48}],
                       "Części i akcesoria": [{"id": 51}, {"id": 54}],
                       "Uchwyty na narty i snowboardy": [{"id": 51}, {"id": 50}],
                       "Uchwyty rowerowe, Uchwyty rowerowe > Na dach": [{"id": 49}, {"id": 52}],
                       "Uchwyty rowerowe, Uchwyty rowerowe > Na hak": [{"id": 49}, {"id": 53}],
                       "Uchwyty rowerowe, Uchwyty rowerowe > Na klapę": [{"id": 49}, {"id": 59}]
                       }


class CreateAdvert:
    def __init__(self):
        self.photo_downloader = PhotoDownloader()
        # self.photo_resizer = PhotoResizer()
        self.photo_resizer_cv = PhotoResizerCv()
        self.s3_link_generator = S3LinkGenerator()
        # try:
        #     self.CONSUMER_KEY_WC = os.getenv("CONSUMER_KEY_WC")
        #     self.CONSUMER_SECRET_WC = os.getenv("CONSUMER_SECRET_WC")
        #     self.WC_URL = os.getenv("WC_URL")
        # except:
        self.CONSUMER_KEY_WC = os.environ["CONSUMER_KEY_WC"]
        self.CONSUMER_SECRET_WC = os.environ["CONSUMER_SECRET_WC"]
        self.WC_URL = os.environ["WC_URL"]

    def create_woocommerce_advert(self, title, price, product_id, description, parts_category, shipping, new_used, manufacturer):
        photos_folder_path = self.photo_downloader.download_products_photos(product_id=product_id)
        # self.photo_resizer.resize_photo(input_path=photos_folder_path, output_path=photos_folder_path)
        self.photo_resizer_cv.resize_image(photos_folder_path)
        list_urls = self.s3_link_generator.generate_public_urls(path_to_save_photos=photos_folder_path, product_id=product_id)
        images = self.s3_link_generator.get_formatted_urls(list_urls=list_urls)

        # product_id = payload_data["product_id"]
        # title = payload_data["title"]
        # description = payload_data["description"]
        # price = payload_data["price"]
        # new_used = payload_data["new_used"]
        # manufacturer = payload_data["manufacturer"]
        # parts_category = payload_data["parts-category"]
        # images = [{"src": "https://static4.winylownia.pl/pol_pl_PLACEBO-Placebo-LP-60305_1.jpg"}]
        # manufacturer_code = payload_data["manufacturer_code"]

        product_data = {
            "name": title,
            "type": "simple",
            "regular_price": price,
            "description": description,
            "categories": PARTS_CATEGORY_DICT[parts_category],
            "images": images,
            'shipping_required': True,
            'shipping_taxable': True,
            'shipping_class': SHIPPING_DICT[shipping],
            # 'shipping_class_id': shipping[1],
            'attributes': [
                {
                    'id': 0,
                    'name': 'Producent',
                    'position': 0,
                    'visible': True,
                    'variation': True,
                    'options': [
                        manufacturer
                    ]
                },
                {
                    'id': 0,
                    'name': 'Stan',
                    'position': 1,
                    'visible': True,
                    'variation': True,
                    'options': [
                        NEW_USED_DICT[new_used]
                    ]
                }
            ],
        }

        Woocommerceendpoint = 'products'
        print(product_data)
        url = f'{self.WC_URL}{Woocommerceendpoint}'

        response = requests.post(
            url=url, auth=(self.CONSUMER_KEY_WC, self.CONSUMER_SECRET_WC),
            json=product_data
        )
        print(response.status_code)
        print(response.text)
        print(response.json())
        # if response.status_code != 500:
        #     print(response.json())
        # else:
        #     print(response.json())
        print("add report here")

    def get_list_all_products(self):
        Woocommerceendpoint = "products"
        url = f'{self.WC_URL}{Woocommerceendpoint}'
        response = requests.get(
            url=url, auth=(self.CONSUMER_KEY_WC, self.CONSUMER_SECRET_WC))

    def get_product_by_id(self, id):
        Woocommerceendpoint = f"products/{id}"
        url = f'{self.WC_URL}{Woocommerceendpoint}'
        print(url)
        response = requests.get(
            url=url, auth=(self.CONSUMER_KEY_WC, self.CONSUMER_SECRET_WC))
        print(response.json())


# create_advert = CreateAdvert()
# create_advert.get_product_by_id(1188)
# create_advert.get_list_all_products()
# create_advert.create_woocommerce_advert(title="New product 4",
#                                         price="52.99",
#                                         product_id=51111_1,
#                                         description="Smell like long big mouse",
#                                         parts_category="Bagażniki dachowe > Bez relingów",
#                                         images=[{"src": "https://besarab-records.com/wp-content/uploads/2024/01/The-Last-Shadow-Puppets-The-Age-of-Understatement.jpg"}],
#                                         shipping="small",
#                                         manufacturer="Oryginalny",
#                                         new_used="new")
