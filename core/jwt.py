import jwt

from datetime import datetime, timedelta

from core import config

ALGORITHM = 'HS256'
access_token_jwt_subject = 'access'


def create_access_token(data: dict, expires_delta: timedelta = None):
    """ Create access token """

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire, 'sub': access_token_jwt_subject})
    encoded_jwt = jwt.encode(payload=to_encode, key=config.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
