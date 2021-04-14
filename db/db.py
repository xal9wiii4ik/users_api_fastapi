import databases

from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URL = "postgresql://django_user:1234567816@localhost/micro_blog"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_some_tread': False}
)
database = databases.Database(SQLALCHEMY_DATABASE_URL)
