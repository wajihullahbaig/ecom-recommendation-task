import os
from pathlib import Path
from functools import lru_cache
from typing import ClassVar, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

from ._logger_utils_ import configure_logger






class ConfigReader(BaseSettings):
    IS_DEV:Optional[bool] = True
    
    MILVUS_HOST:str = "localhost"
    MILVUS_PORT:int = 19530
    MILVUS_CONN_ALIAS:str = "ecom_recommender_conn"
    MILVUS_DATABASE:str = "recommendation_schema"
    MILVUS_COL_USERS:str = "user_collection"
    MILVUS_COL_PRODS:str = "product_collection"

    EMBEDDING_DEVICE:Optional[str] = "cpu"
    EMBEDDINGS_MODEL:Optional[str] = "sentence-transformers/all-MiniLM-L12-v2"
    # EMBEDDINGS_MODEL:Optional[str] = "sentence-transformers/all-mpnet-base-v2"
    
    CATALOG_SERVICE_BASE_URL:str
    
    RABBITMQ_URI:Optional[str] = ""

    APP_VERSION:Optional[str] = "1.0.0"
    APP_TITLE:Optional[str] = "recommendation-service"
    APP_SUMMARY:Optional[str] = "This micro-service deals with recommendation related endpoints"
    
    
    
    # Load EnvFile
    env_file:ClassVar[str] = os.path.join(str(Path.home()),f".env.{APP_TITLE}")
    if not os.path.exists(env_file):
        env_file = os.path.abspath(os.path.join(os.getcwd(), ".env"))
    print("\n\nReading configuration from env " + env_file + "\n\n")
    model_config = SettingsConfigDict(env_file=env_file)
    


@lru_cache()
def initialize() -> ConfigReader:
    a = ConfigReader()
    configure_logger(a.APP_TITLE)
    return a



ConfigVars:ConfigReader = initialize()