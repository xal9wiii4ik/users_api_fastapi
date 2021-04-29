from fastapi import APIRouter

from apps.user.views import user_router
from apps.auth.views import auth_router

routers = APIRouter()

routers.include_router(user_router, prefix='')
routers.include_router(auth_router, prefix='/auth')
