from pydantic import BaseModel

from app.domain.schemas.auth import UserBase


class BlogBase(BaseModel):
    title: str
    body: str


class BlogInfo(BlogBase):
    id: int
    author: UserBase
