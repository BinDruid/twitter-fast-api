from fastapi import FastAPI

from api.core.config import app_configs
from api.core.middleware import ExceptionMiddleware
from api.core.startup import startup
from .views import router


def get_application() -> FastAPI:
    app = FastAPI(**app_configs)
    app.include_router(router)
    app.on_event('startup')(startup)
    return app


api = get_application()

api.add_middleware(ExceptionMiddleware)
