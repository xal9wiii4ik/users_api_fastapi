from fastapi import APIRouter, HTTPException, BackgroundTasks, Body, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from apps.token.schemas import Token, LoginForm
from apps.token.services import authenticate_user, create_access_token

from .config import social_auth, redirect_uri
from ..user.schemas import SocialAuthCreate, SocialAuthShow
from ..user.services import create_social_auth_account, check_exist_social_auth_account

auth_router = APIRouter()


@auth_router.post(path='/login', response_model=Token, status_code=200)
async def get_access_token(item: LoginForm):
    """ Create access token """

    user = await authenticate_user(**item.dict())
    if user is None:
        raise HTTPException(status_code=404, detail='User does not exist')
    else:
        data = create_access_token(data={'user_id': user['id']})
        return data


@auth_router.get('/')
async def login_oauth(request: Request):
    github = social_auth.create_client('github')
    return await github.authorize_redirect(request, redirect_uri)


@auth_router.get('/github_login', response_model=SocialAuthShow)
async def authorize(request: Request):
    token = await social_auth.github.authorize_access_token(request)
    response = await social_auth.github.get('user', token=token)
    profile = response.json()
    serializer_profile = SocialAuthCreate(
        account_id=profile['id'],
        username=profile['login'],
        provider='github'
    )
    await check_exist_social_auth_account(username=profile['login'], account_id=profile['id'])
    profile = await create_social_auth_account(item=serializer_profile)
    return profile

# TODO move create social user to new func
# TODO create func for verificate email and add user to social auth
