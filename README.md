# 📚 Books API (FastAPI)

A **FastAPI** application for managing a collection of books with full **CRUD operations**.  
This project was built as part of a technical interview exercise at O|Tech.

---

## 📝 Project Overview

The API exposes REST endpoints for:

- Creating, reading, updating, and deleting books
- Filtering by **author**, **genre**, or **publication year**
- Pagination (`page`, `page_size`) with `X-Total-Count` response header
- Health check endpoint (`/`)

### Features
- **FastAPI** with automatic **OpenAPI/Swagger** documentation
- **Pydantic** validation with constraints:
  - `title` (≤200 chars), `author` (≤100 chars), `isbn` (13 digits), `year` (1000–2024), `genre` (≤50 chars)
- Layered architecture: **controller → service → repository**
- **Default:** In-memory repository (per exercise spec)
- **Optional:** SQLite via SQLModel (requires uncommenting code)

---

## 🛠️ Tech Stack

- **FastAPI** (Python 3.11+)
- **Pydantic** for validation
- **Pytest** for testing
- **Optional:** SQLModel + SQLite

---

## 📂 Folder Structure

```
books-fastapi/
├── app/
│   ├── main.py                    # App entrypoint
│   ├── core/
│   │   ├── database.py            # SQLModel engine/session
│   │   └── exceptions.py          # Custom errors
│   ├── models/
│   │   └── book_models.py         # Pydantic + ORM models
│   ├── api/v1/
│   │   └── books_controller.py    # Routes & DI
│   ├── repository/
│   │   ├── book_repository.py     # In-memory repository
│   │   └── book_repository_sql.py # SQLModel repository
│   └── services/
│       └── book_service.py        # Business logic
├── tests/
│   └── test_books_api.py          # API tests
├── requirements.txt
└── README.md
```

---

## ▶️ How to Run Locally

### Requirements
- Python **3.11+**
- pip

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run (default: in-memory repo)
```bash
uvicorn app.main:app --reload
```

Server will be available at:
- API root: http://localhost:8000/
- Swagger docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## ⚙️ Switching to SQLite (Optional)

By default, the API uses **in-memory storage**.  
To use **SQLite with SQLModel**, uncomment the provided code sections in:

- `app/api/v1/books_controller.py`
- `app/main.py`
- `requirements.txt` (to enable `sqlmodel` and `sqlalchemy`)
- `tests/test_books_api.py` (for DB-backed tests)

Then run:
```bash
uvicorn app.main:app --reload
```

This will create a `books.db` SQLite file locally.

---

## 🧪 Tests

Run all tests with:

```bash
pytest -q
```

The test suite covers:
- Valid and invalid book creation
- Retrieval, update, and deletion
- Filtering and pagination
- Edge cases (invalid ISBN, year out of range, etc.)

> ⚠️ Note: Tests assume **in-memory** by default.  
> If running with SQLite, uncomment the relevant overrides in `tests/test_books_api.py`.

---

## 📖 API Endpoints

| Method | Path           | Description                      | Notes |
|--------|----------------|----------------------------------|-------|
| GET    | `/books`       | List books (with filters & pagination) | Headers: `X-Total-Count` |
| GET    | `/books/{id}`  | Retrieve a book by ID            | 404 if not found |
| POST   | `/books`       | Create a new book                | 201 + `Location` header |
| PUT    | `/books/{id}`  | Update book             | 404 if not found |
| DELETE | `/books/{id}`  | Delete a book                    | 204 if success |

---

## 🧩 Design Decisions

- **In-memory repository** as default to satisfy interview spec
- **SQLite option** included to show extensibility
- **Layered design** for testability and separation of concerns
- **Validation rules** chosen to mirror real-world book attributes
- **Pagination & filters** implemented as bonus features

---

## 🔮 Next Steps

- Add authentication & authorization (JWT/OAuth2)
- Add search capabilities (e.g., by title keywords)
- Containerize with Docker
- CI/CD pipeline with GitHub Actions
- Deploy a demo in AWS

---

## 👤 Author

- **Artur Gomes Barreto**  
  - [LinkedIn](https://www.linkedin.com/in/arturgomesbarreto/)  
  - [GitHub](https://github.com/ArturBarreto) 
  - [Email](artur.gomes.barreto@gmail.com)  
  - [WhatsApp](https://api.whatsapp.com/send?phone=35677562008)  