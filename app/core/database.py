from typing import Iterator

from sqlmodel import SQLModel, Session, create_engine

# SQLite file in project root
DATABASE_URL = "sqlite:///./books.db"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
)

def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)
