from datetime import date
from pydantic import BaseModel



class CustomerCreateDTO(BaseModel):
    title:str
    gender:str
    age:int
    location:str
    preference:str

class CustomerDTO(CustomerCreateDTO):
    id: int
    
    class Config:
        orm_mode = True
        use_enum_values = True
