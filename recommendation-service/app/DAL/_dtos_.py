from pydantic import BaseModel
from typing import Optional, List



class RecommendationResultDTO(BaseModel):
    product_id: int
    product:str
    
    category_id: int
    category:str



# SHARED WITH CATALOG SERVICE
class ProductInfoDTO(BaseModel):
    category_id:int
    category_title:str
    product_id:int
    product_title:str
    product_tags:List[str]
    
class CustomerPurchaseRecordDTO(BaseModel):
    category_title:str
    product_title:str
    product_tags:Optional[List[str]]
    
class CustomerPurchaseCollectionDTO(BaseModel):
    id:int
    age:int
    title:str
    gender:str
    location:str
    preference:str
    
    purchases:Optional[List[CustomerPurchaseRecordDTO]]