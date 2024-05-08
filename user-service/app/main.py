import uvicorn
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from DAL import DBManager
from common import ConfigVars
from api.v1.customer_routes import router as customer_router



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



app.include_router(customer_router)



@app.get('/')
async def index():
    return {"Real": "Python"}



def load_seed_data():
    import os
    import csv
    import logging
    from sqlalchemy.orm import Session
    from DAL import CustomerRepository, CustomerCreateDTO
    
    logger = logging.getLogger()
    logger.info("Attempting to read dataset.csv")
    if not os.path.exists('dataset.csv'):
        logger.error("Aborting seed data loading operation as dataset.csv is not found")
    
    with Session(DBManager.engine) as session:
        repo = CustomerRepository(session)
        if len(repo.get_all()) > 5: return
        
        with open('dataset.csv', 'r') as csv_handle:
            reader = csv.DictReader(csv_handle)
            
            added_names = set()
            for r in reader:
                
                if r["name"] in added_names: continue
                
                try:
                    dto = CustomerCreateDTO(title=r["name"], gender=r["gender"], age=r["age"], location=r["location"], preference=r["preferences"])
                    repo.add(dto)
                    
                    added_names.add(r["name"])
                except:
                    logger.warning(f"Exception raised while adding {r['id']} - {r['name']} in DB. Skipping record . . .")



if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8001)