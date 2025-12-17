from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from .upload import router as upload_router
from .db import Base, engine, SessionLocal
from . import models  # registers Product model
from .models import Product
from .schemas import PaginatedProducts

app = FastAPI(title="Streamoid Product Service", version="1.0.0")

# Create DB tables on startup
Base.metadata.create_all(bind=engine)
app.include_router(upload_router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Streamoid Product Service. Visit /docs for API documentation."}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/products", response_model=PaginatedProducts)
def list_products(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    offset = (page - 1) * limit

    total = db.query(Product).count()
    products = db.query(Product).offset(offset).limit(limit).all()

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "items": products,
    }
