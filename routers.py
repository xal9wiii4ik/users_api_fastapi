from fastapi import APIRouter

from apps.user import views


routers = APIRouter()

routers.include_router(views.router, prefix='/blog')
