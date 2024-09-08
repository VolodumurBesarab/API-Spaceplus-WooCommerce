import json

from modules.AdvertsCreator.create_advert import CreateAdvert

def lambda_handler(event, context):
    create_advert = CreateAdvert()

    # try:
        # payload_data = json.loads(event['body'])
    payload_data = event
    product_id = payload_data["product_id"]
    title = payload_data["title"]
    description = payload_data["description"]
    price = payload_data["price"]
    new_used = payload_data["new_used"]
    manufacturer = payload_data["manufacturer"]
    parts_category = payload_data["parts_category"]
    shipping = payload_data["shipping"]
    # images = payload_data["images"]
    # manufacturer_code = payload_data["manufacturer_code"]
    create_advert.create_woocommerce_advert(title=title,
                                            price=price,
                                            product_id=product_id,
                                            description=description,
                                            parts_category=parts_category,
                                            shipping=shipping,
                                            new_used=new_used,
                                            manufacturer=manufacturer)

    # except Exception as e:
    #     print(e)
        # reports_creator.create_base_report(str(product_id), str(e))

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }