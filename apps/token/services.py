from core.security import verify_password
from db.db import database
from apps.user.models import users


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
