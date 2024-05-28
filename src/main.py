from fastapi import FastAPI

from .core.config import settings
from .core.middleware import ExceptionMiddleware
from .database.config import register_db
from .lifetime import startup
from .users.routes import router as user_router


def get_application() -> FastAPI:
    app = FastAPI(
        title='fast_micro',
        description='',
        debug=settings.DEBUG,
    )
    app.include_router(user_router)
    register_db(app)
    app.on_event('startup')(startup)

    return app


api = get_application()

api.add_middleware(ExceptionMiddleware)
