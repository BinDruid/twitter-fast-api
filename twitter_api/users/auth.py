from datetime import datetime, timedelta

import bcrypt
from fastapi import HTTPException, status
from jose import jwt

from twitter_api.core.config import settings

InvalidCredentialException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail=[{'msg': 'Could not validate credentials'}]
)


def generate_token(*, user) -> str:
    now = datetime.utcnow()
    exp = (now + timedelta(seconds=settings.JWT_EXP)).timestamp()
    data = {'exp': exp, 'username': user.username, 'id': user.id}
    return jwt.encode(data, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


def hash_password(password: str) -> str:
    pw = bytes(password, 'utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt).decode('utf-8')


def check_password(*, user, password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
