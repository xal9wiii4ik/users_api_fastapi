import os
import py_env

SECRET_KEY = py_env.SECRET_KEY

# Token 60 minutes * 24 hours * 8 days = 8 days
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{py_env.POSTGRES_USER}:{py_env.POSTGRES_PASSWORD}@{py_env.POSTGRES_SERVER}/{py_env.POSTGRES_DB}"
)

USERS_OPEN_REGISTRATION = True

# ''.join(secrets.choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50))
