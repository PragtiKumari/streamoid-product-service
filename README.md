# Streamoid Product Service (Take-Home)

Backend service built with **FastAPI + SQLite (SQLAlchemy)**.

## Features
- Upload products via CSV: `POST /upload`  
- List products with pagination: `GET /products?page=&limit=`  
- Search products (to be implemented next): `GET /products/search`  

## Tech Stack
- Python
- FastAPI
- SQLAlchemy
- SQLite (local)

## Setup (Windows / VS Code)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
