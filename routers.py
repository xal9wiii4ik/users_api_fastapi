from fastapi import APIRouter

from apps.user import views as user_view
from apps.token import views as token_views

routers = APIRouter()

routers.include_router(user_view.router, prefix='')
routers.include_router(token_views.router, prefix='')
