from core import py_env

SECRET_KEY = py_env.SECRET_KEY

# Token 60 minutes * 24 hours * 8 days = 8 days
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{py_env.POSTGRES_USER}:{py_env.POSTGRES_PASSWORD}@{py_env.POSTGRES_SERVER}/{py_env.POSTGRES_DB}"
)

TOKEN_TYPE = py_env.TOKEN_TYPE
ALGORITHM = py_env.ALGORITHM
ACCESS_TOKEN_JWT_SUBJECT = py_env.ACCESS_TOKEN_JWT_SUBJECT

EMAIL_HOST = py_env.EMAIL_HOST
EMAIL_HOST_PASSWORD = py_env.EMAIL_HOST_PASSWORD
EMAIL_HOST_USER = py_env.EMAIL_HOST_USER
EMAIL_PORT = py_env.EMAIL_PORT
EMAIL_USE_TLS = py_env.EMAIL_USE_TLS
EMAIL_USERNAME = py_env.EMAIL_USERNAME

# ''.join(secrets.choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50))
