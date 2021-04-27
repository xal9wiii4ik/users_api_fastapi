from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from db.base_model_class import Base


class User(Base):
    """ Model user """

    id = Column(Integer, primary_key=True)
    username = Column(String, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)


users = User.__table__


class SocialAuth(Base):
    """ Model for social auth """

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer)
    username = Column(String)
    email = Column(String, nullable=True)
    provider = Column(String)
    user = Column(Integer, ForeignKey('user.id'), nullable=True)
    user_id = relationship(User)


social_auth_accounts = SocialAuth.__table__
