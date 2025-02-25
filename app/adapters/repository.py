import abc

from app.domain.models.auth import User
from app.domain.models.blog import Blog, Tag


class UserRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_email(self, email: str) -> User:
        raise NotImplementedError


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session):
        self.session = session

    def add(self, user: User):
        self.session.add(user)

    def get(self, id: int):
        return self.session.query(User).filter_by(id=id).first()

    def get_by_email(self, email: str):
        return self.session.query(User).filter_by(email=email).first()


class AbstractBlogRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, blog: Blog):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int):
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_by_tags(self, tags: list[Tag]):
        raise NotImplementedError



class SqlAlchemyBlogRepository(abc.ABC):
    def __init__(self, session):
        self.session = session

    def add(self, blog: Blog):
        self.session.add(blog)

    def get(self, id: int):
        return self.session.query(Blog).filter_by(id=id).first()
