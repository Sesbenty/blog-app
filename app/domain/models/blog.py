from dataclasses import dataclass

from app.domain.models.auth import User


@dataclass
class Blog:
    title: str
    body: str
    author_id: int

    id: int = None

    author: User = None
