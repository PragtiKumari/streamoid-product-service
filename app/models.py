from sqlalchemy import Column, Integer, String
from .db import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    sku = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    brand = Column(String, index=True, nullable=False)

    color = Column(String, index=True, nullable=True)
    size = Column(String, nullable=True)

    mrp = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
