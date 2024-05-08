from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status, Depends

from DAL import DBManager, \
                PurchaseCreateDTO, PurchaseDTO, CustomerPurchaseCollectionDTO, \
                PurchaseRepository



# Define router
router = APIRouter(
    prefix="/Purchases",
    tags=["Purchases"],
    responses={status.HTTP_404_NOT_FOUND: {"Error": "Requested resource is either relocated or does not exist"}},
)



@router.get('/{purchase_id}', response_model=PurchaseDTO)
async def get_purchase_detail(purchase_id: int, session:Session = Depends(DBManager.get_session)):
    repo = PurchaseRepository(session)
    try:
        return repo.get(purchase_id)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))
    



@router.post('/', response_model=PurchaseCreateDTO)
async def create_purchase(payload: PurchaseCreateDTO, session:Session = Depends(DBManager.get_session)):
    repo = PurchaseRepository(session)
    try:
        return repo.add(payload)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))



@router.get('/customer_purchased_products/{customer_id}', response_model=CustomerPurchaseCollectionDTO)
async def get_customer_purchases_detail(customer_id: int, session:Session = Depends(DBManager.get_session)):
    repo = PurchaseRepository(session)
    try:
        return repo.get_customer_purchases(customer_id)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))