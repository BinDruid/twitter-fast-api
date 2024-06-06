from datetime import datetime, timedelta
from typing import Optional

import bcrypt
from jose import jwt
from pydantic import field_validator
from pydantic.networks import EmailStr
from sqlalchemy import Boolean, CheckConstraint, Column, ForeignKey, Integer, String, UniqueConstraint

from twitter_api.core.config import settings
from twitter_api.core.pagination import Pagination
from twitter_api.database import Base, PydanticBase, TimeStampedModel


def hash_password(password: str):
    """Generates a hashed version of the provided password."""
    pw = bytes(password, 'utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)


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

    @property
    def token(self):
        now = datetime.utcnow()
        exp = (now + timedelta(seconds=settings.JWT_EXP)).timestamp()
        data = {'exp': exp, 'username': self.username, 'id': self.id}
        return jwt.encode(data, settings.JWT_SECRET, algorithm=settings.JWT_ALG)

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))


class Followership(Base, TimeStampedModel):
    __tablename__ = 'followerships'
    __table_args__ = (
        CheckConstraint('follower_id <> following_id', name='user_can_not_follow_themself'),
        UniqueConstraint('following_id', 'follower_id', name='unique_followership_relations'),
    )
    id = Column(Integer, primary_key=True)
    following_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    follower_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    def __str__(self):
        return f'{self.following_id}->{self.follower_id}'


class UserCreatePayload(PydanticBase):
    username: str
    email: EmailStr
    password: str

    @field_validator('password')
    @classmethod
    def make_hash(cls, password: str) -> str:
        hashed_password = hash_password(password)
        return hashed_password.decode('utf-8')


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
