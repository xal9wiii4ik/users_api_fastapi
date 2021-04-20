from fastapi import APIRouter, Depends

from apps.user.permissions import get_current_active_user
from apps.user.schemas import UserBaseInDb, UserCreate, UserInDb
from apps.user.services import user_create, user_delete, user_update, user_verification

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


@router.put(path='/user/{pk}', response_model=UserInDb, status_code=200)
async def update_user(pk: int, item: UserBaseInDb, user: dict = Depends(get_current_active_user)):
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
