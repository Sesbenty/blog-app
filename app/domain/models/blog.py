from dataclasses import dataclass


@dataclass
class Blog:
    title: str
    body: str
    author_id: int
