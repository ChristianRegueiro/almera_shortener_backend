from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .settings import DATABASE_URL


class Database:
    def __init__(self, db_url: str = DATABASE_URL):
        self.engine = create_engine(db_url, connect_args={"check_same_thread": False})
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )


Base = declarative_base()  # this is needed for models to inherit from

db = Database()


def get_db():
    session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()
