import datetime

from fastapi import status
from fastapi.responses import JSONResponse, Response
from pydantic import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from src.core.config import settings
from .logging import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = datetime.datetime.utcnow()
        method_name = request.method.upper()
        url = request.url
        query_params = request.query_params
        path_params = request.path_params
        with open(f'{settings.PATHS.ROOT_DIR}/logs/requests.log', mode='a') as request_logs:
            log_message = f'[{start_time}] [{method_name}] {url} ,query: {query_params}, path: {path_params}\n'
            request_logs.write(log_message)
        response = await call_next(request)
        process_time = datetime.datetime.utcnow() - start_time
        response.headers['X-Process-Time'] = str(process_time)
        return response


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> JSONResponse:
        try:
            response = await call_next(request)
        except ValidationError as e:
            logger.exception(e)
            response = JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={'detail': e.errors()})
        except ValueError as e:
            logger.exception(e)
            response = JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={'detail': [{'msg': 'Unknown', 'loc': ['Unknown'], 'type': 'Unknown'}]},
            )
        except Exception as e:  # noqa
            logger.exception(e)
            response = JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={'detail': [{'msg': 'Unknown', 'loc': ['Unknown'], 'type': 'Unknown'}]},
            )

        return response
