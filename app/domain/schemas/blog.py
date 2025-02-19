from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    body: str

