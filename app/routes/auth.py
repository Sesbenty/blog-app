from fastapi import APIRouter, Response

from app.domain.schemas import UserAuth, UserRegister

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register/")
async def register_user(user_data: UserRegister):
    pass


@auth_router.post("/login/")
async def auth_user(response: Response, user_data: UserAuth):
    pass


@auth_router.post("/logout/")
async def logout(response: Response):
    pass


@auth_router.post("/me/")
async def get_me():
    pass
