from sqlalchemy.orm import Session
from .models import URL


class URLRepository:
    @staticmethod
    def save(db: Session, url: URL) -> URL:
        db.add(url)
        db.commit()
        db.refresh(url)
        return url

    @staticmethod
    def get_by_short_code(db: Session, short_code: str) -> URL | None:
        return db.query(URL).filter(URL.short_code == short_code).first()

    @staticmethod
    def get_by_original_url(db: Session, original_url: str) -> URL | None:
        return db.query(URL).filter(URL.original_url == original_url).first()

    @staticmethod
    def increment_visit_count(db: Session, url: URL) -> None:
        url.clicks += 1
        db.commit()
        db.refresh(url)
