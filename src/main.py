from fastapi import FastAPI

from src.core.config import app_configs
from src.core.middleware import ExceptionMiddleware, LoggingMiddleware
from src.core.startup import startup
from src.routes import api_router


def get_application() -> FastAPI:
    app = FastAPI(**app_configs)
    app.include_router(api_router)
    app.on_event('startup')(startup)
    return app


api = get_application()

api.add_middleware(LoggingMiddleware)
api.add_middleware(ExceptionMiddleware)
