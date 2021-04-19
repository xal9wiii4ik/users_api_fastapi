from core.security import get_hashed_password
from db.db import database
from apps.user.models import users
from apps.user.schemas import UserCreate, UserBaseInDb


async def user_create(item: UserCreate) -> dict:
    """ Creating user """

    item_dict = item.dict()
    password = item_dict.pop('password')
    repeat_password = item_dict.pop('repeat_password')
    if password == repeat_password:
        item_dict.update({'hashed_password': get_hashed_password(password=password)})
    query = users.insert().values(**item_dict)
    pk = await database.execute(query=query)
    item_dict.update({'id': pk})
    return item_dict


async def user_update(pk: int, item: UserBaseInDb) -> dict:
    """ Update user profile"""

    query = users.update().where(users.c.id == pk).values(**item.dict())
    return await database.execute(query=query)


async def user_delete(pk: int) -> dict:
    """ Delete user profile"""

    query = users.delete().where(users.c.id == pk)
    return await database.execute(query=query)


async def get_user(pk: int) -> dict or None:
    """ Getting user """

    query = users.select().where(users.c.id == pk)
    user = await database.fetch_one(query=query)
    if user is not None:
        return dict(user)
    else:
        return None
