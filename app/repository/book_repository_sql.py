from typing import List, Optional, Tuple
from sqlmodel import select, Session
from app.models.book_models import BookORM


class BookRepositorySQL:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(
        self,
        *,
        author: Optional[str],
        genre: Optional[str],
        year: Optional[int],
        skip: int,
        limit: int
    ) -> Tuple[List[dict], int]:
        base = select(BookORM)
        if author:
            base = base.where(BookORM.author == author)
        if genre:
            base = base.where(BookORM.genre == genre)
        if year is not None:
            base = base.where(BookORM.publication_year == year)

        # total count (simple but fine for SQLite + tests)
        total = len(self.session.exec(base).all())

        # stable ordering + pagination
        page_query = base.order_by(BookORM.id).offset(skip).limit(limit)
        rows = self.session.exec(page_query).all()

        items = [
            {
                "id": r.id,
                "title": r.title,
                "author": r.author,
                "isbn": r.isbn,
                "publication_year": r.publication_year,
                "genre": r.genre,
            }
            for r in rows
        ]
        return items, total

    def get(self, book_id: int) -> Optional[dict]:
        r = self.session.get(BookORM, book_id)
        if not r:
            return None
        return {
            "id": r.id,
            "title": r.title,
            "author": r.author,
            "isbn": r.isbn,
            "publication_year": r.publication_year,
            "genre": r.genre,
        }

    def create(self, data: dict) -> dict:
        row = BookORM(**data)
        self.session.add(row)
        self.session.commit()
        self.session.refresh(row)
        return {
            "id": row.id,
            "title": row.title,
            "author": row.author,
            "isbn": row.isbn,
            "publication_year": row.publication_year,
            "genre": row.genre,
        }

    def update(self, book_id: int, data: dict) -> Optional[dict]:
        row = self.session.get(BookORM, book_id)
        if not row:
            return None
        for k, v in data.items():
            setattr(row, k, v)
        self.session.add(row)
        self.session.commit()
        self.session.refresh(row)
        return {
            "id": row.id,
            "title": row.title,
            "author": row.author,
            "isbn": row.isbn,
            "publication_year": row.publication_year,  # fixed typo here
            "genre": row.genre,
        }

    def delete(self, book_id: int) -> bool:
        row = self.session.get(BookORM, book_id)
        if not row:
            return False
        self.session.delete(row)
        self.session.commit()
        return True
