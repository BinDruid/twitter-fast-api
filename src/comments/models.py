from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database.core import Base
from src.database.mixin_models import TimeStampedModel


class Comment(Base, TimeStampedModel):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    author = relationship('User', backref='comments')
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'))
    post = relationship('Post', backref='comments')
    content = Column(String, nullable=False)
