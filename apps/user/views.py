from fastapi import APIRouter, Depends, HTTPException

from apps.token.services import authenticate
from apps.user.schemas import UserBaseInDb, UserCreate, UserInDb
from apps.user.services import user_create, get_user, user_update, user_delete

router = APIRouter()


@router.post(path='/user', response_model=UserInDb, status_code=201)
async def create_user(item: UserCreate):
    """ Create user """

    return await user_create(item=item)


@router.get(path='/user/{pk}', response_model=UserInDb, status_code=200)
async def get_user_me(pk: int, user: dict = Depends(authenticate)):
    """ Get my profile """

    current_user = await get_user(pk=pk)
    if current_user is not None:
        if user is not None and user.get('id') == current_user['id']:
            return current_user
        raise HTTPException(status_code=403, detail='You have not permissions')
    raise HTTPException(status_code=404, detail='User not found')


@router.put(path='/user/{pk}', response_model=UserInDb, status_code=200)
async def update_user(pk: int, item: UserBaseInDb, user: dict = Depends(authenticate)):
    """ Update my profile """

    current_user = await get_user(pk=pk)
    if current_user is not None:
        if user is not None and user.get('id') == current_user['id']:
            current_user.update(**item.dict())
            await user_update(item=item, pk=pk)
            return UserInDb(**current_user)
        raise HTTPException(status_code=403, detail='You have not permissions')
    raise HTTPException(status_code=404, detail='User not found')


@router.delete(path='/user/{pk}', response_model=None, status_code=204)
async def delete_user(pk: int, user: dict = Depends(authenticate)):
    """ Delete my profile """

    current_user = await get_user(pk=pk)
    if current_user is not None:
        if user is not None and user.get('id') == current_user['id']:
            await user_delete(pk=pk)
            return {}
        raise HTTPException(status_code=403, detail='You have not permissions')
    raise HTTPException(status_code=404, detail='User not found')
