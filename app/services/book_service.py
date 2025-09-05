from typing import List, Optional, Tuple
from app.core.exceptions import NotFoundError
from app.models.book_models import Book, BookCreate, BookUpdate
from app.repository.book_repository import BookRepositoryInMemory

class BookService:
    def __init__(self, repo: BookRepositoryInMemory) -> None:
        self._repo = repo

    def list_books(self, *, author: Optional[str], genre: Optional[str], year: Optional[int],
                   page: int, page_size: int) -> Tuple[List[Book], int]:
        skip = (page - 1) * page_size
        raw_items, total = self._repo.list(author=author, genre=genre, year=year, skip=skip, limit=page_size)
        return [Book(**b) for b in raw_items], total

    def get_book(self, book_id: int) -> Book:
        b = self._repo.get(book_id)
        if not b:
            raise NotFoundError(f"Book with id={book_id} not found")
        return Book(**b)

    def create_book(self, payload: BookCreate) -> Book:
        new_dict = payload.model_dump()
        created = self._repo.create(new_dict)
        return Book(**created)

    def update_book(self, book_id: int, payload: BookUpdate) -> Book:
        existing = self._repo.get(book_id)
        if not existing:
            raise NotFoundError(f"Book with id={book_id} not found")
        update_dict = {k: v for k, v in payload.model_dump().items() if v is not None}
        updated = self._repo.update(book_id, update_dict)
        return Book(**updated)  # type: ignore

    def delete_book(self, book_id: int) -> None:
        ok = self._repo.delete(book_id)
        if not ok:
            raise NotFoundError(f"Book with id={book_id} not found")
