from pydantic import BaseModel, HttpUrl


class URLCreate(BaseModel):
    original_url: HttpUrl  # checks for valid URL format


class URLInfo(BaseModel):
    id: int
    original_url: str
    short_code: str
    # visit_count: int

    class Config:
        orm_mode = True  # can work with ORM objects
