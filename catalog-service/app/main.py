import uvicorn
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from DAL import DBManager
from common import ConfigVars, RecommendationSVCUtils
from api.v1.product_routes import router as product_router
from api.v1.category_routes import router as category_router
from api.v1.purchase_routes import router as purchase_router



app = FastAPI(
    title=ConfigVars.APP_TITLE,
    version=ConfigVars.APP_VERSION,
    summary=ConfigVars.APP_SUMMARY
)



# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
#     allow_credentials=True
# )
@app.on_event("startup")
async def startup():
    DBManager.initialize()
    logging.getLogger().info("DB Initialized Successfully :)")
    
    load_seed_data()
    logging.getLogger().info("Seed Data Loaded Successfully :)")



app.include_router(product_router)
app.include_router(category_router)
app.include_router(purchase_router)



@app.get('/')
async def index():
    return {"Real": "Python"}



def load_seed_data():
    import os
    import csv
    import logging
    from sqlalchemy.orm import Session
    from DAL import CategoryCreateDTO, ProductCreateDTO, PurchaseCreateDTO, \
                    CategoryRepository, ProductRepository, PurchaseRepository
                    

    logger = logging.getLogger()
    logger.info("Attempting to read dataset.csv")
    if not os.path.exists('dataset.csv'):
        logger.error("Aborting seed data loading operation as dataset.csv is not found")
    
    with Session(DBManager.engine) as session:
        repo_prod = ProductRepository(session)
        repo_cat = CategoryRepository(session)
        repo_prch = PurchaseRepository(session)
        
        if len(repo_prod.get_all()) > 5: return
        
        rows = []
        cat_dict = dict()
        prod_dict = dict()
        with open('dataset.csv', 'r') as csv_handle:
            reader = csv.DictReader(csv_handle)
            for r in reader: 
                rows.append(r)
        
        #region Get all categories
        for r in rows:
            if r["category"].lower().strip() in cat_dict.keys(): continue
            try:
                ccdto = CategoryCreateDTO(title=r["category"].strip())
                cdto = repo_cat.add(ccdto)
                cat_dict[cdto.title.lower()] = cdto.id
            except:
                logger.warning(f"Exception raised while adding Category {r['category']} in DB. Skipping record . . .")
        #endregion

        #region Get all products
        for r in rows:
            if r["product_name"].lower().strip() in prod_dict.keys(): continue
            
            try:
                tags = [t.strip() for t in r["tags"].split(',')]
                pcdto = ProductCreateDTO(title=r["product_name"].strip(), 
                                        category_id=cat_dict[r["category"].lower().strip()],
                                        description=r["description"],
                                        tags=tags)
                pdto = repo_prod.add(pcdto)
                prod_dict[pdto.title.lower()] = pdto.id
                
                product_info_dto = RecommendationSVCUtils.ProductInfoDTO(product_id=pdto.id, product_title=pdto.title,
                                                                         category_id=pdto.category_id, category_title=r["category"],
                                                                         product_tags=pdto.tags)
                RecommendationSVCUtils.vectorize_product_info(product_info_dto)
            except:
                logger.warning(f"Exception raised while adding Product {r['product_name']} in DB. Skipping record . . .")
        #endregion

        #region Get all purchases
        for r in rows:
            try:
                pcdto = PurchaseCreateDTO(customer_id=r["user_id"],
                                          category_id=cat_dict[r["category"].lower().strip()],
                                          product_id=prod_dict[r["product_name"].lower().strip()])
                pdto = repo_prch.add(pcdto)
            except:
                logger.warning(f"Exception raised while adding Purchase of {r['product_name']} by {r['name']} in DB. Skipping record . . .")
        #endregion



if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8001)