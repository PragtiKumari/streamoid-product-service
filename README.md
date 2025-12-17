# Streamoid Product Service 

A backend API built using **FastAPI** to validate, store, list, and search seller product catalogs uploaded via **CSV files**.

This project simulates a real-world service used by e-commerce platforms to process seller catalogs before publishing them on marketplaces.

---

##  Key Features

-  **CSV Upload API**
  - Accepts product catalogs in CSV format
  - Validates each row independently
  - Supports partial success (valid rows stored, invalid rows reported)

-  **Row-level Validation**
  - Required fields check
  - `price ≤ mrp`
  - `quantity ≥ 0`
  - Duplicate SKU detection

-  **Persistent Storage**
  - Stores valid products in SQLite using SQLAlchemy ORM

-  **Product Listing**
  - Paginated listing using `page` and `limit`

-  **Search & Filters**
  - Filter products by brand, color, and price range *(in progress)*

-  **Auto-generated API Docs**
  - Swagger UI available at `/docs`

---

## 🛠 Tech Stack

- **Python**
- **FastAPI**
- **SQLAlchemy**
- **SQLite**
- **Pytest** (for unit testing – planned)

---

##  Project Structure
streamoid-product-service/
│
├── app/
│ ├── main.py # FastAPI app entry point
│ ├── db.py # Database setup
│ ├── models.py # SQLAlchemy models
│ ├── schemas.py # Response schemas
│ └── upload.py # CSV upload & validation logic
│
├── tests/ # Unit tests (to be expanded)
├── products.csv # Sample CSV from assignment
├── requirements.txt
├── README.md
└── .gitignore

---

## Features
- Upload products via CSV: `POST /upload`  
- List products with pagination: `GET /products?page=&limit=`  
- Search products (to be implemented next): `GET /products/search`  


##  Setup Instructions (Windows / VS Code)

1️⃣ Clone the repository
```powershell
git clone https://github.com/PragtiKumari/streamoid-product-service.git
cd streamoid-product-service

2️⃣ Create & activate virtual environment
```py -m venv .venv
.\.venv\Scripts\Activate.ps1

3️⃣ Install dependencies
```pip install -r requirements.txt

4️⃣ Run the server
```uvicorn app.main:app --reload --port 8000

---
##  API Documentation
Once the server is running, open:

👉 http://127.0.0.1:8000/docs

All endpoints are documented using Swagger UI.
``` Upload Products CSV
Using Swagger
Go to /docs
Select POST /upload
Upload products.csv
Execute

Using cURL
curl.exe -X POST "http://127.0.0.1:8000/upload" -F "file=@products.csv"

Example Response
{
  "filename": "products.csv",
  "stored": 20,
  "failed": []
}
---
##  List Products (Pagination)
```GET /products?page=1&limit=10

Returns paginated product data.

---
## Design Notes

Each CSV row is validated independently to allow partial success.
Database constraints + application-level validation ensure data integrity.
Clean separation of concerns (routes, validation, persistence).
Designed to be easily extensible (search, Docker, tests).

---
## Author

Pragati Kumari

