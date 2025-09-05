from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_book_valid():
    payload = {
        "title": "The Python Cookbook",
        "author": "David Beazley",
        "isbn": "9781449340377",
        "publication_year": 2013,
        "genre": "Programming"
    }
    r = client.post("/books", json=payload)
    assert r.status_code == 201
    body = r.json()
    assert body["id"] >= 1
    for k in ["title", "author", "isbn", "publication_year", "genre"]:
        assert body[k] == payload[k]

def test_create_book_invalid_year():
    payload = {
        "title": "Too Future",
        "author": "Anon",
        "isbn": "9781449340377",
        "publication_year": 2099,
        "genre": "Sci-Fi"
    }
    r = client.post("/books", json=payload)
    assert r.status_code == 422

def test_get_all_books():
    r = client.get("/books")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_get_existing_book():
    payload = {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "isbn": "9780132350884",
        "publication_year": 2008,
        "genre": "Programming"
    }
    created = client.post("/books", json=payload).json()
    r = client.get(f"/books/{created['id']}")
    assert r.status_code == 200
    assert r.json()["title"] == "Clean Code"

def test_get_nonexistent_book():
    r = client.get("/books/99999")
    assert r.status_code == 404

def test_update_existing_book():
    payload = {
        "title": "Refactoring",
        "author": "Martin Fowler",
        "isbn": "9780201485677",
        "publication_year": 1999,
        "genre": "Programming"
    }
    created = client.post("/books", json=payload).json()
    upd = {"publication_year": 2000}
    r = client.put(f"/books/{created['id']}", json=upd)
    assert r.status_code == 200
    assert r.json()["publication_year"] == 2000

def test_update_nonexistent_book():
    r = client.put("/books/99999", json={"title": "Nope"})
    assert r.status_code == 404

def test_delete_existing_book():
    payload = {
        "title": "Domain-Driven Design",
        "author": "Eric Evans",
        "isbn": "9780321125217",
        "publication_year": 2003,
        "genre": "Software"
    }
    created = client.post("/books", json=payload).json()
    r = client.delete(f"/books/{created['id']}")
    assert r.status_code == 204
    r2 = client.get(f"/books/{created['id']}")
    assert r2.status_code == 404

def test_delete_nonexistent_book():
    r = client.delete("/books/99999")
    assert r.status_code == 404

def test_filters_and_pagination():
    for i in range(1, 6):
        client.post("/books", json={
            "title": f"Book {i}",
            "author": "Same Author" if i % 2 == 0 else "Other Author",
            "isbn": f"97800000000{10+i}",
            "publication_year": 2010 + i,
            "genre": "Fiction" if i <= 3 else "Non-Fiction",
        })
    r = client.get("/books", params={"author": "Same Author"})
    assert r.status_code == 200
    filtered = r.json()
    assert all(b["author"] == "Same Author" for b in filtered)
    r = client.get("/books", params={"page": 1, "page_size": 2})
    assert r.status_code == 200
    assert len(r.json()) == 2
    assert "X-Total-Count" in r.headers
