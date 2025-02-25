from datetime import datetime, timezone

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app import config
from app.adapters.repository import (
    BlogRepository,
    SqlAlchemyBlogRepository,
    SqlAlchemyUserRepository,
    UserRepository,
)
from app.config import database_url
from app.service_layer.unit_of_work import SqlAlchemyUnitOfWork

session_factory = sessionmaker(bind=create_engine(database_url))


def get_session():
    return session_factory()


def get_user_repository(
    session: Session = Depends(get_session),
) -> UserRepository:
    return SqlAlchemyUserRepository(session)


def get_blog_repository(
    session: Session = Depends(get_session),
) -> BlogRepository:
    return SqlAlchemyBlogRepository(session)


def get_uow():
    return SqlAlchemyUnitOfWork(session_factory)


def get_token(request: Request):
    token = request.cookies.get("users_access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found"
        )
    return token


def get_user_id(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=config.ALGORITHM)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="The token is not valid!"
        )

    expire: str = payload.get("exp")
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )

    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID not found"
        )

    return user_id
