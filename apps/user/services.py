from fastapi import HTTPException

from typing import Optional

from core.security import get_hashed_password
from db.db import database

from apps.auth.services import get_web_url, create_uuid, send_email
from apps.auth.models import uid
from apps.user.models import users
from apps.user.schemas import UserCreate, UserInDb


async def get_user_from_email(email: str) -> dict or None:
    """ Getting user using email """

    query = users.select().where(users.c.email == email)
    user = await database.fetch_one(query=query)
    if user is not None:
        return dict(user)
    else:
        return None


async def create_super_user(item: dict) -> bool:
    """ Check if user already exist and creating superuser """

    item = await _validate_password(item=item)
    query = users.select().where(users.c.email == item.get('email'))
    user = await database.fetch_one(query=query)
    if user is None:
        query = users.select().where(users.c.username == item.get('username'))
        user = await database.fetch_one(query=query)
        if user is None:
            item['is_active'], item['is_superuser'] = True, True
            query = users.insert().values(**item)
            await database.execute(query=query)
    return True


async def user_create(request_dict: dict, item: UserCreate, additional_text: Optional[str] = '') -> dict:
    """ Creating user """

    url = await get_web_url(request_dict=request_dict)
    item_dict = await _validate_password(item=item.dict())
    item_dict.update({'is_active': False, 'is_superuser': False})
    query = users.insert().values(**item_dict)
    try:
        pk = await database.execute(query=query)
        item_dict.update({'id': pk})
    except Exception as e:
        raise HTTPException(status_code=404, detail=e.detail)
    uid_items = await create_uuid(user_id=pk)
    await send_email(
        title='This is your verification link:',
        link=f'{url}/verification/{uid_items["uid"]}/{uid_items["pk"]}',
        email=item_dict.get('email'),
        additional_text=additional_text
    )
    return item_dict


async def user_verification(u: str, pk: int) -> None:
    """ Set is_active to true """

    query = uid.select().where(uid.c.id == pk)
    true_uuid = await database.fetch_one(query=query)
    if true_uuid is not None:
        true_uuid = dict(true_uuid)
        if true_uuid['uid'] == u:
            query = users.update().where(users.c.id == true_uuid['user']).values(**{'is_active': True})
            await database.execute(query=query)
            query = uid.delete().where(uid.c.id == pk)
            await database.execute(query=query)


async def user_update(pk: int, item: UserInDb) -> dict:
    """ Update user profile"""

    item_dict = item.dict()
    item_dict['id'] = pk
    if item_dict['password'] is not None:
        item_dict.update({'hashed_password': get_hashed_password(password=item_dict['password'])})
    item_dict.pop('password')
    if item_dict['email'] is None:
        item_dict.pop('email')
    query = users.update().where(users.c.id == pk).values(**item_dict)
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


async def _validate_password(item: dict) -> dict:
    """ Validate password and return dict with hashed password """

    password = item.pop('password')
    repeat_password = item.pop('repeat_password')
    if password == repeat_password:
        item.update({'hashed_password': get_hashed_password(password=password)})
        return item
    raise HTTPException(status_code=404, detail='The password and the repeat password didnt match')
