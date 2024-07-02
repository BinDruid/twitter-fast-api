from datetime import datetime
from typing import Optional

from pydantic import Field
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from twitter_api.core.pagination import Pagination
from twitter_api.database import Base, PydanticBase, TimeStampedModel


class Post(Base, TimeStampedModel):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    content = Column(String(128), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    author = relationship('User', backref='posts')
    quoted_post_id = Column(Integer, ForeignKey('posts.id'), nullable=True)
    quoted_post = relationship('Post', remote_side='Post.id')

    def __str__(self):
        return f'{self.author}#{self.id}'


class Mention(Base, TimeStampedModel):
    __tablename__ = 'mentions'

    id = Column(Integer, primary_key=True)
    mention_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    original_post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    mention = relationship('Post', foreign_keys=[mention_id])
    original_post = relationship('Post', foreign_keys=[original_post_id])


class PostPayload(PydanticBase):
    content: str = Field(max_length=128)


class PostDetail(PydanticBase):
    id: int
    content: str
    created_at: datetime
    updated_at: datetime


class PostDetailWithQuote(PostDetail):
    quoted_post: Optional[PostDetail]


class PostList(Pagination):
    items: list[PostDetail] = []


class PostWithQuoteList(Pagination):
    items: list[PostDetailWithQuote] = []
