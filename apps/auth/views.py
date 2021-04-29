from fastapi import APIRouter, Request

from apps.auth.schemas import Token, LoginForm
from apps.auth.config import social_auth, redirect_uri

from apps.social_account.schemas import SocialAccountCreate, SocialAccountEmail
from apps.social_account.services import (
    update_social_account,
    check_exist_social_auth_account,
    create_social_auth_account,
)

from apps.token.services import authenticate_user, create_access_token
from apps.user.services import user_verification

auth_router = APIRouter()


@auth_router.post(path='/login', response_model=Token, status_code=200)
async def get_access_token(item: LoginForm):
    """ Create access token """

    user = await authenticate_user(**item.dict())
    data = create_access_token(data={'user_id': user['id']})
    return data


@auth_router.get('/github')
async def login_oauth(request: Request):
    """ Connect to git and redirect for authorize """

    github = social_auth.create_client('github')
    return await github.authorize_redirect(request, redirect_uri)


@auth_router.get('/github_login', status_code=201, response_model=None)
async def git_hub_login(request: Request):
    """ Authorize user using github """

    token = await social_auth.github.authorize_access_token(request)
    response = await social_auth.github.get('user', token=token)
    profile = response.json()
    serializer_profile = SocialAccountCreate(
        account_id=profile['id'],
        username=profile['login'],
        provider='github'
    )
    account = await check_exist_social_auth_account(username=profile['login'], account_id=profile['id'])
    if account:
        return create_access_token(data={'user_id': account['user']})
    if not account:
        account = await create_social_auth_account(item=serializer_profile)
        return {
            'email': 'enter the email to continue or if you already have account enter email using in this account',
            'id': account.get('id')
        }


@auth_router.get(path='/verification/{u}/{pk}', response_model=None, status_code=200)
async def verification_user(u: str, pk: int):
    """ Verification user """

    await user_verification(u=u, pk=pk)
    return {'detail': 'User has been activate'}


@auth_router.post('/github_verification/{pk}', response_model=None)
async def git_hub_verification_account(request: Request, pk: int, item: SocialAccountEmail):
    """ Verification email in github account """

    response = await update_social_account(request_dict=dict(request), pk=pk, item_dict=item.dict())
    if response:
        return create_access_token(data=response)
    else:
        return {'email': 'Check your email'}
