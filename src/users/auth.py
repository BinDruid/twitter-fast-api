from collections import namedtuple
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from jose.exceptions import JWKError
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

from src.core.config import settings
from src.core.logging import logger
from src.users.models import User

UserInfo = namedtuple('UserInfo', ['id', 'username'])


def get_current_user(request: Request) -> UserInfo:
    authorization: str = request.headers.get('Authorization')
    scheme, param = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != 'bearer':
        logger.exception(
            f'Malformed authorization header. Scheme: {scheme} Param: {param} Authorization: {authorization}'
        )
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=[{'msg': 'Not Authorized'}],
        ) from None

    token = authorization.split()[1]

    try:
        data = jwt.decode(token, settings.JWT_SECRET)
    except (JWKError, JWTError):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=[{'msg': 'Could not validate credentials'}],
        ) from None
    return UserInfo(data['id'], data['username'])


CurrentUser = Annotated[User, Depends(get_current_user)]

InvalidCredentialException = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED, detail=[{'msg': 'Could not validate credentials'}]
)
