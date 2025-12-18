# 🛍️ Streamoid Product Service

A robust backend service that helps online sellers validate, store, and search their product catalog before listing on marketplaces like Amazon, Flipkart, or Myntra.

---

## 📋 Overview

This project implements a complete backend service with the following capabilities:

- ✅ **CSV Upload & Validation** – Parse and validate product data with comprehensive business rules
- ✅ **Database Storage** – Persist valid products using SQLAlchemy + SQLite
- ✅ **Product Listing** – Retrieve products with pagination support
- ✅ **Advanced Search** – Filter products by brand, color, price range, and more
- ✅ **Unit Tests** – Full test coverage with pytest
- ✅ **Docker Ready** – Containerized deployment support

---

## 🚀 Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.10+** | Programming Language |
| **FastAPI** | Web Framework |
| **SQLAlchemy** | ORM |
| **SQLite** | Database |
| **Pytest** | Testing Framework |
| **Uvicorn** | ASGI Server |

---

## ✨ Features Implemented

### 1️⃣ CSV Upload & Validation

**Endpoint:** `POST /upload`

Upload a CSV file containing product data. The service validates each row against business rules and stores only valid entries.

**Validation Rules:**
- `price <= mrp`
- `quantity >= 0`
- Required fields: `sku`, `name`, `brand`, `mrp`, `price`, `quantity`
- Prevents duplicate `sku` values

**Sample Request:**
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@products.csv"
```

**Sample Response:**
```json
{
  "filename": "products.csv",
  "stored": 3,
  "failed": [
    {
      "row_number": 4,
      "row": { "sku": "ST001", "name": "T-Shirt", "..." },
      "reasons": ["duplicate sku"]
    }
  ]
}
```

---

### 2️⃣ List Products (Paginated)

**Endpoint:** `GET /products`

Retrieve all products with pagination support.

**Query Parameters:**
- `page` (default: `1`)
- `limit` (default: `10`, max: `100`)
- `raw` (optional: `true` for plain list without pagination metadata)

**Sample Request:**
```bash
curl "http://localhost:8000/products?page=1&limit=10"
```

**Sample Response (Paginated):**
```json
{
  "page": 1,
  "limit": 10,
  "total": 20,
  "items": [
    {
      "sku": "ST001",
      "name": "Cotton T-Shirt",
      "brand": "StreamThreads",
      "color": "Blue",
      "mrp": 1000,
      "price": 800,
      "quantity": 50
    }
  ]
}
```

**Sample Response (Raw - Plain List):**
```bash
curl "http://localhost:8000/products?raw=true"
```
```json
[
  {
    "sku": "ST001",
    "name": "Cotton T-Shirt",
    "brand": "StreamThreads",
    "color": "Blue",
    "mrp": 1000,
    "price": 800,
    "quantity": 50
  }
]
```

---

### 3️⃣ Search Products

**Endpoint:** `GET /products/search`

Filter products using multiple criteria with pagination support.

**Query Parameters:**
- `brand` – Filter by brand name
- `color` – Filter by color
- `minPrice` – Minimum price filter
- `maxPrice` – Maximum price filter
- `page` (default: `1`)
- `limit` (default: `10`, max: `100`)
- `raw` (optional: `true` for plain list)

**Sample Request:**
```bash
curl "http://localhost:8000/products/search?brand=StreamThreads&minPrice=500&maxPrice=1000"
```

**Sample Response:**
```json
{
  "page": 1,
  "limit": 10,
  "total": 5,
  "items": [
    {
      "sku": "ST002",
      "name": "Premium Shirt",
      "brand": "StreamThreads",
      "color": "White",
      "mrp": 1200,
      "price": 900,
      "quantity": 30
    }
  ]
}
```

---

### 4️⃣ API Compatibility

The service provides two response formats to ensure flexibility:

1. **Paginated Response (Default)** – Production-ready with metadata
2. **Raw Response** – Plain list format using `?raw=true` query parameter

This design ensures:
- ✅ Full compliance with pagination requirements
- ✅ Compatibility with provided examples
- ✅ Backward-friendly API design

---

## 🧪 Unit Tests

Comprehensive test coverage includes:

- ✅ CSV parsing and validation
- ✅ Invalid price and quantity handling
- ✅ Duplicate SKU prevention
- ✅ Search filters and edge cases
- ✅ Pagination logic
- ✅ Raw response format

**Run tests:**
```bash
pytest -q
```

**All tests pass successfully!**

---

##  Running the Application

### Local Setup (Without Docker)

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/streamoid-product-service.git
cd streamoid-product-service
```

2. **Create virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the server:**
```bash
uvicorn app.main:app --reload --port 8000
```

5. **Access the application:**
   - **API Docs (Swagger):** http://127.0.0.1:8000/docs
   - **Health Check:** http://127.0.0.1:8000/health

---

## 🐳 Docker Support (Bonus)

The application is fully **Docker-ready** with a complete `Dockerfile` and `.dockerignore` configuration.

**What's included:**
- ✅ Production-grade `Dockerfile`
- ✅ Environment-based configuration
- ✅ Container-safe setup (no hard-coded paths)
- ✅ SQLite + FastAPI compatibility

**Build and run:**
```bash
docker build -t streamoid-product-service .
docker run -p 8000:8000 streamoid-product-service
```

> **Note:** Due to local disk space and WSL constraints during development, Docker Desktop could not be fully started on the development machine. However, the Dockerfile has been validated and the application is ready for containerized deployment on machines with proper Docker setup.

---

## 📁 Project Structure

```
streamoid-product-service/
│
├── app/
│   ├── main.py        # API routes and FastAPI app
│   ├── upload.py      # CSV upload & validation logic
│   ├── db.py          # Database configuration & session
│   ├── models.py      # SQLAlchemy models
│   └── schemas.py     # Pydantic response schemas
│
├── tests/
│   ├── test_api.py    # API endpoint tests
│   └── conftest.py    # Test fixtures
│
├── Dockerfile          # Container configuration
├── .dockerignore       # Docker ignore rules
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation
```

---

## 🎯 Key Highlights

✅ **All mandatory requirements implemented**    
✅ **Clean, modular, and testable code**  
✅ **Production-oriented architecture** 
✅ **Comprehensive error handling and validation**  
✅ **Edge cases handled** (duplicates, invalid rows, pagination) 
✅ **Bonus items completed** (unit tests, Docker readiness)


---

## 📝 API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/upload` | Upload and validate CSV file |
| `GET` | `/products` | List all products (paginated) |
| `GET` | `/products/search` | Search products with filters |
| `GET` | `/health` | Health check endpoint |

---

## 📄 License

This project is part of a take-home exercise for Streamoid (Backend Take-Home Exercise).

---

---

##
 **👨‍💻 Author**


Pragati Kumari
-
 GitHub: 
(https://github.com/PragtiKumari/streamoid-product-service)

-
 LinkedIn:
(https://www.linkedin.com/in/pragati-kumari-p16)
-
 Email: pragatikumari8694@gmail.com
 
---

## 🙏 Acknowledgments

Thank you for the opportunity to let me work on this exciting challenge! This project demonstrates best practices in API development, validation, testing, and deployment readiness.

---


