from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    """ Base schema for model User """

    email: str
    username: str


class UserBaseInDb(UserBase):
    """ Second base schema for user for create/update """

    class Config:
        orm_mode = True


class UserInDb(UserBase):
    """ Schema for user in db """

    id: Optional[int] = None
    password: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = True


class UserCreate(UserBaseInDb):
    """ Schema for creating user """

    password: str
    repeat_password: str


class SocialAccountCreate(BaseModel):
    """ Schema for creating social account"""

    account_id: int
    username: str
    email: Optional[str] = None
    provider: str


class SocialAccountShow(SocialAccountCreate):
    """ Schema for display social account"""

    id: int


class SocialAccountEmail(BaseModel):
    """ Schema for updating social account (email) """

    email: str
