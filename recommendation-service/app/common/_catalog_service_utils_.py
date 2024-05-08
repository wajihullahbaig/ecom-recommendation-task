import requests
from fastapi import status, HTTPException

from ._app_config_ import ConfigVars
    
def fetch_customer_purchases(customer_id:int):
    catalog_service_response = requests.get(f"{ConfigVars.CATALOG_SERVICE_BASE_URL}/customer_purchased_products/{customer_id}")
    if catalog_service_response.status_code != status.HTTP_200_OK:
        raise Exception(f"Error encountered while fetching purchase history for Customer-ID : {customer_id}")
    
    return catalog_service_response.json()