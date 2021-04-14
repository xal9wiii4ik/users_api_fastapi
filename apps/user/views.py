from fastapi import APIRouter

from apps.user.schemas import UserBaseInDb, UserCreate, UserInDb
from apps.user.services import user_create

router = APIRouter()


@router.post(path='/user', response_model=UserInDb)
async def create_user(item: UserCreate):
    return await user_create(item=item)
