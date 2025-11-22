from sqlalchemy.orm import Session
from .models import URL
from .repository import URLRepository
from .schemas import URLCreate, URLInfo
from .utils import generate_short_code
from .settings import MAX_RETRIES
from fastapi import HTTPException, status


class URLService:
    @staticmethod
    def create_short_url(db: Session, url_data: URLCreate) -> URLInfo:
        existing = URLRepository.get_by_original_url(db, str(url_data.original_url))
        if existing:
            return URLInfo(
                id=existing.id,
                original_url=existing.original_url,
                short_code=existing.short_code,
            )

        short_code = URLService._generate_unique_code(db)

        new_url = URL(
            original_url=str(url_data.original_url),
            short_code=short_code,
        )

        saved = URLRepository.save(db, new_url)

        return URLInfo(
            id=saved.id, original_url=saved.original_url, short_code=saved.short_code
        )

    @staticmethod
    def _generate_unique_code(db: Session) -> str:
        retries = MAX_RETRIES

        while retries > 0:
            short_code = generate_short_code()
            if URLRepository.get_by_short_code(db, short_code) is None:
                return short_code

            retries -= 1

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to generate unique short code, please try again later",
        )

    @staticmethod
    def get_original_url(db: Session, short_code: str) -> URL | None:
        url = URLRepository.get_by_short_code(db, short_code)
        if url:
            URLRepository.increment_visit_count(db, url)
        return url
