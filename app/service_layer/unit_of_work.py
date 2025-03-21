import abc
from typing import Callable

from sqlalchemy.orm import Session

from app.adapters.repository import (
    BlogRepository,
    CommentRepository,
    SqlAlchemyBlogRepository,
    SqlAlchemyCommentRepository,
    SqlAlchemyTagRepository,
    SqlAlchemyUserRepository,
    TagRepository,
    UserRepository,
)


class AbstractUnitOfWork(abc.ABC):
    users: UserRepository
    blogs: BlogRepository
    comments: CommentRepository
    tags: TagRepository

    def __enter__(self) -> "AbstractUnitOfWork":
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: Callable[[], Session]):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.session.autoflush = True
        self.users = SqlAlchemyUserRepository(self.session)
        self.blogs = SqlAlchemyBlogRepository(self.session)
        self.comments = SqlAlchemyCommentRepository(self.session)
        self.tags = SqlAlchemyTagRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
