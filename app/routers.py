from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .db import get_db
from .schemas import URLCreate, URLInfo
from .service import URLService

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/shorten", response_model=URLInfo)
def shorten_url(url_data: URLCreate, db: Session = Depends(get_db)):
    """
    Create a short URL
    """
    return URLService.create_short_url(db, url_data)


@router.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    """
    Redirects to the original URL if exists
    """
    url = URLService.get_original_url(db, short_code)
    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Short url not found"
        )
    return url
