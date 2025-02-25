from dataclasses import dataclass

from app.domain.models.auth import User


@dataclass
class Blog:
    title: str
    body: str
    author_id: int

    id: int = None

    author: User = None
    tags: list["Tag"] = None

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"


@dataclass
class Tag:
    id: int
    name: str


@dataclass
class BlogTags:
    blog_id: int
    tag_id: int
