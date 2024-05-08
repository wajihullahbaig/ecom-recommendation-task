from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status, Depends

from DAL import DBManager, \
                CategoryModel, \
                CategoryCreateDTO, CategoryDTO, \
                CategoryRepository



# Define router
router = APIRouter(
    prefix="/category",
    tags=["Categories"],
    responses={status.HTTP_404_NOT_FOUND: {"Error": "Requested resource is either relocated or does not exist"}},
)



@router.get('/', response_model=List[CategoryDTO])
async def get_all_categories(session:Session = Depends(DBManager.get_session)):
    repo = CategoryRepository(session)
    return repo.get_all()

@router.get('/{id}', response_model=CategoryDTO)
async def get_category(id: int, session:Session = Depends(DBManager.get_session)):
    repo = CategoryRepository(session)
    try:
        return repo.get(id)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))

@router.post('/', response_model=CategoryDTO)
async def create_category(payload: CategoryCreateDTO, session:Session = Depends(DBManager.get_session)):
    repo = CategoryRepository(session)
    try:
        return repo.add(payload)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))

@router.put('/', response_model=CategoryDTO)
async def update_category(payload: CategoryDTO, session:Session = Depends(DBManager.get_session)):
    repo = CategoryRepository(session)
    try:
        return repo.modify(payload)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))
