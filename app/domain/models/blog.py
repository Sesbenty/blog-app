from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from app.domain.models.auth import User


class BlogStatus(str, Enum):
    PUBLISH = "publish"
    HIDE = "hide"
    DELETE = "delete"


@dataclass
class Blog:
    title: str
    body: str
    author_id: int
    status: BlogStatus
    date_publish: datetime

    id: int = None
    author: User = None
    tags: list["Tag"] = None

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"


@dataclass
class Tag:
    name: str
    id: int = None


@dataclass
class BlogTags:
    blog_id: int
    tag_id: int


@dataclass
class Comment:
    text: str
    date_publish: datetime
    author_id: int
    blog_id: int

    id: int = None
