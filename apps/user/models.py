from sqlalchemy import Column, Integer, String, Boolean

from db.base_model_class import Base


class User(Base):
    """ Model user """

    id = Column(Integer, primary_key=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)


users = User.__table__
