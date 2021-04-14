from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    """ Base schema for model User """

    email: str
    is_active: Optional[bool] = False
    is_superuser: Optional[bool] = False


class UserBaseInDb(UserBase):
    """ Second base schema for user for create/update """

    class Config:
        orm_mode = True


class UserInDb(UserBase):
    """ Schema for user in db """

    id: Optional[int] = None


class UserCreate(UserBaseInDb):
    """ Schema for creating user """

    password: str
    repeat_password: str
