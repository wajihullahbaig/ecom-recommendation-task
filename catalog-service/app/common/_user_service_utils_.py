import requests
from fastapi import status, HTTPException

from ._app_config_ import ConfigVars
    
def fetch_customer_info(customer_id:int):
    user_service_response = requests.get(f"{ConfigVars.CUSTOMER_SERVICE_BASE_URL}/{customer_id}")
    if user_service_response.status_code != status.HTTP_200_OK:
        raise Exception(f"Customer having ID: {customer_id} does not exist")
    
    customer_info = user_service_response.json()
    return customer_info