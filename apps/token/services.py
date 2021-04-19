from datetime import timedelta, datetime

import jwt

from fastapi import Request
from db.db import database
from apps.user.models import users
from core.config import (
    SECRET_KEY,
    TOKEN_TYPE,
    ALGORITHM,
    ACCESS_TOKEN_JWT_SUBJECT,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from core.security import verify_password


async def authenticate_user(password: str, username: str = None, email: str = None) -> dict or None:
    """ Authenticate user """

    user = await _get_user(username=username, email=email)
    if user is None:
        return None
    else:
        if verify_password(plain_password=password, hashed_password=user['hashed_password']):
            return user
        else:
            return None


async def authenticate(request: Request) -> dict or None:
    """ Authenticate user """

    token = request.headers.get("Authorization").split(' ')
    if (token != '') and (token is not None) and (token[0] == TOKEN_TYPE):
        payload = jwt.decode(token[1], SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get('user_id')
        query = users.select().where(users.c.id == user_id)
        user = await database.fetch_one(query=query)
        if user is not None:
            return dict(user)
    return None


def create_access_token(data: dict):
    """ Create access token """

    to_encode = data.copy()
    if ACCESS_TOKEN_EXPIRE_MINUTES is not None:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire, 'sub': ACCESS_TOKEN_JWT_SUBJECT})
    encoded_jwt = jwt.encode(payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    data.update({'access_token': encoded_jwt, 'token_type': TOKEN_TYPE})
    return data


async def _get_user(username: str = None, email: str = None) -> dict or None:
    """ Get user from db """

    if username is None:
        query = users.select().where(users.c.email == email)
    else:
        query = users.select().where(users.c.username == username)
    user = await database.fetch_one(query=query)
    if user is None:
        return None
    else:
        return dict(user)
