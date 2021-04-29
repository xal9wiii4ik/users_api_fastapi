from typing import Optional

from pydantic import BaseModel


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
