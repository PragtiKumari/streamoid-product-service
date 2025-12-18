from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class ProductOut(BaseModel):
    sku: str
    name: str
    brand: str
    color: Optional[str] = None
    size: Optional[str] = None
    mrp: int
    price: int
    quantity: int

    model_config = ConfigDict(from_attributes=True)


class PaginatedProducts(BaseModel):
    page: int
    limit: int
    total: int
    items: List[ProductOut]
