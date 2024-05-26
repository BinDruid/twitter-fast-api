from fastapi import FastAPI

from .core.config import settings
from .core.middleware import ExceptionMiddleware
from .database.config import register_db
from .lifetime import startup
from .routes.users import router as user_router


def get_application() -> FastAPI:
    _app = FastAPI(
        title='fast_micro',
        description='',
        debug=settings.DEBUG,
    )
    _app.include_router(user_router)
    register_db(_app)
    _app.on_event('startup')(startup)

    return _app


app = get_application()

app.add_middleware(ExceptionMiddleware)
