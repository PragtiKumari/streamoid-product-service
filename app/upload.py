import csv
import io
from typing import Any

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from .db import SessionLocal
from .models import Product

router = APIRouter(tags=["Upload"])

REQUIRED_HEADERS = {"sku", "name", "brand", "color", "size", "mrp", "price", "quantity"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _to_int(value: Any, field: str, reasons: list[str]) -> int | None:
    if value is None or str(value).strip() == "":
        reasons.append(f"{field} is required")
        return None
    try:
        return int(str(value).strip())
    except ValueError:
        reasons.append(f"{field} must be an integer")
        return None


def validate_row(row: dict[str, Any]) -> tuple[dict[str, Any] | None, list[str]]:
    reasons: list[str] = []

    # Required text fields
    for field in ["sku", "name", "brand"]:
        v = row.get(field)
        if v is None or str(v).strip() == "":
            reasons.append(f"{field} is required")

    # Optional-ish in real life, but in this take-home they are part of CSV structure
    # We'll accept empty color/size but keep them as None
    color = row.get("color")
    size = row.get("size")

    mrp = _to_int(row.get("mrp"), "mrp", reasons)
    price = _to_int(row.get("price"), "price", reasons)
    quantity = _to_int(row.get("quantity"), "quantity", reasons)

    # Business rules
    if mrp is not None and price is not None:
        if price > mrp:
            reasons.append("price must be less than or equal to mrp")

    if quantity is not None and quantity < 0:
        reasons.append("quantity must be greater than or equal to 0")

    if reasons:
        return None, reasons

    cleaned = {
        "sku": str(row["sku"]).strip(),
        "name": str(row["name"]).strip(),
        "brand": str(row["brand"]).strip(),
        "color": (str(color).strip() if color is not None and str(color).strip() != "" else None),
        "size": (str(size).strip() if size is not None and str(size).strip() != "" else None),
        "mrp": mrp,
        "price": price,
        "quantity": quantity,
    }
    return cleaned, []


@router.post("/upload")
async def upload_products_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a .csv file")

    content = await file.read()
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="CSV must be UTF-8 encoded")

    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames is None:
        raise HTTPException(status_code=400, detail="CSV header row is missing")

    headers = {h.strip().lower() for h in reader.fieldnames if h is not None}
    missing = REQUIRED_HEADERS - headers
    if missing:
        raise HTTPException(status_code=400, detail=f"Missing required columns: {sorted(list(missing))}")

    stored = 0
    failed: list[dict[str, Any]] = []

    for row_num, row in enumerate(reader, start=2):  # row 1 is header
        normalized = {k.strip().lower(): (v.strip() if isinstance(v, str) else v) for k, v in row.items()}

        cleaned, reasons = validate_row(normalized)
        if reasons:
            failed.append({"row_number": row_num, "row": normalized, "reasons": reasons})
            continue

        # Duplicate SKU check
        existing = db.query(Product).filter(Product.sku == cleaned["sku"]).first()
        if existing:
            failed.append(
                {
                    "row_number": row_num,
                    "row": normalized,
                    "reasons": ["duplicate sku"],
                }
            )
            continue

        product = Product(**cleaned)
        db.add(product)

        try:
            db.commit()
            stored += 1
        except Exception:
            db.rollback()
            failed.append(
                {
                    "row_number": row_num,
                    "row": normalized,
                    "reasons": ["database error while inserting row"],
                }
            )

    return {
        "filename": file.filename,
        "stored": stored,
        "failed": failed,
    }
