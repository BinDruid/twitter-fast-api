from sqlalchemy import Column, Integer, UniqueConstraint

from api.database import Base, TimeStampedModel


class View(Base, TimeStampedModel):
    __tablename__ = 'views'
    __table_args__ = (UniqueConstraint('post_id', name='unique_view_for_post_relations'),)

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, unique=True, index=True, nullable=False)
    count = Column(Integer, default=0)
