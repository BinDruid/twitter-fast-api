from __future__ import annotations

from datetime import datetime, timedelta

import bcrypt
from jose import jwt
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model

from src.core.config import settings
from src.database.mixin_models import TimeStampedModel


def hash_password(password: str):
    """Generates a hashed version of the provided password."""
    pw = bytes(password, 'utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)


class User(TimeStampedModel, Model):
    id = fields.IntField(primary_key=True)
    first_name = fields.CharField(max_length=32, null=True)
    last_name = fields.CharField(max_length=32, null=True)
    email = fields.CharField(max_length=254, unique=True)
    password = fields.CharField(max_length=128)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def token(self):
        now = datetime.utcnow()
        exp = (now + timedelta(seconds=settings.JWT_EXP)).timestamp()
        data = {
            'exp': exp,
            'email': self.email,
        }
        return jwt.encode(data, settings.JWT_SECRET, algorithm=settings.JWT_ALG)

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))


UserPydanticIn = pydantic_model_creator(User, name='User', include=('email', 'first_name', 'last_name', 'password'))
UserPydanticAuth = pydantic_model_creator(User, name='UserAuth', include=('email', 'password'))
UserPydanticOut = pydantic_model_creator(User, name='UserOut', include=('id', 'email', 'created_at'))
