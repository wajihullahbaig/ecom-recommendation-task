import uvicorn
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from common import ConfigVars, MilvusUtils, VectorUtils
from api.v1.recommendation_routes import router as recommendation_router



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
    MilvusUtils.configure_milvus(recreate_collections=False)
    logging.getLogger().info("Milvus Initialized Successfully :)")
    _ = VectorUtils.text_to_vector("This is a sample string", True)
    logging.getLogger().info("Embeddings Initialized Successfully :)")



app.include_router(recommendation_router)



@app.get('/')
async def index():
    return {"Real": "Python"}



if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)