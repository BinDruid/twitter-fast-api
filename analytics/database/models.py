from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, UniqueConstraint

from .configs import Base


class PostView(Base):
    __tablename__ = 'views'
    __table_args__ = (UniqueConstraint('post_id', name='unique_view_for_post_relations'),)

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    post_id = Column(Integer, unique=True, index=True, nullable=False)
    count = Column(Integer, default=0)
