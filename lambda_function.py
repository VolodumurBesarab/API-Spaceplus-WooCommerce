import json

from modules.AdvertsCreator.create_advert import CreateAdvert


# def lambda_handler(event, context):
#     create_advert = CreateAdvert()
#     create_advert.create_advert()
#     # client = boto3.client('lambda')
#     # response = client.invoke(
#     #     FunctionName='prod-spaceplus-create-advert',
#     #     InvocationType='Event',
#     #     Payload='{}',
#     # )
#     # print(response)
#     return {
#         'statusCode': 200,
#         'body': json.dumps('Hello from Lambda!')
#     }

def lambda_handler(event, context):
    create_advert = CreateAdvert()
    try:
        # payload_data = json.loads(event['body'])
        payload_data = event
        product_id = payload_data["product_id"]
        title = payload_data["title"]
        description = payload_data["description"]
        price = payload_data["price"]
        new_used = payload_data["new_used"]
        manufacturer = payload_data["manufacturer"]
        parts_category = payload_data["parts_category"]
        images = payload_data["images"]
        shipping = payload_data["shipping"]
        # manufacturer_code = payload_data["manufacturer_code"]

        create_advert.create_woocommerce_advert(title=title,
                                                price=price,
                                                product_id=product_id,
                                                description=description,
                                                parts_category=parts_category,
                                                images=images,
                                                shipping=shipping,
                                                new_used=new_used,
                                                manufacturer=manufacturer)

        # create_advert.create_woocommerce_advert(product_id=product_id,
        #                                   title=title,
        #                                   description=description,
        #                                   price=price,
        #                                   new_used=new_used,
        #                                   manufacturer=manufacturer,
        #                                   parts_category=parts_category,
        #                                   manufacturer_code=manufacturer_code)
    except Exception as e:
        print(e)
        # reports_creator.create_base_report(str(product_id), str(e))

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }