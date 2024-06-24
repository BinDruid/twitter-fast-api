from fastapi import FastAPI

from twitter_api.core.config import app_configs
from twitter_api.core.middleware import AuthenticationMiddleware, ExceptionMiddleware, LoggingMiddleware
from twitter_api.core.startup import lifespan
from twitter_api.routes import api_router


def get_application() -> FastAPI:
    app = FastAPI(**app_configs, lifespan=lifespan)
    app.include_router(api_router)
    return app


api = get_application()

api.add_middleware(LoggingMiddleware)
api.add_middleware(AuthenticationMiddleware)
api.add_middleware(ExceptionMiddleware)
