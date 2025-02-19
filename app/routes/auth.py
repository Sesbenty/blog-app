from dataclasses import asdict

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import utils
from app.domain.models.auth import User
from app.domain.schemas.auth import UserAuth, UserBase, UserRegister
from app.routes.dependecies import get_session, get_current_user

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register/")
async def register_user(
    user_data: UserRegister, session: Session = Depends(get_session)
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
    response: Response, user_data: UserAuth, session: Session = Depends(get_session)
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


@auth_router.get("/logout/")
async def logout(response: Response):
    response.delete_cookie(key="users_access_token")
    return {"message": "User is successfully logout"}


@auth_router.get("/me/")
async def get_me(user_data: User = Depends(get_current_user)):
    return UserBase.model_validate(asdict(user_data))
