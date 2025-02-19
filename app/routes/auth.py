from dataclasses import asdict
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from jose import JWTError, jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app import config, utils
from app.config import database_url
from app.domain.models.auth import User
from app.domain.schemas import UserAuth, UserBase, UserRegister

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

session_factory = sessionmaker(bind=create_engine(database_url))


def get_token(request: Request):
    token = request.cookies.get("users_access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found"
        )
    return token


async def get_current_user(
    token: str = Depends(get_token), session: Session = Depends(session_factory)
):
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

    user = await session.query(User).filter_by(id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user


@auth_router.post("/register/")
async def register_user(
    user_data: UserRegister, session: Session = Depends(session_factory)
):
    user = session.query(User).filter_by(email=user_data.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exsists"
        )

    user_data_dict = user_data.model_dump()
    del user_data_dict["confirm_password"]
    user = User(**user_data_dict)

    session.add(user)
    session.commit()


@auth_router.post("/login/")
async def auth_user(
    response: Response, user_data: UserAuth, session: Session = Depends(session_factory)
):
    user = session.query(User).filter_by(email=user_data.email).first()
    if user and utils.verify_password(user_data.password, user.password):
        access_token = utils.create_access_token({"sub": str(user.id)})
        response.set_cookie(key="users_access_token", value=access_token, httponly=True)
        return {
            "ok": True,
            "access_token": access_token,
            "message": "Authorization is successfully",
        }
    else:
        return {
            "ok": False,
            "message": "Authorization is failed",
        }


@auth_router.post("/logout/")
async def logout(response: Response):
    response.delete_cookie(key="users_access_token")
    return {"message": "User is successfully logout"}


@auth_router.post("/me/")
async def get_me(user_data: User = Depends(get_current_user)):
    return UserBase.model_validate(asdict(user_data))
