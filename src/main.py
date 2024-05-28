from fastapi import FastAPI

from src.core.config import settings
from src.core.middleware import ExceptionMiddleware
from src.database.config import register_db
from src.lifetime import startup
from src.users.routes import router as user_router


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
