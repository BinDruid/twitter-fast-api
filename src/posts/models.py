from datetime import datetime

from pydantic import Field
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.core.pagination import Pagination
from src.database.core import Base, PydanticBase
from src.database.mixin_models import TimeStampedModel


class Post(Base, TimeStampedModel):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    content = Column(String(128), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    author = relationship('User', backref='posts')

    def __str__(self):
        return f'{self.author}#{self.id}'


class PostPayload(PydanticBase):
    content: str = Field(max_length=128)


class PostDetail(PydanticBase):
    id: int
    content: str
    created_at: datetime
    updated_at: datetime


class PostList(Pagination):
    items: list[PostDetail] = []
