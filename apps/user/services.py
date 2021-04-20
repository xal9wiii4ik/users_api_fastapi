import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import HTTPException

from core.security import get_hashed_password
from db.db import database
from apps.user.models import users
from apps.user.schemas import UserCreate, UserInDb

from core.config import (
    EMAIL_HOST,
    EMAIL_HOST_PASSWORD,
    EMAIL_PORT,
    EMAIL_USERNAME,
)


async def user_create(item: UserCreate) -> dict:
    """ Creating user """

    item_dict = item.dict()
    password = item_dict.pop('password')
    repeat_password = item_dict.pop('repeat_password')
    if password == repeat_password:
        item_dict.update({'hashed_password': get_hashed_password(password=password)})
    query = users.insert().values(**item_dict)
    try:
        pk = await database.execute(query=query)
        item_dict.update({'id': pk})
    except Exception as e:
        raise HTTPException(status_code=404, detail=e.detail)

    server = smtplib.SMTP(host=EMAIL_HOST, port=EMAIL_PORT)
    server.starttls()
    server.login(user=EMAIL_USERNAME, password=EMAIL_HOST_PASSWORD)
    message = MIMEMultipart('alternative')
    text = "Hi!"
    html = f"""\
    <h1 style="color:red;">This is your verification link:<h1>
    <h3>http://127.0.0.1:8000/verification/{pk}/<h3>
    """
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    message['Subject'] = 'Verification user'
    message.attach(part1)
    message.attach(part2)
    server.sendmail(from_addr=EMAIL_USERNAME, to_addrs=item_dict.get('email'), msg=message.as_string())
    server.quit()
    return item_dict


async def user_verification(pk: int) -> None:
    """ Set is_active to true """

    query = users.update().where(users.c.id == pk).values(**{'is_active': True})
    return await database.execute(query=query)


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
