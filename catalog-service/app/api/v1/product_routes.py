from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status, Depends

from DAL import DBManager, \
                ProductCreateDTO, ProductDTO, \
                ProductRepository


# Define router
router = APIRouter(
    prefix="/products",
    tags=["Products"],
    responses={status.HTTP_404_NOT_FOUND: {"Error": "Requested resource is either relocated or does not exist"}},
)



@router.get('/', response_model=List[ProductDTO])
async def get_all_products(session:Session = Depends(DBManager.get_session)):
    repo = ProductRepository(session)
    return repo.get_all()

@router.get('/{id}', response_model=ProductDTO)
async def get_product(id: int, session:Session = Depends(DBManager.get_session)):
    repo = ProductRepository(session)
    try:
        return repo.get(id)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))

@router.post('/', response_model=ProductDTO)
async def create_product(payload: ProductCreateDTO, session:Session = Depends(DBManager.get_session)):
    repo = ProductRepository(session)
    try:
        dto = repo.add(payload)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))

@router.put('/', response_model=ProductDTO)
async def update_product(payload: ProductDTO, session:Session = Depends(DBManager.get_session)):
    repo = ProductRepository(session)
    try:
        return repo.modify(payload)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))
