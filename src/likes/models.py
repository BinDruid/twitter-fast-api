from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database.core import Base
from src.database.mixin_models import TimeStampedModel


class Like(Base, TimeStampedModel):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User', backref='likes')
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)
    post = relationship('Post', backref='likes')

    def __str__(self):
        return f'{self.user_id}#{self.id}'
