# Streamoid Product Service 

A backend service built using **FastAPI** to validate, store, list, and search seller product catalogs uploaded via **CSV files**.

This project implements all the requirements of the take-home exercise, simulating a real-world catalog ingestion service used by e-commerce platforms to process seller product data.

---

## 🚀 Features Implemented

- 📁 **CSV Upload API**
  - Accepts product catalog CSV files
  - Performs row-level validation
  - Supports partial success (valid rows stored, invalid rows reported with reasons)

- ✅ **Data Validation**
  - Required field checks
  - `price ≤ mrp`
  - `quantity ≥ 0`
  - Duplicate SKU detection

- 🗃️ **Persistent Storage**
  - Valid products stored in SQLite database
  - Implemented using SQLAlchemy ORM

- 📃 **Product Listing**
  - Paginated listing using `page` and `limit` query parameters

- 🔍 **Product Search & Filtering**
  - Filter products by brand
  - Filter products by color
  - Filter products by price range (`minPrice`, `maxPrice`)

- 📖 **Auto-Generated API Documentation**
  - Swagger UI available at `/docs`

---

## 🛠 Tech Stack

- **Python**
- **FastAPI**
- **SQLAlchemy**
- **SQLite**
- **Pytest**

---

## 📂 Project Structure

```
streamoid-product-service/
│
├── app/
│   ├── main.py          # Application entry point
│   ├── db.py            # Database configuration
│   ├── models.py        # ORM models
│   ├── schemas.py       # API response schemas
│   └── upload.py        # CSV upload & validation logic
│
├── tests/               # Unit tests
├── products.csv         # Sample CSV (from assignment)
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Setup Instructions (Windows / VS Code)

### 1️⃣ Clone the repository

```powershell
git clone https://github.com/PragtiKumari/streamoid-product-service.git
cd streamoid-product-service
```

### 2️⃣ Create and activate virtual environment

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3️⃣ Install dependencies

```powershell
pip install -r requirements.txt
```

### 4️⃣ Run the server

```powershell
uvicorn app.main:app --reload --port 8000
```

---

## 📖 API Documentation

Once the server is running, open:

👉 **http://127.0.0.1:8000/docs**

All endpoints are fully documented using Swagger UI.

---

## 📤 Upload Product Catalog (CSV)

### Using Swagger UI

1. Open `/docs`
2. Select `POST /upload`
3. Upload `products.csv`
4. Execute

### Using cURL

```powershell
curl.exe -X POST "http://127.0.0.1:8000/upload" -F "file=@products.csv"
```

### Example Response

```json
{
  "filename": "products.csv",
  "stored": 20,
  "failed": []
}
```

---

## 📃 List Products (Pagination)

```http
GET /products?page=1&limit=10
```

Returns paginated product data.

---

## 🔍 Search Products

```http
GET /products/search?brand=StreamThreads&color=Red&minPrice=500&maxPrice=1000
```

Supports filtering by:
- Brand
- Color
- Price range

---

## 🧠 Design Notes

- Each CSV row is validated independently to allow partial success.
- Validation logic ensures business rule correctness before persistence.
- Clean separation of concerns across routing, validation, and persistence layers.
- Database schema enforces uniqueness and data integrity.

---

## 👩‍💻 Author

**Pragati Kumari**

---

## 📄 License

This project is part of a take-home assignment for Streamoid Technologies.
