from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from api.database.base_models import TimeStampedModel
from api.database.configs import Base


class Bookmark(Base, TimeStampedModel):
    __tablename__ = 'bookmarks'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User', backref='bookmarks')
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)
    post = relationship('Post')
