from sqlalchemy import Column, Integer, String, Date

from common import ConfigVars
from ._db_manager_ import DBDeclerativeBase



class CustomerModel(DBDeclerativeBase):
    __tablename__ = "customer"
    __table_args__ = {"schema": ConfigVars.DB_SCHEMA}
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(150), nullable=False, unique=True)
    gender = Column(String(15), nullable=False)
    age = Column(Integer, nullable=False)
    
    location = Column(String(150), nullable=False)
    
    preference = Column(String(150), nullable=False)
