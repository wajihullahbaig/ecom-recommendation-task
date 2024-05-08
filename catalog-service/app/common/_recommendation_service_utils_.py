import requests
from typing import List
from fastapi import status
from pydantic import BaseModel

from ._app_config_ import ConfigVars

# SHARED WITH RECOMMENDATION SERVICE
class ProductInfoDTO(BaseModel):
    category_id:int
    category_title:str
    product_id:int
    product_title:str
    product_tags:List[str]
    
def vectorize_product_info(dto:ProductInfoDTO):
    recommendation_service_response = requests.post(url=f"{ConfigVars.RECOMMENDATION_SERVICE_BASE_URL}/vectorize_product", 
                                                    data=dto.model_dump_json(), headers={'Content-type': 'application/json', 'Accept': 'application/json'})
    if recommendation_service_response.status_code != status.HTTP_200_OK:
        raise Exception("Error occured while performing product vectorizing operation")
