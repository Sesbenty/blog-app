from pydantic import BaseModel

from app.domain.schemas.auth import UserInfo


class BlogBase(BaseModel):
    title: str
    body: str


class BlogCreate(BlogBase):
    tags: list["TagResponse"]


class BlogInfo(BlogBase):
    id: int
    author: UserInfo
    tags: list["TagResponse"]

class TagResponse(BaseModel):
    id: int
    name: str