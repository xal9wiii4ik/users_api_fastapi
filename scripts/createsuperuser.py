import os
import sys
import asyncio

from fastapi import HTTPException

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from apps.user.services import create_super_user
from apps.user.schemas import UserCreate
from core.config import (
    USERNAME_SUPERUSER,
    EMAIL_SUPERUSER,
    PASSWORD_SUPERUSER,
    REPEAT_PASSWORD_SUPERUSER,
)


async def main():
    """ Getting data from terminal """

    await database.connect()
    print('Creating super user')
    username = input('Username (default xal9): ')
    if username == '':
        username = USERNAME_SUPERUSER
    email = input('email: ')
    if email == '':
        email = EMAIL_SUPERUSER
    password = input('password: ')
    if password == '':
        password = PASSWORD_SUPERUSER
    repeat_password = input('repeat_password: ')
    if repeat_password == '':
        repeat_password = REPEAT_PASSWORD_SUPERUSER
    item = UserCreate(
        username=username,
        email=email,
        password=password,
        repeat_password=repeat_password)
    try:
        await create_super_user(item=item.dict())
    except HTTPException as e:
        print(e.detail)
    await database.disconnect()


if __name__ == '__main__':
    from db.db import database

    asyncio.get_event_loop()
    asyncio.run(main=main())
