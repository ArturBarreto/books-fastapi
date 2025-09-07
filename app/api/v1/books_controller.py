from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlmodel import Session

from app.core.exceptions import NotFoundError
from app.core.database import get_session
from app.models.book_models import Book, BookCreate, BookUpdate
from app.repository.book_repository_sql import BookRepositorySQL
from app.services.book_service import BookService

router = APIRouter()

def get_service(session: Session = Depends(get_session)) -> BookService:
    repo = BookRepositorySQL(session)
    return BookService(repo)

@router.get("", response_model=List[Book])
def list_books(
    response: Response,
    author: Optional[str] = Query(None, description="Filter by author (exact match)"),
    genre: Optional[str] = Query(None, description="Filter by genre (exact match)"),
    year: Optional[int] = Query(None, ge=1000, le=2024, description="Filter by publication year"),
    page: int = Query(1, ge=1, description="Page number (1-based)"),
    page_size: int = Query(10, ge=1, le=100, description="Page size"),
    svc: BookService = Depends(get_service),
) -> List[Book]:
    items, total = svc.list_books(author=author, genre=genre, year=year, page=page, page_size=page_size)
    response.headers["X-Total-Count"] = str(total)
    return items

@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int, svc: BookService = Depends(get_service)) -> Book:
    try:
        return svc.get_book(book_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("", status_code=status.HTTP_201_CREATED, response_model=Book)
def create_book(payload: BookCreate, response: Response, svc: BookService = Depends(get_service)) -> Book:
    created = svc.create_book(payload)
    response.headers["Location"] = f"/books/{created.id}"
    return created

@router.put("/{book_id}", response_model=Book)
def update_book(book_id: int, payload: BookUpdate, svc: BookService = Depends(get_service)) -> Book:
    try:
        return svc.update_book(book_id, payload)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, svc: BookService = Depends(get_service)) -> None:
    try:
        svc.delete_book(book_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
