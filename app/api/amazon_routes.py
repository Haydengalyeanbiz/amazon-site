from paapi5_python_sdk.api.default_api import DefaultApi
from paapi5_python_sdk.models.get_items_request import GetItemsRequest
from paapi5_python_sdk.models.get_items_resource import GetItemsResource
from paapi5_python_sdk.models.partner_type import PartnerType
from paapi5_python_sdk.rest import ApiException
import os
from flask import Blueprint, jsonify, request
from flask_login import login_required

ACCESS_KEY = os.getenv('AMAZON_ACCESS_KEY')
SECRET_KEY = os.getenv('AMAZON_SECRET_KEY')
PARTNER_TAG = os.getenv('AMAZON_ASSOCIATE_TAG')
REGION = 'us-east-1'
HOST = f"webservices.amazon.com"

amazon_routes = Blueprint('amazon', __name__)


# *------------------------Fetch Product Details-------------------------------
@amazon_routes.route('/fetch-product-details', methods=['POST'])
@login_required
def fetch_product_details():
    asin = request.json.get('asin')
    if not asin:
        return jsonify({"error": "ASIN is required"}), 400

    try:
        # Initialize the API client without partner_tag
        api_instance = DefaultApi(
            access_key=ACCESS_KEY,
            secret_key=SECRET_KEY,
            host=HOST,
            region=REGION
        )

        # Define the resources you want in the response
        get_items_resources = [
            GetItemsResource.ITEMINFO_TITLE,
            GetItemsResource.OFFERS_LISTINGS_PRICE,
            GetItemsResource.IMAGES_PRIMARY_LARGE
        ]

        # Create the GetItemsRequest
        get_items_request = GetItemsRequest(
            partner_tag=PARTNER_TAG,
            partner_type=PartnerType.ASSOCIATES,
            marketplace='www.amazon.com',
            item_ids=[asin],
            resources=get_items_resources,
        )

        # Make the API call to fetch product details
        response = api_instance.get_items(get_items_request)

        # Process the response and return product info
        if response.items_result and response.items_result.items:
            item = response.items_result.items[0]

            title = item.item_info.title.display_value if item.item_info and item.item_info.title else "Title unavailable"
            price = (item.offers.listings[0].price.display_amount 
                     if item.offers and item.offers.listings and item.offers.listings[0].price 
                     else "Price unavailable")
            imageUrl = (item.images.primary.large.url 
                        if item.images and item.images.primary and item.images.primary.large 
                        else None)

            product_info = {
                'title': title,
                'price': price,
                'imageUrl': imageUrl
            }
            return jsonify(product_info), 200
        else:
            return jsonify({"error": "Product not found"}), 404

    except ApiException as e:
        print(f"API exception: {e}")
        return jsonify({"error": "Failed to fetch product details"}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "Something went wrong"}), 500