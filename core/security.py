from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password: str, hashed_password: str):
    """ Verify user password """

    return pwd_context.verify(secret=plain_password, hash=hashed_password)


def get_hashed_password(password: str):
    """ Get hash password """

    return pwd_context.hash(secret=password)
