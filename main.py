from fastapi import FastAPI

from db.db import database
from routers import routers

app = FastAPI()


@app.on_event('startup')
async def startup():
    """Connect to database when server starting"""

    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    """Connect to database when server stopping"""

    await database.disconnect()


app.include_router(routers)
