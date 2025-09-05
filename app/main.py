from fastapi import FastAPI
from app.api.v1.books_controller import router as books_router

app = FastAPI(
    title="Books API",
    version="1.0.0",
    description="Simple book management API (layered architecture) using in-memory storage.",
)

@app.get("/", tags=["Health"])
def health() -> dict:
    return {"status": "ok"}

app.include_router(books_router, prefix="/books", tags=["Books"])
