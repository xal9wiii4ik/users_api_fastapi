from apps.social_account.models import social_accounts
from apps.social_account.schemas import SocialAccountCreate

from apps.user.services import get_user_from_email, user_create
from apps.user.schemas import UserCreate

from db.db import database


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
