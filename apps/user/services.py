from core.security import get_hashed_password
from db.db import database
from apps.user.models import users
from apps.user.schemas import UserCreate


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
