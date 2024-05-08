from typing import Optional, List
from sqlalchemy.orm import Session

from ._models_ import CustomerModel
from . import _db_manager_ as DBManager
from ._dtos_ import CustomerCreateDTO, CustomerDTO



class CustomerRepository():
    def __init__(self, session:Session) -> None:
        self.session = session
    
    def add(self, payload: CustomerCreateDTO) -> CustomerDTO:
        customer = CustomerModel(**payload.model_dump())
        self.session.add(customer)
        self.session.commit()
        self.session.refresh(customer)
        return customer

    def get_all(self, skip:int=0, limit:int=10, ids:List[int]=None) -> Optional[List[CustomerDTO]]:
        if ids is None or len(ids)<1:
            customers = self.session.query(CustomerModel).offset(skip).limit(limit).all()
        else:
            customers = self.session.query(CustomerModel).filter(CustomerModel.id.in_(ids)).offset(skip).limit(limit).all()
        return customers

    def get(self, id) -> Optional[CustomerDTO]:
        customer = self.session.query(CustomerModel).where(CustomerModel.id == id).first()
        if customer is None:
            raise Exception(f"Customer having ID: {id} does not exist")
        return customer


    def modify(self, payload: CustomerDTO) -> CustomerDTO:
        customer_proxy = self.session.query(CustomerModel).filter(CustomerModel.id == payload.id)
        if customer_proxy.first() is None:
            raise Exception(f"Customer having ID: {payload.id} does not exist")
        customer_proxy.update(payload.model_dump(), synchronize_session=False)
        self.session.commit()
        return payload
