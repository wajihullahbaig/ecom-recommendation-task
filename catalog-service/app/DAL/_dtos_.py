from pydantic import BaseModel
from typing import Optional, List

class CategoryCreateDTO(BaseModel):
    title: str

class CategoryDTO(CategoryCreateDTO):
    id: int
    
    class Config:
        orm_mode = True



class ProductCreateDTO(BaseModel):
    title: str
    category_id: int
    description: str
    tags: Optional[List[str]]
    
    class Config:
        orm_mode = True
class ProductDTO(ProductCreateDTO):
    id: int



class PurchaseCreateDTO(BaseModel):
    product_id: int
    category_id: int
    customer_id: int
class PurchaseDTO(PurchaseCreateDTO):
    id: int
    
    product_title: str
    category_title: str
    customer_title: str
    
    product_tags:Optional[List[str]]
    class Config:
        orm_mode = True



# SHARED WITH RECOMMENDATION SERVICE
class CustomerPurchaseRecordDTO(BaseModel):
    purchase_id:int
    
    category_id:int
    category_title:str
    
    product_id:int
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