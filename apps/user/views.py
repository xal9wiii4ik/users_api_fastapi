from fastapi import APIRouter, Depends

from apps.token.services import create_access_token
from apps.user.permissions import get_current_active_user
from apps.user.schemas import UserBaseInDb, UserCreate, UserInDb, SocialAccountEmail
from apps.user.services import (
    user_create,
    user_delete,
    user_update,
    user_verification,
    update_social_account,
)

router = APIRouter()


@router.post(path='/user', response_model=UserInDb, status_code=201)
async def create_user(item: UserCreate):
    """ Create user """

    return await user_create(item=item)


@router.get(path='/user/{pk}', response_model=UserInDb, status_code=200)
async def get_user_me(pk: int, user: dict = Depends(get_current_active_user)):
    """ Get my profile """

    if user is not None:
        return user


@router.put(path='/user/{pk}', response_model=UserBaseInDb, status_code=200)
async def update_user(pk: int, item: UserInDb, user: dict = Depends(get_current_active_user)):
    """ Update my profile """

    if user is not None:
        user.update(**item.dict())
        await user_update(item=item, pk=pk)
        return UserInDb(**user)


@router.delete(path='/user/{pk}', response_model=None, status_code=204)
async def delete_user(pk: int, user: dict = Depends(get_current_active_user)):
    """ Delete my profile """

    if user is not None:
        await user_delete(pk=pk)
        return {}


@router.get(path='/verification/{pk}', response_model=None, status_code=200)
async def verification_user(pk: int):
    """ Verification user """

    await user_verification(pk=pk)
    return {'detail': 'User has been activate'}


@router.post('/github_verification/{pk}', response_model=None)
async def git_hub_verification_account(pk: int, item: SocialAccountEmail):
    response = await update_social_account(pk=pk, item_dict=item.dict())
    if response:
        return create_access_token(data=response)
    else:
        return {'email': 'Check your email'}
