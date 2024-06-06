from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint

from api.database import Base, TimeStampedModel


class Like(Base, TimeStampedModel):
    __tablename__ = 'likes'
    __table_args__ = (UniqueConstraint('user_id', 'post_id', name='unique_like_for_user_post_relations'),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)


class Bookmark(Base, TimeStampedModel):
    __tablename__ = 'bookmarks'
    __table_args__ = (UniqueConstraint('user_id', 'post_id', name='unique_bookmark_for_user_post_relations'),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)


class View(Base, TimeStampedModel):
    __tablename__ = 'views'
    __table_args__ = (UniqueConstraint('post_id', name='unique_view_for_post_relations'),)

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)
    count = Column(Integer, default=0)
