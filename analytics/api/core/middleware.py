from fastapi import HTTPException, status
from fastapi.responses import JSONResponse, Response
from pydantic import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request

from api.core.config import settings

from .logging import logger


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
