from datetime import datetime
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
    date_publish: datetime
    tags: list["TagResponse"]


class TagResponse(BaseModel):
    id: int
    name: str


class FeedFilter(BaseModel):
    pass


class CommentCreate(BaseModel):
    text: str
