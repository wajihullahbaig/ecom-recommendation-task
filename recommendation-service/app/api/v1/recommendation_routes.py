from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status

from DAL import CustomerPurchaseCollectionDTO, ProductInfoDTO, \
                RecommendationResultDTO, \
                RecommendationRepository
from common import CatalogSVCUtils



# Define router
router = APIRouter(
    prefix="/recommendation",
    tags=["recommendation"],
    responses={status.HTTP_404_NOT_FOUND: {"Error": "Requested resource is either relocated or does not exist"}},
)



@router.get('/{customer_id}', response_model=List[RecommendationResultDTO])
async def get_recommendations_for_customer(customer_id: int):
    repo = RecommendationRepository()
    try:
        res = CatalogSVCUtils.fetch_customer_purchases(customer_id)
        cpcdto:CustomerPurchaseCollectionDTO = CustomerPurchaseCollectionDTO.model_validate(res)
        return repo.get_recommendations(cpcdto)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))
    

# @router.post('/vectorize_user')
# async def prepare_customer_data(payload: CustomerPurchaseCollectionDTO):
#     repo = RecommendationRepository()
#     return repo.upsert_user(payload)

@router.post('/vectorize_product')
async def prepare_product_data(payload: ProductInfoDTO):
    repo = RecommendationRepository()
    return repo.upsert_product(payload)