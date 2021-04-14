from fastapi import FastAPI

from db.db import database
from routers import routers
from starlette.requests import Request
from starlette.responses import Response


app = FastAPI()


@app.on_event('startup')
async def startup():
    """Connect to database when server starting"""

    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    """Connect to database when server stopping"""

    await database.disconnect()


# @app.middleware("http")
# async def db_session_middleware(request: Request, call_next):
#     response = Response("Internal server error", status_code=500)
#     try:
#         request.state.db = SessionLocal()
#         response = await call_next(request)
#     finally:
#         request.state.db.close()
#     return response

app.include_router(routers)

# uvicorn main:app --reload  -  start server
# pip install fastapi\[all\]
# Alembic: alembic init migrations(add file)
# Alembic: alembic revision --autogenerate -m 'commit'
# Alembic: alembic upgrade head -> migrate
