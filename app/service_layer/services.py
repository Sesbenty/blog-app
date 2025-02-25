from app import utils
from app.domain.models.auth import User
from app.domain.schemas.auth import UserAuth, UserRegister
from app.service_layer.unit_of_work import AbstractUnitOfWork


def register_user(user_data: UserRegister,  uow: AbstractUnitOfWork):
    with uow:
        user = uow.users.get_by_email(user_data.email)
        if user is not None:
            raise Exception()
        
        user_data_dict = user_data.model_dump()
        del user_data_dict["confirm_password"]
        user = User(**user_data_dict)

        uow.users.add(user)


def auth_user(user_data: UserAuth, uow: AbstractUnitOfWork) -> User:
    with uow:
        user = uow.users.get_by_email(user_data.email)
        if user and utils.verify_password(user_data.password, user.password):
            return user
        else:
            raise Exception()
