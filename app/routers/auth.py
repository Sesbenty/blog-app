from dataclasses import asdict

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app import utils
from app.adapters.repository import UserRepository
from app.domain.schemas.auth import UserAuth, UserInfo, UserRegister
from app.routers.dependecies import get_uow, get_user_id, get_user_repository
from app.service_layer import services
from app.service_layer.exceptions import ServicesException
from app.service_layer.unit_of_work import AbstractUnitOfWork

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register/")
async def register_user(
    user_data: UserRegister, uow: AbstractUnitOfWork = Depends(get_uow)
):
    try:
        services.register_user(user_data, uow)
    except ServicesException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@auth_router.post("/login/")
async def auth_user(
    response: Response,
    user_data: UserAuth,
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    try:
        user_id = services.auth_user(user_data, uow)
    except ServicesException as e:
        return {
            "ok": False,
            "message": f"Authorization is failed: {str(e)}",
        }
    access_token = utils.create_access_token({"sub": str(user_id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {
        "ok": True,
        "access_token": access_token,
        "message": "Authorization is successfully",
    }


@auth_router.get("/logout/")
async def logout(response: Response):
    response.delete_cookie(key="users_access_token")
    return {"message": "User is successfully logout"}


@auth_router.get("/me/")
async def get_me(
    user_id: int = Depends(get_user_id),
    repo: UserRepository = Depends(get_user_repository),
):
    return UserInfo(**asdict(repo.get(user_id)))
