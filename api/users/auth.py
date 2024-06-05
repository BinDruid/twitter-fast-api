from typing import Annotated

from fastapi import Depends, HTTPException
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

from api.core.middleware import AuthenticatedUser


def get_current_user(request: Request) -> AuthenticatedUser:
    if request.state.user.is_anonymous:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=[{'msg': 'Not Authorized'}],
        )
    return request.state.user


CurrentUser = Annotated[AuthenticatedUser, Depends(get_current_user)]

InvalidCredentialException = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED, detail=[{'msg': 'Could not validate credentials'}]
)
