from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException

from core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from core.jwt import create_access_token
from apps.token.schemas import TokenData, Token, LoginForm
from apps.token.services import authenticate_user

router = APIRouter()


@router.post(path='/token', response_model=Token, status_code=200)
async def get_access_token(item: LoginForm):
    """ Create access token """

    user = await authenticate_user(**item.dict())
    if user is None:
        raise HTTPException(status_code=404, detail='User does not exist')
    else:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={'user_id': user['id']}, expires_delta=access_token_expires)
        return {'access_token': access_token, 'token_type': 'Bearer'}
