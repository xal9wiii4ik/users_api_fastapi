from fastapi import APIRouter

from apps.user import views as user_view
from apps.token.views import auth_router

routers = APIRouter()

routers.include_router(user_view.router, prefix='')
routers.include_router(auth_router, prefix='')
