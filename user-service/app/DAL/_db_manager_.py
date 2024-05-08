from typing import Iterator
from functools import lru_cache

from sqlalchemy.orm import Session
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from common import ConfigVars



@lru_cache()
def initialize():
    if ConfigVars.DB_SCHEMA is not None:
        from sqlalchemy.schema import CreateSchema
        with engine.connect() as conn:
            conn.execute(CreateSchema(ConfigVars.DB_SCHEMA, if_not_exists=True))
            conn.commit()
    DBDeclerativeBase.metadata.create_all(bind=engine)



engine = create_engine(ConfigVars.DATABASE_URI, echo=ConfigVars.IS_DEV)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
DBDeclerativeBase = declarative_base(metadata=MetaData(schema=ConfigVars.DB_SCHEMA))

def get_session() -> Iterator[Session]:
    session = SessionLocal()
    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.close()
