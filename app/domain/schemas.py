from typing import Self
from pydantic import BaseModel, EmailStr, Field, model_validator

from app.utils import get_password_hash


class EmailModel(BaseModel):
    email: EmailStr = Field()


class UserBase(EmailModel):
    first_name: str = Field(min_length=3, max_length=50)
    last_name: str = Field(min_length=3, max_length=50)


class UserRegister(UserBase):
    password: str = Field(min_length=8, max_length=50)
    confirm_password: str = Field(min_length=8, max_length=50)

    @model_validator(mode="after")
    def check_password(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError("")

        self.password = get_password_hash(self.password)
        self.confirm_password = self.password
        return self


class UserAddDB(UserBase):
    password: str = Field(min_length=8, max_length=50)


class UserAuth(EmailModel):
    password: str = Field(min_length=8, max_length=50)
