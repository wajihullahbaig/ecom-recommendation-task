from sqlalchemy import Column, Integer, String, ForeignKey

from common import ConfigVars
from ._db_manager_ import DBDeclerativeBase



class CategoryModel(DBDeclerativeBase):
    __tablename__ = "category"
    __table_args__ = {"schema": ConfigVars.DB_SCHEMA}
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(150), nullable=False, unique=True, index=True)



class ProductModel(DBDeclerativeBase):
    __tablename__ = "product"
    __table_args__ = {"schema": ConfigVars.DB_SCHEMA}
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False, index=True)
    title = Column(String(150), nullable=False, unique=True)
    description = Column(String(1500), nullable=False)
    tags = Column(String(2500))

class PurchaseModel(DBDeclerativeBase):
    __tablename__ = "purchase"
    __table_args__ = {"schema": ConfigVars.DB_SCHEMA}
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False, index=True)
    customer_id = Column(Integer, nullable=False, index=True)