import os
from pathlib import Path
from functools import lru_cache
from typing import ClassVar, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

from ._logger_utils_ import configure_logger






class ConfigReader(BaseSettings):
    IS_DEV:Optional[bool] = True
    
    DB_HOST:str
    DB_PORT:int
    DB_USER:str
    DB_PASS:str
    DB_DATABASE:str
    DB_CONNECTOR:Optional[str] = "postgresql"
    DB_SCHEMA:Optional[str] = None
    
    RABBITMQ_URI:Optional[str] = ""
    APP_VERSION:Optional[str] = "1.0.0"
    APP_TITLE:Optional[str] = "user-service"
    APP_SUMMARY:Optional[str] = "This micro-service deals with customer management endpoints"
    
    
    
    DATABASE_URI:ClassVar[str]
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
    ConfigReader.DATABASE_URI = f"{a.DB_CONNECTOR}://{a.DB_USER}:{a.DB_PASS}@{a.DB_HOST}:{a.DB_PORT}/{a.DB_DATABASE}"
    return a



ConfigVars:ConfigReader = initialize()