from typing import Dict, List, Optional, Tuple
from itertools import count

class BookRepositoryInMemory:
    """
    A very simple in-memory repository backed by a list of dicts.
    """
    def __init__(self) -> None:
        self._books: List[Dict] = []
        self._id_gen = count(start=1)

    def list(self, *, author: Optional[str], genre: Optional[str], year: Optional[int],
             skip: int, limit: int) -> Tuple[List[Dict], int]:
        items = self._books
        if author:
            items = [b for b in items if b.get("author") == author]
        if genre:
            items = [b for b in items if b.get("genre") == genre]
        if year is not None:
            items = [b for b in items if b.get("publication_year") == year]
        total = len(items)
        return items[skip: skip + limit], total

    def get(self, book_id: int) -> Optional[Dict]:
        for b in self._books:
            if b["id"] == book_id:
                return b
        return None

    def create(self, data: Dict) -> Dict:
        new = {**data}
        new["id"] = next(self._id_gen)
        self._books.append(new)
        return new

    def update(self, book_id: int, data: Dict) -> Optional[Dict]:
        for idx, b in enumerate(self._books):
            if b["id"] == book_id:
                updated = {**b, **data, "id": book_id}
                self._books[idx] = updated
                return updated
        return None

    def delete(self, book_id: int) -> bool:
        for idx, b in enumerate(self._books):
            if b["id"] == book_id:
                del self._books[idx]
                return True
        return False
