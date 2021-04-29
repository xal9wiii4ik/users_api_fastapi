import smtplib
import uuid

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

from fastapi import HTTPException

from apps.token.models import uid
from core.security import get_hashed_password
from db.db import database
from apps.user.models import users, social_accounts
from apps.user.schemas import UserCreate, UserInDb, SocialAccountCreate

from core.config import (
    EMAIL_HOST,
    EMAIL_HOST_PASSWORD,
    EMAIL_PORT,
    EMAIL_USERNAME,
)


async def get_user_from_email(email: str) -> dict or None:
    """ Getting user using email """

    query = users.select().where(users.c.email == email)
    user = await database.fetch_one(query=query)
    if user is not None:
        return dict(user)
    else:
        return None


async def update_social_account(request_dict: dict, pk: int, item_dict: dict) -> bool or dict:
    """ Getting social account using email """

    user = await get_user_from_email(email=item_dict.get('email'))
    is_new_user = False
    if user is None:
        is_new_user = True
        query = social_accounts.select().where(social_accounts.c.id == pk)
        account = dict(await database.fetch_one(query=query))
        password = f'{account["account_id"]}_{account["provider"]}/{account["id"]}'
        new_dict = UserCreate(
            password=password,
            repeat_password=password,
            email=item_dict['email'],
            username=account['username']
        )
        user = await user_create(
            request_dict=request_dict,
            item=new_dict,
            additional_text=f'Your password is: {password}. '
                            f'That is if you want to login with password (username: {account["username"]})'
        )
    item_dict.update({'user': user['id']})
    query = social_accounts.update().where(social_accounts.c.id == pk).values(**item_dict)
    await database.execute(query=query)
    if not is_new_user:
        return {'user_id': user['id']}
    return False


async def create_social_auth_account(item: SocialAccountCreate) -> dict:
    """ Creating social auth account with out relation with user"""

    item_dict = item.dict()
    query = social_accounts.insert().values(**item_dict)
    pk = await database.execute(query=query)
    item_dict.update({'id': pk})
    return item_dict


async def check_exist_social_auth_account(username: str, account_id: int) -> dict or bool:
    """ Check if social auth account exist in db"""

    query = social_accounts.select().where(social_accounts.c.username == username).where(
        social_accounts.c.account_id == account_id)
    account = await database.fetch_one(query=query)
    if account:
        return dict(account)
    return False


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


async def send_email(title: str, link: str, email: str, additional_text: str):
    """ Sending email to user """

    # TODO protocol = 'https://' if is_secure else 'http://'
    #     web_url = protocol + host
    #     return web_url + url
    server = smtplib.SMTP(host=EMAIL_HOST, port=EMAIL_PORT)
    server.starttls()
    server.login(user=EMAIL_USERNAME, password=EMAIL_HOST_PASSWORD)
    message = MIMEMultipart('alternative')
    text = "Hi!"
    html = f"""\
        <h1 style="color:red;">{title}</h1><h3>{link}</h3><h3>{additional_text}</h3>
        """
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    message['Subject'] = 'Verification user'
    message.attach(part1)
    message.attach(part2)
    server.sendmail(from_addr=EMAIL_USERNAME, to_addrs=email, msg=message.as_string())
    server.quit()


async def _get_web_url(request_dict: dict) -> str:
    """ Build url for emails """

    return f'{request_dict["scheme"]}://{request_dict["server"][0]}:{request_dict["server"][1]}'


async def _create_uuid(user_id: Optional[int] = None, social_user_id: Optional[int] = None) -> dict:
    """ Creating uuid and write in db """

    items = {
        'uid': uuid.uuid4().hex
    }
    if user_id is not None:
        items.update({'user': user_id})
    if social_user_id is not None:
        items.update(({'social_user': social_user_id}))
    query = uid.insert().values(**items)
    try:
        pk = await database.execute(query=query)
        items.update({'pk': pk})
        return items
    except Exception as e:
        raise HTTPException(status_code=404, detail=e.detail)


async def user_create(request_dict: dict, item: UserCreate, additional_text: Optional[str] = '') -> dict:
    """ Creating user """

    url = await _get_web_url(request_dict=request_dict)
    item_dict = await _validate_password(item=item.dict())
    item_dict.update({'is_active': False, 'is_superuser': False})
    query = users.insert().values(**item_dict)
    try:
        pk = await database.execute(query=query)
        item_dict.update({'id': pk})
    except Exception as e:
        raise HTTPException(status_code=404, detail=e.detail)
    uid_items = await _create_uuid(user_id=pk)
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
