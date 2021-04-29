from fastapi import APIRouter, Depends, Request

from apps.user.permissions import get_current_active_user
from apps.user.schemas import UserBaseInDb, UserCreate, UserInDb
from apps.user.services import (
    user_create,
    user_delete,
    user_update,
)

user_router = APIRouter()


@user_router.post(path='/user', response_model=UserInDb, status_code=201)
async def create_user(request: Request, item: UserCreate):
    """ Create user """

    return await user_create(request_dict=dict(request), item=item)


@user_router.get(path='/user/{pk}', response_model=UserInDb, status_code=200)
async def get_user_me(pk: int, user: dict = Depends(get_current_active_user)):
    """ Get my profile """

    if user is not None:
        return user


@user_router.put(path='/user/{pk}', response_model=UserBaseInDb, status_code=200)
async def update_user(pk: int, item: UserInDb, user: dict = Depends(get_current_active_user)):
    """ Update my profile """

    if user is not None:
        user.update(**item.dict())
        await user_update(item=item, pk=pk)
        return UserInDb(**user)


@user_router.delete(path='/user/{pk}', response_model=None, status_code=204)
async def delete_user(pk: int, user: dict = Depends(get_current_active_user)):
    """ Delete my profile """

    if user is not None:
        await user_delete(pk=pk)
        return {}
