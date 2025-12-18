from typing import List, Union

from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session

from .upload import router as upload_router
from .db import Base, engine, get_db
from . import models  # registers Product model
from .models import Product
from .schemas import PaginatedProducts, ProductOut

app = FastAPI(title="Streamoid Product Service", version="1.0.0")

# Create DB tables on startup
Base.metadata.create_all(bind=engine)

# Include upload router
app.include_router(upload_router)


@app.get("/")
def root():
    return {"message": "Streamoid Product Service. Visit /docs for API documentation."}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/products", response_model=Union[PaginatedProducts, List[ProductOut]])
def list_products(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    raw: bool = Query(False, description="If true, return a plain list (non-paginated)"),
    db: Session = Depends(get_db),
):
    query = db.query(Product)

    if raw:
        return query.all()

    offset = (page - 1) * limit
    total = query.count()
    products = query.offset(offset).limit(limit).all()

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "items": products,
    }


@app.get("/products/search", response_model=Union[PaginatedProducts, List[ProductOut]])
def search_products(
    brand: str | None = None,
    color: str | None = None,
    minPrice: int | None = Query(None, ge=0),
    maxPrice: int | None = Query(None, ge=0),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    raw: bool = Query(False, description="If true, return a plain list (non-paginated)"),
    db: Session = Depends(get_db),
):
    query = db.query(Product)

    if brand:
        query = query.filter(Product.brand.ilike(f"%{brand}%"))

    if color:
        query = query.filter(Product.color.ilike(f"%{color}%"))

    if minPrice is not None:
        query = query.filter(Product.price >= minPrice)

    if maxPrice is not None:
        query = query.filter(Product.price <= maxPrice)

    if raw:
        return query.all()

    total = query.count()
    offset = (page - 1) * limit
    items = query.offset(offset).limit(limit).all()

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "items": items,
    }
