from datetime import datetime
from pydantic import BaseModel

from app.domain.models.blog import BlogStatus
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
    name: str


class FeedFilter(BaseModel):
    pass


class CommentCreate(BaseModel):
    text: str


class CommentUpdate(BaseModel):
    text: str


class BlogStatusChange(BaseModel):
    status: BlogStatus
