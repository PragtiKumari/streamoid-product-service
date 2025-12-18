import os
import uuid
import importlib
from fastapi.testclient import TestClient


def make_test_db_url() -> str:
    # unique DB file per test run to avoid Windows file-lock issues
    fname = f"test_products_{uuid.uuid4().hex}.db"
    return f"sqlite:///./{fname}"


def get_client(db_url: str):
    os.environ["DATABASE_URL"] = db_url

    import app.db
    import app.models
    import app.upload
    import app.main

    importlib.reload(app.db)
    importlib.reload(app.models)
    importlib.reload(app.upload)
    importlib.reload(app.main)

    # Ensure tables exist for this test DB
    app.db.Base.metadata.create_all(bind=app.db.engine)
    return TestClient(app.main.app)


def cleanup_db_file(db_url: str):
    # db_url looks like sqlite:///./filename.db
    if db_url.startswith("sqlite:///./"):
        fname = db_url.replace("sqlite:///./", "")
        try:
            # dispose engine to release file handles
            import app.db
            app.db.engine.dispose()
        except Exception:
            pass

        if os.path.exists(fname):
            try:
                os.remove(fname)
            except PermissionError:
                pass


def test_upload_stores_valid_rows():
    db_url = make_test_db_url()
    client = get_client(db_url)

    csv_content = (
        "sku,name,brand,color,size,mrp,price,quantity\n"
        "SKU100,Test Tee,BrandA,Black,M,1000,800,5\n"
        "SKU101,Test Shoe,BrandA,White,UK8,2000,1500,3\n"
    )

    files = {"file": ("products.csv", csv_content, "text/csv")}
    resp = client.post("/upload", files=files)
    assert resp.status_code == 200

    data = resp.json()
    assert data["stored"] == 2
    assert data["failed"] == []

    resp2 = client.get("/products?page=1&limit=10")
    assert resp2.status_code == 200
    assert resp2.json()["total"] == 2

    cleanup_db_file(db_url)


def test_upload_rejects_invalid_price_and_quantity():
    db_url = make_test_db_url()
    client = get_client(db_url)

    csv_content = (
        "sku,name,brand,color,size,mrp,price,quantity\n"
        "SKU200,Bad Price,BrandB,Red,M,500,600,2\n"   # price > mrp
        "SKU201,Bad Qty,BrandB,Blue,L,500,400,-1\n"  # quantity < 0
    )

    files = {"file": ("products.csv", csv_content, "text/csv")}
    resp = client.post("/upload", files=files)
    assert resp.status_code == 200

    data = resp.json()
    assert data["stored"] == 0
    assert len(data["failed"]) == 2

    reasons_1 = data["failed"][0]["reasons"]
    reasons_2 = data["failed"][1]["reasons"]

    assert "price must be less than or equal to mrp" in reasons_1
    assert "quantity must be greater than or equal to 0" in reasons_2

    cleanup_db_file(db_url)


def test_search_by_brand_and_price_range():
    db_url = make_test_db_url()
    client = get_client(db_url)

    csv_content = (
        "sku,name,brand,color,size,mrp,price,quantity\n"
        "SKU300,Item1,StreamThreads,Black,M,1000,700,5\n"
        "SKU301,Item2,StreamThreads,Red,L,1000,900,2\n"
        "SKU302,Item3,OtherBrand,Blue,S,1000,800,1\n"
    )

    files = {"file": ("products.csv", csv_content, "text/csv")}
    resp = client.post("/upload", files=files)
    assert resp.status_code == 200
    assert resp.json()["stored"] == 3

    r1 = client.get("/products/search?brand=StreamThreads&page=1&limit=10")
    assert r1.status_code == 200
    assert r1.json()["total"] == 2

    r2 = client.get("/products/search?minPrice=800&maxPrice=900&page=1&limit=10")
    assert r2.status_code == 200
    assert r2.json()["total"] == 2

    cleanup_db_file(db_url)


def test_list_raw_returns_plain_list():
    db_url = make_test_db_url()
    client = get_client(db_url)

    csv_content = (
        "sku,name,brand,color,size,mrp,price,quantity\n"
        "SKU1,Item1,BrandA,Black,M,1000,700,5\n"
        "SKU2,Item2,BrandB,Red,L,1000,900,2\n"
    )

    files = {"file": ("products.csv", csv_content, "text/csv")}
    r = client.post("/upload", files=files)
    assert r.status_code == 200
    assert r.json()["stored"] == 2

    resp = client.get("/products?raw=true")
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert "sku" in data[0]
    assert "price" in data[0]

    cleanup_db_file(db_url)


def test_search_raw_returns_plain_list_filtered():
    db_url = make_test_db_url()
    client = get_client(db_url)

    csv_content = (
        "sku,name,brand,color,size,mrp,price,quantity\n"
        "SKU10,Item1,StreamThreads,Black,M,1000,700,5\n"
        "SKU11,Item2,StreamThreads,Red,L,1000,900,2\n"
        "SKU12,Item3,OtherBrand,Blue,S,1000,800,1\n"
    )

    files = {"file": ("products.csv", csv_content, "text/csv")}
    r = client.post("/upload", files=files)
    assert r.status_code == 200
    assert r.json()["stored"] == 3

    resp = client.get("/products/search?brand=StreamThreads&raw=true")
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert all(p["brand"] == "StreamThreads" for p in data)

    cleanup_db_file(db_url)
