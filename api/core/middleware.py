import datetime

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse, Response
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from jose.exceptions import JWKError
from pydantic import BaseModel, ValidationError
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request

from api.core.config import settings

from .logging import logger


class AnonymousUser:
    id = None
    username = None

    @property
    def is_authenticated(self):
        return False

    @property
    def is_anonymous(self):
        return True


class AuthenticatedUser(BaseModel):
    id: int
    username: str

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False


class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        authorization: str = request.headers.get('Authorization')
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != 'bearer':
            logger.info(
                f'Malformed authorization header. Scheme: {scheme} Param: {param} Authorization: {authorization}'
            )
            request.state.user = AnonymousUser()
            response = await call_next(request)
            return response
        token = authorization.split()[1]
        try:
            data = jwt.decode(token, settings.JWT_SECRET)
            request.state.user = AuthenticatedUser(id=data['id'], username=data['username'])
        except (JWKError, JWTError):
            request.state.user = AnonymousUser()
        response = await call_next(request)
        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = datetime.datetime.utcnow()
        method_name = request.method.upper()
        url = request.url
        user = request.state.user.id
        with open(f'{settings.PATHS.ROOT_DIR}/logs/requests.log', mode='a') as request_logs:
            log_message = f'[{start_time}] [User #{user}] [{method_name}] {url}\n'
            request_logs.write(log_message)
        response = await call_next(request)
        process_time = datetime.datetime.utcnow() - start_time
        response.headers['X-Process-Time'] = str(process_time)
        return response


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> JSONResponse:
        try:
            response = await call_next(request)
        except HTTPException as http_exception:
            response = JSONResponse(
                status_code=http_exception.status_code, content={'detail': str(http_exception.detail)}
            )
        except ValidationError as e:
            response = JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={'detail': e.errors()})
        except Exception as e:  # noqa
            logger.exception(e)
            content = {'detail': [{'msg': 'Unknown', 'loc': ['Unknown'], 'type': 'Unknown'}]}
            if settings.DEBUG:
                content = {'detail': [{'error': e.__class__.__name__, 'mgs': e.args}]}
            response = JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=content)
        return response
