from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from apps.social_account.models import SocialAccount
from apps.user.models import User
from db.base_model_class import Base


class Uid(Base):
    """Model uid for future verification of user"""

    id = Column(Integer, primary_key=True)
    uid = Column(String)
    user = Column(Integer, ForeignKey('user.id'), nullable=True, unique=True)
    user_id = relationship(User)
    social_user = Column(Integer, ForeignKey('user.id'), nullable=True, unique=True)
    social_user_id = relationship(SocialAccount)


uid = Uid.__table__
