from typing import Optional

from pydantic import field_validator
from pydantic.networks import EmailStr
from sqlalchemy import Boolean, CheckConstraint, Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from twitter_api.core.pagination import Pagination
from twitter_api.database import Base, PydanticBase, TimeStampedModel

from .auth import hash_password


class User(Base, TimeStampedModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(32), unique=True, index=True)
    first_name = Column(String(256), nullable=True)
    last_name = Column(String(256), nullable=True)
    email = Column(String(256), nullable=False, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    password = Column(String(128), nullable=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Followership(Base, TimeStampedModel):
    __tablename__ = 'followerships'
    __table_args__ = (
        CheckConstraint('follower_id <> following_id', name='user_can_not_follow_themself'),
        UniqueConstraint('following_id', 'follower_id', name='unique_followership_relations'),
    )
    id = Column(Integer, primary_key=True)
    following_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    follower_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    following = relationship('User', foreign_keys='Followership.following_id')
    follower = relationship('User', foreign_keys='Followership.follower_id')

    def __str__(self):
        return f'{self.following_id}->{self.follower_id}'


class UserCreatePayload(PydanticBase):
    username: str
    email: EmailStr
    password: str

    @field_validator('password')
    @classmethod
    def make_hash(cls, password: str) -> str:
        return hash_password(password)


class UserLoginPayload(PydanticBase):
    username: str
    password: str


class UserDetail(PydanticBase):
    id: int
    username: str
    email: EmailStr
    first_name: Optional[str] = ''
    last_name: Optional[str] = ''


class UserList(Pagination):
    items: list[UserDetail] = []


class FollowerShipPayload(PydanticBase):
    user_id: int
