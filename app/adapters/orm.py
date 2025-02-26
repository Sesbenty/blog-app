from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    DateTime,
    Enum,
)
from sqlalchemy.orm import registry, relationship

from app.domain.models.auth import User
from app.domain.models.blog import Blog, BlogStatus, BlogTags, Comment, Tag


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
    Column("status", Enum(BlogStatus)),
    Column("date_publish", DateTime),
)

tags_table = Table(
    "tags",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(50), unique=True),
)

blog_tags_table = Table(
    "blog_tags",
    metadata,
    Column("blog_id", Integer, ForeignKey("blogs.id"), nullable=False, primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), nullable=False, primary_key=True),
)

comment_table = Table(
    "comments",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("text", String(200), nullable=False),
    Column("date_publish", DateTime(timezone=True), nullable=False),
    Column("author_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("blog_id", Integer, ForeignKey("blogs.id"), nullable=False),
)


def start_mappers():
    mapper_registry = registry()

    mapper_registry.map_imperatively(User, users_table)
    mapper_registry.map_imperatively(
        Blog,
        blog_table,
        properties={
            "author": relationship(User, backref="users", order_by=users_table.c.id),
            "tags": relationship(Tag, secondary=blog_tags_table, collection_class=list),
        },
    )
    mapper_registry.map_imperatively(Tag, tags_table)
    mapper_registry.map_imperatively(BlogTags, blog_tags_table)
    mapper_registry.map_imperatively(Comment, comment_table)
