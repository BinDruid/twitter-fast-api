import datetime

import bcrypt
from jose import jwt

from twitter_api.core.config import settings


def generate_token(*, user) -> str:
    now = datetime.datetime.utcnow()
    exp = (now + datetime.timedelta(seconds=settings.JWT_EXP)).timestamp()
    data = {'exp': exp, 'username': user.username, 'id': user.id}
    return jwt.encode(data, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


def hash_password(password: str) -> str:
    pw = bytes(password, 'utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt).decode('utf-8')


def check_password(*, user, password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
