from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.database.core import Base
from src.database.mixin_models import TimeStampedModel


class Bookmark(Base, TimeStampedModel):
    __tablename__ = 'bookmarks'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    user = relationship('User', backref='bookmarks')
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'))
    post = relationship('Post')
