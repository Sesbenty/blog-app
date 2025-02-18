from sqlalchemy import Column, Integer, MetaData, String, Table
from sqlalchemy.orm import registry

from app.domain.model import User

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


def start_mappers():
    mapper_registry = registry()

    mapper_registry.map_imperatively(User, users_table)
