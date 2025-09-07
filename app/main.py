from fastapi import FastAPI
from app.api.v1.books_controller import router as books_router
from app.core.database import create_db_and_tables

app = FastAPI(
    title="Books API",
    version="1.0.0",
    description="Books API with SQLite via SQLModel.",
)

# # For simple SQLite storage
# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()

@app.get("/", tags=["Health"])
def health() -> dict:
    return {"status": "ok"}

app.include_router(books_router, prefix="/books", tags=["Books"])
