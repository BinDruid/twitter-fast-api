from fastapi import FastAPI

from twitter_api.core.config import app_configs
from twitter_api.core.middleware import AuthenticationMiddleware, ExceptionMiddleware, LoggingMiddleware
from twitter_api.core.startup import startup
from twitter_api.routes import api_router


def get_application() -> FastAPI:
    app = FastAPI(**app_configs)
    app.include_router(api_router)
    app.on_event('startup')(startup)
    return app


api = get_application()

api.add_middleware(LoggingMiddleware)
api.add_middleware(AuthenticationMiddleware)
api.add_middleware(ExceptionMiddleware)
