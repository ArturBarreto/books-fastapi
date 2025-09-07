from typing import Optional
from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Field as SQLField

MAX_YEAR = 2024  # per exercise requirement

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    isbn: Optional[str] = Field(
        default=None,
        min_length=13,
        max_length=13,
        pattern=r"^\d{13}$",
        description="13-digit ISBN (digits only) if provided."
    )
    publication_year: Optional[int] = Field(default=None, ge=1000, le=MAX_YEAR)
    genre: Optional[str] = Field(default=None, min_length=1, max_length=50)

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    author: Optional[str] = Field(default=None, min_length=1, max_length=100)
    isbn: Optional[str] = Field(default=None, min_length=13, max_length=13, pattern=r"^\d{13}$")
    publication_year: Optional[int] = Field(default=None, ge=1000, le=MAX_YEAR)
    genre: Optional[str] = Field(default=None, min_length=1, max_length=50)

class Book(BookBase):
    id: int

class BookORM(SQLModel, table=True):
    __tablename__ = "books"

    id: Optional[int] = SQLField(default=None, primary_key=True, index=True)
    title: str
    author: str
    isbn: Optional[str] = None
    publication_year: Optional[int] = None
    genre: Optional[str] = None
