from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from apps.user.models import User
from db.base_model_class import Base


class SocialAccount(Base):
    """ Model for social account """

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer)
    username = Column(String)
    email = Column(String, nullable=True)
    provider = Column(String)
    user = Column(Integer, ForeignKey('user.id'), nullable=True)
    user_id = relationship(User)


social_accounts = SocialAccount.__table__
