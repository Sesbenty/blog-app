import abc

from app.domain.models.auth import User


class AbstractUserRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_email(self, email: str):
        raise NotImplementedError


class SqlAlchemyUserRepository(AbstractUserRepository):
    def __init__(self, session):
        self.session = session

    def add(self, user: User):
        self.session.add(user)

    def get(self, id):
        return self.session.query(User).filter_by(id=id).first()

    def get_by_email(self, email: str):
        return self.session.query(User).filter_by(email=email).first()
