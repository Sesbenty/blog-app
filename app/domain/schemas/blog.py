from pydantic import BaseModel

from app.domain.schemas.auth import UserInfo


class BlogBase(BaseModel):
    title: str
    body: str


class BlogCreate(BlogBase):
    pass

class BlogInfo(BlogBase):
    id: int
    author: UserInfo
