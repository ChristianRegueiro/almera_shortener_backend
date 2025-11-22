from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timedelta
from .db import Base
from .settings import DEFAULT_EXPIRATION_DAYS


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(
        DateTime,
        default=lambda: datetime.utcnow() + timedelta(days=DEFAULT_EXPIRATION_DAYS),
    )
    clicks = Column(Integer, default=0)
