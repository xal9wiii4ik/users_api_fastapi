from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    """ Schema for token """

    access_token: str
    token_type: str


class LoginForm(BaseModel):
    """ Schema for login form """

    username: Optional[str] = None
    email: Optional[str] = None
    password: str
