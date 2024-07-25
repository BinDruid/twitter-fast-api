from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentry_asgi import SentryMiddleware

from twitter_api.core.config import app_configs, settings
from twitter_api.core.lifespan import lifespan
from twitter_api.core.middleware import AuthenticationMiddleware, ExceptionMiddleware, LoggingMiddleware
from twitter_api.routes import api_router


def get_application() -> FastAPI:
    app = FastAPI(**app_configs, lifespan=lifespan)
    app.include_router(api_router)
    return app


api = get_application()

api.add_middleware(SentryMiddleware)
api.add_middleware(LoggingMiddleware)
api.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=('GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'),
    allow_headers=settings.CORS_HEADERS,
)
api.add_middleware(AuthenticationMiddleware)
api.add_middleware(ExceptionMiddleware)
