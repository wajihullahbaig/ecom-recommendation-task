from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status, Depends

from DAL import DBManager, \
                CustomerModel, \
                CustomerCreateDTO, CustomerDTO, \
                CustomerRepository



# Define router
router = APIRouter(
    prefix="/customer",
    tags=["customer"],
    responses={status.HTTP_404_NOT_FOUND: {"Error": "Requested resource is either relocated or does not exist"}},
)



@router.get('/', response_model=List[CustomerDTO])
async def get_all_customers(session:Session = Depends(DBManager.get_session)):
    repo = CustomerRepository(session)
    return repo.get_all()

@router.get('/{id}', response_model=CustomerDTO)
async def get_customer(id: int, session:Session = Depends(DBManager.get_session)):
    repo = CustomerRepository(session)
    try:
        return repo.get(id)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))

@router.post('/', response_model=CustomerDTO)
async def create_customer(payload: CustomerCreateDTO, session:Session = Depends(DBManager.get_session)):
    repo = CustomerRepository(session)
    try:
        return repo.add(payload)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))

@router.put('/', response_model=CustomerDTO)
async def update_customer(payload: CustomerDTO, session:Session = Depends(DBManager.get_session)):
    repo = CustomerRepository(session)
    try:
        return repo.modify(payload)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))
