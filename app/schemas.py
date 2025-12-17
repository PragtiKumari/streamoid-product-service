from pydantic import BaseModel

class ProductOut(BaseModel):
    sku: str
    name: str
    brand: str
    color: str | None = None
    size: str | None = None
    mrp: int
    price: int
    quantity: int

    class Config:
        from_attributes = True


class PaginatedProducts(BaseModel):
    page: int
    limit: int
    total: int
    items: list[ProductOut]
