from typing import Annotated

from fastapi import Depends, HTTPException
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

from src.core.middleware import AuthenticatedUser
from src.users.models import User


def get_current_user(request: Request) -> AuthenticatedUser:
    if request.state.user.is_anonymous:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=[{'msg': 'Not Authorized'}],
        )
    return request.state.user


CurrentUser = Annotated[User, Depends(get_current_user)]

InvalidCredentialException = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED, detail=[{'msg': 'Could not validate credentials'}]
)
