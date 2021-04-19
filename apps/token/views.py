from fastapi import APIRouter, HTTPException

from apps.token.schemas import Token, LoginForm
from apps.token.services import authenticate_user, create_access_token

router = APIRouter()


@router.post(path='/token', response_model=Token, status_code=200)
async def get_access_token(item: LoginForm):
    """ Create access token """

    user = await authenticate_user(**item.dict())
    if user is None:
        raise HTTPException(status_code=404, detail='User does not exist')
    else:
        data = create_access_token(data={'user_id': user['id']})
        return data
