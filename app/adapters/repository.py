import abc

from app.domain.models.auth import User
from app.domain.models.blog import Blog, Comment, Tag


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

    def get(self, id: int) -> User:
        return self.session.query(User).filter_by(id=id).first()

    def get_by_email(self, email: str) -> User:
        return self.session.query(User).filter_by(email=email).first()


class BlogRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, blog: Blog):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int) -> Blog:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, blog: Blog):
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_tags(self, tags: list[Tag]) -> list[Blog]:
        raise NotImplementedError


class SqlAlchemyBlogRepository(abc.ABC):
    def __init__(self, session):
        self.session = session

    def add(self, blog: Blog):
        self.session.add(blog)

    def get(self, id: int) -> Blog:
        return self.session.query(Blog).filter_by(id=id).first()

    def delete(self, blog: Blog) -> Blog:
        self.session.delete(blog)

    def get_by_tags(self, tags: list[Tag]) -> list[Blog]:
        pass


class CommentRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, comment: Comment):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int) -> Comment:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, comment: Comment):
        raise NotImplementedError

    @abc.abstractmethod
    def get_blog_comments(self, blog_id: int) -> list[Comment]:
        raise NotImplementedError


class SqlAlchemyCommentRepository(CommentRepository):
    def __init__(self, session):
        self.session = session

    def add(self, comment: Comment):
        self.session.add(comment)

    def get(self, id: int) -> Comment:
        return self.session.query(Comment).filter_by(id=id).first()

    def delete(self, comment: Comment):
        self.session.delete(comment)

    def get_blog_comments(self, blog_id: int) -> list[Comment]:
        return self.session.query(Comment).filter_by(blog_id=blog_id).all()
