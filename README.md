# Streamoid Product Service 

A backend API built using **FastAPI** to validate, store, list, and search seller product catalogs uploaded via **CSV files**.

This project simulates a real-world service used by e-commerce platforms to process seller catalogs before publishing them on marketplaces.

---

## 🚀 Key Features

- 📁 **CSV Upload API**
  - Accepts product catalogs in CSV format
  - Validates each row independently
  - Supports partial success (valid rows stored, invalid rows reported)

- ✅ **Row-level Validation**
  - Required fields check
  - `price ≤ mrp`
  - `quantity ≥ 0`
  - Duplicate SKU detection

- 🗃️ **Persistent Storage**
  - Stores valid products in SQLite using SQLAlchemy ORM

- 📃 **Product Listing**
  - Paginated listing using `page` and `limit`

- 🔍 **Search & Filters**
  - Filter products by brand, color, and price range *(in progress)*

- 📖 **Auto-generated API Docs**
  - Swagger UI available at `/docs`

---

## 🛠 Tech Stack

- **Python**
- **FastAPI**
- **SQLAlchemy**
- **SQLite**
- **Pytest** (for unit testing – planned)

---

## 📂 Project Structure
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


## ⚙️ Setup Instructions (Windows / VS Code)

1️⃣ Clone the repository
```powershell
git clone https://github.com/PragtiKumari/streamoid-product-service.git
cd streamoid-product-service

2️⃣ Create & activate virtual environment
```py -m venv .venv
.\.venv\Scripts\Activate.ps1
