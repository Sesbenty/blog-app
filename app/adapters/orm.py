from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, Table, Text
from sqlalchemy.orm import registry, relationship

from app.domain.models.auth import User
from app.domain.models.blog import Blog


metadata = MetaData()

users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("email", String(50), nullable=False),
    Column("first_name", String(50)),
    Column("last_name", String(50)),
    Column("password", String(255), nullable=False),
)

blog_table = Table(
    "blogs",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(50)),
    Column("body", Text(5000)),
    Column("author_id", Integer, ForeignKey("users.id"), nullable=False),
)


def start_mappers():
    mapper_registry = registry()

    mapper_registry.map_imperatively(User, users_table)
    mapper_registry.map_imperatively(
        Blog,
        blog_table,
        properties={
            "author": relationship(User, backref="users", order_by=users_table.c.id)
        },
    )
